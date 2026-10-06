import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import ingest_local_documents


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPOSITORY_ROOT / "ingest_local_documents.py"


class IngestLocalDocumentsTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.source = self.root / "source"
        self.source.mkdir(parents=True)
        self.output = self.root / "output.jsonl"

    def tearDown(self):
        self.temporary_directory.cleanup()

    def read_records(self, output=None):
        path = output or self.output
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]

    def test_records_preserve_content_and_hash_exact_bytes(self):
        raw = "first line\r\nCafé — document\n".encode("utf-8")
        (self.source / "one.txt").write_bytes(raw)

        self.assertEqual(ingest_local_documents.ingest(self.source, self.output, 2), 1)
        self.assertEqual(
            self.read_records(),
            [{
                "source_path": "one.txt",
                "sha256": hashlib.sha256(raw).hexdigest(),
                "content": raw.decode("utf-8"),
            }],
        )

    def test_parallel_output_is_sorted_and_deterministic(self):
        for name, content in (("z.txt", "z\n"), ("nested/a.txt", "a\n"), ("m.TXT", "m\n")):
            path = self.source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

        ingest_local_documents.ingest(self.source, self.output, 4)
        first_output = self.output.read_bytes()
        self.assertEqual(
            [record["source_path"] for record in self.read_records()],
            ["m.TXT", "nested/a.txt", "z.txt"],
        )
        ingest_local_documents.ingest(self.source, self.output, 1)
        self.assertEqual(self.output.read_bytes(), first_output)

    def test_invalid_utf8_fails_without_replacing_existing_output(self):
        self.output.write_bytes(b"prior output\n")
        (self.source / "bad.txt").write_bytes(b"\xff")

        with self.assertRaisesRegex(ingest_local_documents.IngestionError, "invalid UTF-8"):
            ingest_local_documents.ingest(self.source, self.output, 2)

        self.assertEqual(self.output.read_bytes(), b"prior output\n")
        self.assertEqual(list(self.root.glob(".output.jsonl.*.tmp")), [])

    def test_output_inside_source_is_rejected(self):
        with self.assertRaisesRegex(ingest_local_documents.IngestionError, "must not be inside"):
            ingest_local_documents.ingest(self.source, self.source / "result.jsonl", 1)

    def test_symlink_in_source_is_rejected(self):
        target = self.root / "outside.txt"
        target.write_text("outside", encoding="utf-8")
        try:
            (self.source / "linked.txt").symlink_to(target)
        except (NotImplementedError, OSError):
            self.skipTest("symlinks unavailable")

        with self.assertRaisesRegex(ingest_local_documents.IngestionError, "symlink"):
            ingest_local_documents.ingest(self.source, self.output, 1)

    def test_output_write_error_is_explicit_and_atomic(self):
        self.output.write_bytes(b"prior output\n")
        (self.source / "one.txt").write_text("valid", encoding="utf-8")
        original_replace = ingest_local_documents.os.replace

        def fail_replace(source, destination):
            raise OSError("simulated replacement failure")

        ingest_local_documents.os.replace = fail_replace
        try:
            with self.assertRaisesRegex(ingest_local_documents.IngestionError, "cannot write output"):
                ingest_local_documents.ingest(self.source, self.output, 1)
        finally:
            ingest_local_documents.os.replace = original_replace

        self.assertEqual(self.output.read_bytes(), b"prior output\n")
        self.assertEqual(list(self.root.glob(".output.jsonl.*.tmp")), [])

    def test_cli_options_and_default_paths(self):
        args = ingest_local_documents.build_parser().parse_args([])
        self.assertEqual(args.source, ingest_local_documents.DEFAULT_SOURCE)
        self.assertEqual(args.output, ingest_local_documents.DEFAULT_OUTPUT)

        (self.source / "cli.txt").write_text("CLI text", encoding="utf-8")
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--source",
                str(self.source),
                "--output",
                str(self.output),
                "--workers",
                "2",
            ],
            cwd=REPOSITORY_ROOT,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(self.read_records()[0]["content"], "CLI text")

    def test_cli_default_targets_the_repository_paths(self):
        self.assertEqual(
            ingest_local_documents.DEFAULT_SOURCE,
            REPOSITORY_ROOT / "04_LEGAL_GOVERNANCE_AND_FEDERAL_FILINGS",
        )
        self.assertEqual(
            ingest_local_documents.DEFAULT_OUTPUT,
            REPOSITORY_ROOT / "02_DATABASE_AND_STORAGE_LAYERS" / "local_documents.jsonl",
        )


if __name__ == "__main__":
    unittest.main()
