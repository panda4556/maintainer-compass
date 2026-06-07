from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class CheckResult:
    key: str
    title: str
    category: str
    weight: int
    passed: bool
    detail: str
    recommendation: str


@dataclass(frozen=True)
class AuditReport:
    path: str
    created_at: str
    score: int
    max_score: int
    category_scores: dict[str, dict[str, int]]
    checks: list[CheckResult]
    languages: list[str]
    github: dict[str, object] | None = None

    @property
    def percent(self) -> int:
        if self.max_score == 0:
            return 0
        return round((self.score / self.max_score) * 100)


def audit_repository(path: str | Path, github: dict[str, object] | None = None) -> AuditReport:
    root = Path(path).expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"Repository path does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Repository path is not a directory: {root}")

    checks = _build_checks(root)
    score = sum(check.weight for check in checks if check.passed)
    max_score = sum(check.weight for check in checks)
    categories = _category_scores(checks)

    return AuditReport(
        path=str(root),
        created_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        score=score,
        max_score=max_score,
        category_scores=categories,
        checks=checks,
        languages=detect_languages(root),
        github=github,
    )


def detect_languages(root: Path) -> list[str]:
    signals = {
        "Python": ["pyproject.toml", "setup.py", "requirements.txt"],
        "Node.js": ["package.json", "pnpm-lock.yaml", "yarn.lock", "package-lock.json"],
        "Rust": ["Cargo.toml"],
        "Go": ["go.mod"],
        "Java": ["pom.xml", "build.gradle", "settings.gradle"],
        ".NET": ["*.csproj", "*.sln"],
    }
    languages: list[str] = []
    for language, patterns in signals.items():
        if any(_exists(root, pattern) for pattern in patterns):
            languages.append(language)
    return languages


def _build_checks(root: Path) -> list[CheckResult]:
    return [
        _check(
            root,
            key="readme",
            title="README",
            category="Onboarding",
            weight=12,
            passed=_has_any(root, ["README.md", "README.rst", "README.txt"]),
            detail="A README helps users and contributors understand the project quickly.",
            recommendation="Add a README with purpose, install steps, usage, and contribution links.",
        ),
        _check(
            root,
            key="license",
            title="License",
            category="Onboarding",
            weight=8,
            passed=_has_any(root, ["LICENSE", "LICENSE.md", "COPYING"]),
            detail="A license makes reuse rights explicit.",
            recommendation="Add an OSI-approved license file.",
        ),
        _check(
            root,
            key="contributing",
            title="Contribution guide",
            category="Onboarding",
            weight=7,
            passed=_has_any(root, ["CONTRIBUTING.md", ".github/CONTRIBUTING.md", "docs/CONTRIBUTING.md"]),
            detail="A contribution guide reduces repeated maintainer explanations.",
            recommendation="Add CONTRIBUTING.md with setup, tests, and pull request expectations.",
        ),
        _check(
            root,
            key="code_of_conduct",
            title="Code of conduct",
            category="Governance",
            weight=4,
            passed=_has_any(root, ["CODE_OF_CONDUCT.md", ".github/CODE_OF_CONDUCT.md"]),
            detail="A code of conduct sets collaboration expectations.",
            recommendation="Add CODE_OF_CONDUCT.md for community behavior expectations.",
        ),
        _check(
            root,
            key="security",
            title="Security policy",
            category="Governance",
            weight=7,
            passed=_has_any(root, ["SECURITY.md", ".github/SECURITY.md"]),
            detail="A security policy gives users a safe reporting path.",
            recommendation="Add SECURITY.md with private vulnerability reporting guidance.",
        ),
        _check(
            root,
            key="issue_templates",
            title="Issue templates",
            category="Governance",
            weight=5,
            passed=_directory_has_files(root, ".github/ISSUE_TEMPLATE")
            or _has_any(root, [".github/ISSUE_TEMPLATE.md", "ISSUE_TEMPLATE.md"]),
            detail="Issue templates reduce triage time and collect reproducible details.",
            recommendation="Add bug and feature request templates under .github/ISSUE_TEMPLATE.",
        ),
        _check(
            root,
            key="pull_request_template",
            title="Pull request template",
            category="Governance",
            weight=4,
            passed=_has_any(root, [".github/pull_request_template.md", "pull_request_template.md"]),
            detail="A pull request template prompts contributors for tests and context.",
            recommendation="Add .github/pull_request_template.md with summary and test plan sections.",
        ),
        _check(
            root,
            key="ci",
            title="Continuous integration",
            category="Automation",
            weight=10,
            passed=_directory_has_files(root, ".github/workflows", suffixes=(".yml", ".yaml"))
            or _has_any(root, [".gitlab-ci.yml", ".circleci/config.yml"]),
            detail="CI catches regressions before maintainers review or release changes.",
            recommendation="Add a CI workflow that runs tests on pull requests.",
        ),
        _check(
            root,
            key="dependency_automation",
            title="Dependency automation",
            category="Automation",
            weight=4,
            passed=_has_any(root, [".github/dependabot.yml", "renovate.json", ".renovaterc"]),
            detail="Dependency automation keeps projects current with less manual checking.",
            recommendation="Add Dependabot or Renovate configuration if dependencies need monitoring.",
        ),
        _check(
            root,
            key="tests",
            title="Tests",
            category="Automation",
            weight=8,
            passed=_has_tests(root),
            detail="Tests make review safer and reduce maintainer uncertainty.",
            recommendation="Add tests or document how verification is performed.",
        ),
        _check(
            root,
            key="package_metadata",
            title="Package metadata",
            category="Release readiness",
            weight=6,
            passed=_has_any(root, ["pyproject.toml", "package.json", "Cargo.toml", "go.mod", "pom.xml", "*.csproj"]),
            detail="Package metadata helps users install and verify versions.",
            recommendation="Add package metadata for the primary ecosystem.",
        ),
        _check(
            root,
            key="changelog",
            title="Changelog",
            category="Release readiness",
            weight=5,
            passed=_has_any(root, ["CHANGELOG.md", "CHANGES.md", "HISTORY.md", "RELEASES.md"]),
            detail="A changelog makes upgrades and releases easier to audit.",
            recommendation="Add CHANGELOG.md or release notes.",
        ),
        _check(
            root,
            key="docs",
            title="Documentation directory",
            category="Onboarding",
            weight=4,
            passed=_directory_has_files(root, "docs"),
            detail="A docs directory gives longer guidance a stable home.",
            recommendation="Add docs/ for deeper usage, architecture, or maintainer notes.",
        ),
        _check(
            root,
            key="examples",
            title="Examples",
            category="Onboarding",
            weight=3,
            passed=_directory_has_files(root, "examples"),
            detail="Examples help users succeed without maintainer intervention.",
            recommendation="Add examples/ with realistic usage samples.",
        ),
        _check(
            root,
            key="gitignore",
            title="Git ignore rules",
            category="Automation",
            weight=2,
            passed=_has_any(root, [".gitignore"]),
            detail="Ignore rules prevent generated files from polluting reviews.",
            recommendation="Add .gitignore for build, cache, and environment artifacts.",
        ),
    ]


def _check(
    root: Path,
    *,
    key: str,
    title: str,
    category: str,
    weight: int,
    passed: bool,
    detail: str,
    recommendation: str,
) -> CheckResult:
    return CheckResult(
        key=key,
        title=title,
        category=category,
        weight=weight,
        passed=passed,
        detail=detail,
        recommendation=recommendation,
    )


def _category_scores(checks: Iterable[CheckResult]) -> dict[str, dict[str, int]]:
    scores: dict[str, dict[str, int]] = {}
    for check in checks:
        category = scores.setdefault(check.category, {"score": 0, "max_score": 0})
        category["max_score"] += check.weight
        if check.passed:
            category["score"] += check.weight
    return scores


def _has_any(root: Path, candidates: Iterable[str]) -> bool:
    return any(_exists(root, candidate) for candidate in candidates)


def _exists(root: Path, candidate: str) -> bool:
    if "*" in candidate:
        return any(root.glob(candidate))
    return _candidate_path(root, candidate) is not None


def _candidate_path(root: Path, candidate: str) -> Path | None:
    path = root / candidate
    if path.exists():
        return path
    return _case_insensitive_path(root, candidate)


def _case_insensitive_path(root: Path, candidate: str) -> Path | None:
    current = root
    for part in Path(candidate).parts:
        if not current.is_dir():
            return None
        matches = [child for child in current.iterdir() if child.name.lower() == part.lower()]
        if not matches:
            return None
        current = matches[0]
    return current


def _directory_has_files(root: Path, candidate: str, *, suffixes: tuple[str, ...] | None = None) -> bool:
    directory = _candidate_path(root, candidate)
    if directory is None or not directory.is_dir():
        return False
    files = (path for path in directory.rglob("*") if path.is_file())
    if suffixes is None:
        return any(files)
    normalized_suffixes = tuple(suffix.lower() for suffix in suffixes)
    return any(path.name.lower().endswith(normalized_suffixes) for path in files)


def _has_tests(root: Path) -> bool:
    if any(_directory_has_files(root, candidate) for candidate in ["tests", "test", "__tests__"]):
        return True
    patterns = ["test_*.py", "*_test.py", "*.test.js", "*.spec.js", "*Test.java", "*Tests.cs"]
    return any(next(root.rglob(pattern), None) is not None for pattern in patterns)
