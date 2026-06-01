# Maintainer Compass

Maintainer Compass is a zero-dependency CLI that audits an open-source
repository for maintenance readiness. It turns common maintainer work into a
small, repeatable report: onboarding files, governance docs, CI, tests, release
signals, and contributor workflows.

The project is designed for small and mid-sized OSS maintainers who want a
clear, automated way to answer:

- Can a new contributor understand how to help?
- Are maintenance expectations visible?
- Do pull requests have enough automation around them?
- What should the maintainer fix first?

## Features

- Local repository audit with no network required.
- Optional GitHub metadata lookup for public repositories.
- Markdown or JSON output for humans, bots, and GitHub Actions.
- Weighted score across onboarding, governance, automation, and release
  readiness.
- Actionable recommendations instead of vague pass/fail messages.
- Standard library only. No runtime dependencies.

## Quick start

```bash
python -m pip install -e .
python -m maintainer_compass audit . --format markdown
```

Audit a public GitHub repository and include public metadata:

```bash
python -m maintainer_compass audit . \
  --github https://github.com/panda4556/maintainer-compass \
  --format markdown \
  --output maintainer-compass-report.md
```

Generate JSON for automation:

```bash
python -m maintainer_compass audit . --format json
```

## Example output

```text
Maintainer Compass score: 76/100

Top recommendations:
1. Add SECURITY.md so users know how to report vulnerabilities.
2. Add pull request and issue templates to reduce maintainer triage load.
3. Add release notes or CHANGELOG.md to make upgrades easier.
```

## GitHub Actions

```yaml
name: Maintainer Compass

on:
  pull_request:
  workflow_dispatch:
  schedule:
    - cron: "0 8 * * 1"

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python -m pip install -e .
      - run: python -m maintainer_compass audit . --format markdown --output maintainer-compass-report.md
      - uses: actions/upload-artifact@v4
        with:
          name: maintainer-compass-report
          path: maintainer-compass-report.md
```

## What gets checked

Maintainer Compass looks for practical OSS maintenance signals:

- README, license, contribution guide, security policy, code of conduct.
- Issue templates, pull request template, support or funding files.
- CI workflows, dependency automation, tests, package metadata.
- Changelog, docs, examples, release and version files.
- Language-specific signals for Python, Node.js, Rust, Go, Java, and .NET.

The score is not meant to shame a project. It is a map for the next few
maintenance improvements.

## Roadmap

- Comment reports directly on pull requests.
- Produce suggested issue labels from audit results.
- Add optional OpenAI-powered issue triage summaries for maintainers who opt in.
- Track score history over time.
- Export SARIF for repository health checks.

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md)
before opening a pull request.

## License

MIT. See [LICENSE](LICENSE).

