from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from maintainer_compass.audit import audit_repository, detect_languages


class AuditRepositoryTests(unittest.TestCase):
    def test_scores_repository_health_signals(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "README.md").write_text("# Example\n", encoding="utf-8")
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            (root / "pyproject.toml").write_text("[project]\nname='example'\n", encoding="utf-8")
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / ".github" / "workflows" / "ci.yml").write_text("name: CI\n", encoding="utf-8")
            (root / "tests").mkdir()
            (root / "tests" / "test_example.py").write_text("def test_ok(): pass\n", encoding="utf-8")

            report = audit_repository(root)

        checks = {check.key: check for check in report.checks}
        self.assertTrue(checks["readme"].passed)
        self.assertTrue(checks["license"].passed)
        self.assertTrue(checks["ci"].passed)
        self.assertTrue(checks["tests"].passed)
        self.assertIn("Python", report.languages)
        self.assertGreater(report.score, 0)
        self.assertLess(report.score, report.max_score)

    def test_detects_language_signals(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "package.json").write_text('{"name": "example"}\n', encoding="utf-8")
            (root / "go.mod").write_text("module example\n", encoding="utf-8")

            languages = detect_languages(root)

        self.assertEqual(languages, ["Node.js", "Go"])

    def test_missing_path_raises(self) -> None:
        with self.assertRaises(FileNotFoundError):
            audit_repository("does-not-exist")


if __name__ == "__main__":
    unittest.main()

