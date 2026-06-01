from __future__ import annotations

import json
from dataclasses import asdict

from .audit import AuditReport, CheckResult


def render_report(report: AuditReport, output_format: str) -> str:
    if output_format == "json":
        return render_json(report)
    if output_format == "markdown":
        return render_markdown(report)
    raise ValueError(f"Unsupported format: {output_format}")


def render_json(report: AuditReport) -> str:
    return json.dumps(asdict(report), indent=2, sort_keys=True)


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
    lines = ["## Category scores", "", "| Category | Score |", "| --- | ---: |"]
    for category, scores in sorted(report.category_scores.items()):
        lines.append(f"| {category} | {scores['score']}/{scores['max_score']} |")
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

