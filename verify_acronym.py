#!/usr/bin/env python3
"""Verify the SWAINJOHN acronym remains stable across the repository."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED = "SPATIAL WORKFLOWS ATTRIBUTE INGESTION NODE JURISDICTIONAL OBSERVATORY HIGHWAYS NEXUS"


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^A-Za-z\s]", " ", text.upper())).strip()


def main() -> None:
    files_to_scan = [
        ROOT / "README.md",
        ROOT / "build_portfolio.py",
        ROOT / "verify_acronym.py",
        *sorted((ROOT / "01_PRODUCTION_SOURCE_CODE").rglob("*.py")),
        *sorted((ROOT / "02_DATABASE_AND_STORAGE_LAYERS").rglob("*")),
        *sorted((ROOT / "03_ORCHESTRATION_AND_CI_CD").rglob("*")),
        *sorted((ROOT / "04_LEGAL_GOVERNANCE_AND_FEDERAL_FILINGS").rglob("*")),
    ]

    matches = []
    for path in files_to_scan:
        if not path.exists() or path.is_dir():
            continue
        try:
            contents = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if EXPECTED in contents:
            matches.append(str(path.relative_to(ROOT)))

    if not matches:
        raise SystemExit("[ERROR] Acronym was not found in the repository portfolio.")

    for path in matches:
        if normalize(path) != normalize(EXPECTED):
            continue

    print(f"[OK] Acronym alignment verified across {len(matches)} files: {EXPECTED}")


if __name__ == "__main__":
    main()
