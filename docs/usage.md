# Usage Guide

Maintainer Compass can be used locally, in CI, or as a lightweight audit step
before preparing a release.

## Local Audit

```bash
python -m pip install -e .
python -m maintainer_compass audit . --format markdown
```

## JSON for Automation

```bash
python -m maintainer_compass audit . --format json --output report.json
```

JSON output includes the total score, category scores, detected languages,
individual checks, and optional GitHub metadata.

## SARIF for Code Scanning

```bash
python -m maintainer_compass audit . --format sarif --output maintainer-compass.sarif
```

SARIF output maps failed maintenance checks to warning results. This lets
GitHub Actions upload repository health findings to Code Scanning:

```yaml
- run: python -m maintainer_compass audit . --format sarif --output maintainer-compass.sarif
- uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: maintainer-compass.sarif
```

## Quality Gates

Use `--fail-under` when you want CI to fail below a minimum score:

```bash
python -m maintainer_compass audit . --fail-under 80
```

The command still prints the report, then exits with status `1` if the
percentage is below the threshold.

Markdown reports include category percentages so maintainers can see whether a
repository is mainly missing onboarding, governance, automation, or release
readiness work.

## GitHub Metadata

Local checks do not require network access. Public GitHub metadata is optional:

```bash
python -m maintainer_compass audit . \
  --github https://github.com/panda4556/maintainer-compass \
  --ignore-github-errors
```

Set `GITHUB_TOKEN` or `GH_TOKEN` to use authenticated GitHub API requests.
