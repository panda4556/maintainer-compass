from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from . import __version__
from .audit import audit_repository
from .github import fetch_github_metadata, token_from_environment
from .report import render_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="maintainer-compass",
        description="Audit an OSS repository for maintenance readiness.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command")

    audit = subparsers.add_parser("audit", help="Audit a local repository.")
    audit.add_argument("path", nargs="?", default=".", help="Repository path to audit.")
    audit.add_argument(
        "--format",
        choices=["markdown", "json", "sarif"],
        default="markdown",
        help="Report format.",
    )
    audit.add_argument("--output", "-o", help="Write report to a file instead of stdout.")
    audit.add_argument("--github", help="Public GitHub repository URL to include metadata.")
    audit.add_argument(
        "--fail-under",
        type=int,
        metavar="PERCENT",
        help="Exit with status 1 if the score percentage is below this threshold.",
    )
    audit.add_argument(
        "--ignore-github-errors",
        action="store_true",
        help="Continue if public GitHub metadata cannot be fetched.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    raw_args = list(argv) if argv is not None else sys.argv[1:]
    if not raw_args or raw_args[0] not in {"audit", "-h", "--help", "--version"}:
        raw_args = ["audit", *raw_args]
    args = parser.parse_args(raw_args)

    try:
        return _run_audit(args)
    except (FileNotFoundError, NotADirectoryError, ValueError, RuntimeError) as exc:
        print(f"maintainer-compass: {exc}", file=sys.stderr)
        return 2


def _run_audit(args: argparse.Namespace) -> int:
    if args.fail_under is not None and not 0 <= args.fail_under <= 100:
        raise ValueError("--fail-under must be between 0 and 100")

    github_metadata = None
    if args.github:
        try:
            github_metadata = fetch_github_metadata(args.github, token_from_environment())
        except RuntimeError:
            if not args.ignore_github_errors:
                raise

    report = audit_repository(args.path, github=github_metadata)
    rendered = render_report(report, args.format)

    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")

    if args.fail_under is not None and report.percent < args.fail_under:
        print(
            f"maintainer-compass: score {report.percent}% is below required threshold {args.fail_under}%",
            file=sys.stderr,
        )
        return 1
    return 0
