from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

from maintainer_compass.cli import main


class CliTests(unittest.TestCase):
    def test_writes_json_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "README.md").write_text("# Example\n", encoding="utf-8")
            output = root / "report.json"

            code = main(["audit", str(root), "--format", "json", "--output", str(output)])

            payload = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(code, 0)
        self.assertIn("score", payload)
        self.assertEqual(payload["path"], str(root.resolve()))

    def test_writes_sarif_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            output = root / "report.sarif"

            code = main(["audit", str(root), "--format", "sarif", "--output", str(output)])

            payload = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(code, 0)
        self.assertEqual(payload["version"], "2.1.0")
        self.assertEqual(payload["runs"][0]["tool"]["driver"]["name"], "Maintainer Compass")
        self.assertGreater(len(payload["runs"][0]["results"]), 0)

    def test_default_command_is_audit(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "README.md").write_text("# Example\n", encoding="utf-8")

            stdout = StringIO()
            with redirect_stdout(stdout):
                code = main([str(root), "--format", "json"])

        self.assertEqual(code, 0)
        self.assertIn('"score"', stdout.getvalue())

    def test_fail_under_returns_one_when_score_is_too_low(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            stdout = StringIO()
            stderr = StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                code = main(["audit", temp, "--format", "json", "--fail-under", "90"])

        self.assertEqual(code, 1)
        self.assertIn('"score"', stdout.getvalue())
        self.assertIn("below required threshold 90%", stderr.getvalue())

    def test_fail_under_rejects_invalid_threshold(self) -> None:
        stderr = StringIO()

        with redirect_stderr(stderr):
            code = main(["audit", ".", "--fail-under", "101"])

        self.assertEqual(code, 2)
        self.assertIn("--fail-under must be between 0 and 100", stderr.getvalue())

    def test_version_flag_prints_version(self) -> None:
        stdout = StringIO()

        with self.assertRaises(SystemExit) as raised, redirect_stdout(stdout):
            main(["--version"])

        self.assertEqual(raised.exception.code, 0)
        self.assertIn("maintainer-compass 0.3.0", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
