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

    def test_empty_signal_directories_do_not_pass_checks(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / ".github" / "ISSUE_TEMPLATE").mkdir()
            (root / "tests").mkdir()
            (root / "docs").mkdir()
            (root / "examples").mkdir()

            report = audit_repository(root)

        checks = {check.key: check for check in report.checks}
        self.assertFalse(checks["ci"].passed)
        self.assertFalse(checks["issue_templates"].passed)
        self.assertFalse(checks["tests"].passed)
        self.assertFalse(checks["docs"].passed)
        self.assertFalse(checks["examples"].passed)

    def test_populated_signal_directories_pass_checks_case_insensitively(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / ".GitHub" / "Workflows").mkdir(parents=True)
            (root / ".GitHub" / "Workflows" / "ci.YAML").write_text("name: CI\n", encoding="utf-8")
            (root / ".GitHub" / "ISSUE_TEMPLATE").mkdir()
            (root / ".GitHub" / "ISSUE_TEMPLATE" / "bug.yml").write_text("name: Bug\n", encoding="utf-8")
            (root / "Tests").mkdir()
            (root / "Tests" / "test_example.py").write_text("def test_ok(): pass\n", encoding="utf-8")
            (root / "Docs").mkdir()
            (root / "Docs" / "usage.md").write_text("# Usage\n", encoding="utf-8")
            (root / "Examples").mkdir()
            (root / "Examples" / "sample.md").write_text("# Sample\n", encoding="utf-8")

            report = audit_repository(root)

        checks = {check.key: check for check in report.checks}
        self.assertTrue(checks["ci"].passed)
        self.assertTrue(checks["issue_templates"].passed)
        self.assertTrue(checks["tests"].passed)
        self.assertTrue(checks["docs"].passed)
        self.assertTrue(checks["examples"].passed)

    def test_missing_path_raises(self) -> None:
        with self.assertRaises(FileNotFoundError):
            audit_repository("does-not-exist")


if __name__ == "__main__":
    unittest.main()
