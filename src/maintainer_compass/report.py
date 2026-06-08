from __future__ import annotations

import json
from dataclasses import asdict

from .audit import AuditReport, CheckResult


def render_report(report: AuditReport, output_format: str) -> str:
    if output_format == "json":
        return render_json(report)
    if output_format == "markdown":
        return render_markdown(report)
    if output_format == "sarif":
        return render_sarif(report)
    raise ValueError(f"Unsupported format: {output_format}")


def render_json(report: AuditReport) -> str:
    return json.dumps(asdict(report), indent=2, sort_keys=True)


def render_sarif(report: AuditReport) -> str:
    rules = [_sarif_rule(check) for check in report.checks]
    results = [_sarif_result(report, check) for check in report.checks if not check.passed]
    payload = {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "automationDetails": {
                    "id": "maintainer-compass/repository-health",
                },
                "invocations": [
                    {
                        "executionSuccessful": True,
                    }
                ],
                "tool": {
                    "driver": {
                        "name": "Maintainer Compass",
                        "informationUri": "https://github.com/panda4556/maintainer-compass",
                        "rules": rules,
                    }
                },
                "results": results,
                "properties": {
                    "score": report.score,
                    "maxScore": report.max_score,
                    "percent": report.percent,
                    "generatedAt": report.created_at,
                    "detectedLanguages": report.languages,
                },
            }
        ],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def render_markdown(report: AuditReport) -> str:
    lines: list[str] = [
        "# Maintainer Compass Report",
        "",
        f"Repository: `{report.path}`",
        f"Generated: `{report.created_at}`",
        "",
        f"Score: **{report.score}/{report.max_score}** ({report.percent}%)",
        "",
    ]

    if report.github:
        lines.extend(_github_lines(report.github))

    if report.languages:
        lines.extend(["## Detected languages", "", ", ".join(report.languages), ""])

    lines.extend(_category_lines(report))
    lines.extend(_recommendation_lines(report.checks))
    lines.extend(_check_lines(report.checks))
    return "\n".join(lines).rstrip() + "\n"


def _github_lines(github: dict[str, object]) -> list[str]:
    lines = ["## GitHub metadata", ""]
    labels = [
        ("url", "URL"),
        ("stars", "Stars"),
        ("forks", "Forks"),
        ("open_issues", "Open issues"),
        ("license", "License"),
        ("pushed_at", "Last push"),
    ]
    for key, label in labels:
        value = github.get(key)
        if value not in (None, ""):
            lines.append(f"- {label}: {value}")
    lines.append("")
    return lines


def _category_lines(report: AuditReport) -> list[str]:
    lines = ["## Category scores", "", "| Category | Score | Percent |", "| --- | ---: | ---: |"]
    for category, scores in sorted(report.category_scores.items()):
        percent = _score_percent(scores["score"], scores["max_score"])
        lines.append(f"| {category} | {scores['score']}/{scores['max_score']} | {percent}% |")
    lines.append("")
    return lines


def _recommendation_lines(checks: list[CheckResult]) -> list[str]:
    failed = [check for check in checks if not check.passed]
    failed.sort(key=lambda check: check.weight, reverse=True)
    lines = ["## Top recommendations", ""]
    if not failed:
        lines.append("No missing checks. Keep maintaining the project and review this report as the project grows.")
        lines.append("")
        return lines

    for index, check in enumerate(failed[:5], start=1):
        lines.append(f"{index}. **{check.title}**: {check.recommendation}")
    lines.append("")
    return lines


def _check_lines(checks: list[CheckResult]) -> list[str]:
    lines = ["## Checks", "", "| Status | Category | Check | Weight |", "| --- | --- | --- | ---: |"]
    for check in checks:
        status = "PASS" if check.passed else "TODO"
        lines.append(f"| {status} | {check.category} | {check.title} | {check.weight} |")
    lines.append("")
    return lines


def _sarif_rule(check: CheckResult) -> dict[str, object]:
    return {
        "id": check.key,
        "name": check.title,
        "shortDescription": {"text": check.title},
        "fullDescription": {"text": check.detail},
        "help": {
            "text": check.recommendation,
            "markdown": check.recommendation,
        },
        "properties": {
            "category": check.category,
            "weight": check.weight,
        },
    }


def _sarif_result(report: AuditReport, check: CheckResult) -> dict[str, object]:
    return {
        "ruleId": check.key,
        "level": "warning",
        "message": {"text": check.recommendation},
        "locations": [
            {
                "physicalLocation": {
                    "artifactLocation": {
                        "uri": ".",
                    },
                }
            }
        ],
        "properties": {
            "category": check.category,
            "weight": check.weight,
        },
    }


def _score_percent(score: int, max_score: int) -> int:
    if max_score == 0:
        return 0
    return round((score / max_score) * 100)
