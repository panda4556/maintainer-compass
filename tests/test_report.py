from __future__ import annotations

import unittest
import json

from maintainer_compass.audit import AuditReport, CheckResult
from maintainer_compass.report import render_json, render_markdown, render_sarif


def _sample_report() -> AuditReport:
    return AuditReport(
        path="/repo",
        created_at="2026-06-07T00:00:00+00:00",
        score=10,
        max_score=20,
        category_scores={"Automation": {"score": 0, "max_score": 10}, "Onboarding": {"score": 10, "max_score": 10}},
        checks=[
            CheckResult(
                key="readme",
                title="README",
                category="Onboarding",
                weight=10,
                passed=True,
                detail="A README helps users.",
                recommendation="Add README.md.",
            ),
            CheckResult(
                key="ci",
                title="Continuous integration",
                category="Automation",
                weight=10,
                passed=False,
                detail="CI catches regressions.",
                recommendation="Add CI.",
            ),
        ],
        languages=["Python"],
        github={"url": "https://github.com/panda4556/maintainer-compass", "stars": 1},
    )


class ReportRenderingTests(unittest.TestCase):
    def test_render_markdown_includes_recommendations_and_metadata(self) -> None:
        rendered = render_markdown(_sample_report())

        self.assertIn("# Maintainer Compass Report", rendered)
        self.assertIn("Score: **10/20** (50%)", rendered)
        self.assertIn("## GitHub metadata", rendered)
        self.assertIn("| Automation | 0/10 | 0% |", rendered)
        self.assertIn("| Onboarding | 10/10 | 100% |", rendered)
        self.assertIn("**Continuous integration**: Add CI.", rendered)

    def test_render_json_is_stable_and_sorted(self) -> None:
        rendered = render_json(_sample_report())

        self.assertIn('"created_at": "2026-06-07T00:00:00+00:00"', rendered)
        self.assertIn('"github"', rendered)
        self.assertIn('"languages"', rendered)

    def test_render_sarif_includes_failed_checks_as_results(self) -> None:
        payload = json.loads(render_sarif(_sample_report()))
        run = payload["runs"][0]

        self.assertEqual(payload["version"], "2.1.0")
        self.assertEqual(run["tool"]["driver"]["name"], "Maintainer Compass")
        self.assertEqual(run["automationDetails"]["id"], "maintainer-compass/repository-health")
        self.assertTrue(run["invocations"][0]["executionSuccessful"])
        self.assertEqual(run["properties"]["percent"], 50)
        self.assertEqual(len(run["tool"]["driver"]["rules"]), 2)
        self.assertEqual(len(run["results"]), 1)
        self.assertEqual(run["results"][0]["ruleId"], "ci")
        self.assertEqual(run["results"][0]["level"], "warning")
        self.assertEqual(run["results"][0]["locations"][0]["physicalLocation"]["artifactLocation"]["uri"], ".")


if __name__ == "__main__":
    unittest.main()
