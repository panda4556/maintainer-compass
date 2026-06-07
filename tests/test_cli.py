from __future__ import annotations

import json
import tempfile
import unittest
from contextlib import redirect_stdout
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

    def test_default_command_is_audit(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "README.md").write_text("# Example\n", encoding="utf-8")

            stdout = StringIO()
            with redirect_stdout(stdout):
                code = main([str(root), "--format", "json"])

        self.assertEqual(code, 0)
        self.assertIn('"score"', stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
