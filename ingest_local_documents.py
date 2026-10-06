#!/usr/bin/env python3
"""Ingest local UTF-8 text files into a deterministic JSON Lines archive."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
import stat
import sys
import tempfile
from pathlib import Path
from typing import Iterable


REPOSITORY_ROOT = Path(__file__).resolve().parent
DEFAULT_SOURCE = REPOSITORY_ROOT / "04_LEGAL_GOVERNANCE_AND_FEDERAL_FILINGS"
DEFAULT_OUTPUT = REPOSITORY_ROOT / "02_DATABASE_AND_STORAGE_LAYERS" / "local_documents.jsonl"
MAX_WORKERS = 32


class IngestionError(Exception):
    """An expected failure while discovering, reading, or writing documents."""


def _check_no_symlink_components(path: Path) -> None:
    """Reject symlinks in existing path components instead of following them."""
    absolute = Path(os.path.abspath(path))
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        try:
            if current.is_symlink():
                raise IngestionError(f"unsafe symlink path: {current}")
        except OSError as exc:
            raise IngestionError(f"cannot inspect path {current}: {exc}") from exc


def _discover_text_files(source: Path) -> list[Path]:
    _check_no_symlink_components(source)
    if not source.exists() or not source.is_dir():
        raise IngestionError(f"source is not a directory: {source}")

    discovered: list[Path] = []

    def fail_scan(error: OSError) -> None:
        raise IngestionError(f"cannot scan source directory {source}: {error}") from error

    try:
        for root, directories, filenames in os.walk(
            source, topdown=True, onerror=fail_scan, followlinks=False
        ):
            root_path = Path(root)
            for name in directories:
                candidate = root_path / name
                if candidate.is_symlink():
                    raise IngestionError(f"unsafe symlink directory in source: {candidate}")
            for name in filenames:
                candidate = root_path / name
                if candidate.is_symlink():
                    raise IngestionError(f"unsafe symlink file in source: {candidate}")
                if candidate.suffix.lower() == ".txt":
                    if not stat.S_ISREG(candidate.lstat().st_mode):
                        raise IngestionError(f"source is not a regular file: {candidate}")
                    discovered.append(candidate)
    except OSError as exc:
        raise IngestionError(f"cannot scan source directory {source}: {exc}") from exc

    return sorted(discovered, key=lambda path: path.relative_to(source).as_posix())


def _read_document(path: Path, source: Path) -> dict[str, str]:
    relative_path = path.relative_to(source).as_posix()
    descriptor: int | None = None
    try:
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(path, flags)
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise IngestionError(f"source is not a regular file: {relative_path}")
        with os.fdopen(descriptor, "rb") as document:
            descriptor = None
            raw = document.read()
    except IngestionError:
        raise
    except OSError as exc:
        raise IngestionError(f"cannot read {relative_path}: {exc}") from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)
    try:
        content = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise IngestionError(f"invalid UTF-8 in {relative_path}: {exc}") from exc
    return {
        "source_path": relative_path,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "content": content,
    }


def _validate_output_path(source: Path, output: Path) -> Path:
    _check_no_symlink_components(output)
    resolved_source = source.resolve(strict=True)
    resolved_output = output.resolve(strict=False)
    try:
        resolved_output.relative_to(resolved_source)
    except ValueError:
        return output
    raise IngestionError(f"output must not be inside source directory: {output}")


def _write_atomically(output: Path, records: Iterable[dict[str, str]]) -> None:
    temporary_path: Path | None = None
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=output.parent,
            prefix=f".{output.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
            for record in records:
                temporary.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")))
                temporary.write("\n")
            temporary.flush()
            os.fsync(temporary.fileno())
        os.replace(temporary_path, output)
        temporary_path = None
    except OSError as exc:
        raise IngestionError(f"cannot write output {output}: {exc}") from exc
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass


def ingest(source: Path, output: Path, workers: int) -> int:
    """Read UTF-8 .txt files in parallel and atomically write sorted JSONL."""
    if workers < 1 or workers > MAX_WORKERS:
        raise IngestionError(f"workers must be between 1 and {MAX_WORKERS}")
    source = Path(os.path.abspath(source))
    output = Path(os.path.abspath(output))
    _check_no_symlink_components(source)
    if not source.exists() or not source.is_dir():
        raise IngestionError(f"source is not a directory: {source}")
    output = _validate_output_path(source, output)
    files = _discover_text_files(source)

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            records = list(executor.map(lambda path: _read_document(path, source), files))
    except IngestionError:
        raise
    except OSError as exc:
        raise IngestionError(f"document processing failed: {exc}") from exc

    _write_atomically(output, records)
    return len(records)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ingest local UTF-8 .txt files into deterministic JSON Lines (no network access)."
    )
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE, help="source directory")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="JSONL output path")
    parser.add_argument(
        "--workers",
        type=int,
        default=min(8, os.cpu_count() or 1),
        help=f"parallel file readers (1-{MAX_WORKERS}; default: min(8, CPU count))",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        count = ingest(args.source, args.output, args.workers)
    except IngestionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"Ingested {count} document(s) to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
