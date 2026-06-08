# Maintainer Compass

[![CI](https://github.com/panda4556/maintainer-compass/actions/workflows/ci.yml/badge.svg)](https://github.com/panda4556/maintainer-compass/actions/workflows/ci.yml)
[![GitHub release](https://img.shields.io/github/v/release/panda4556/maintainer-compass?include_prereleases)](https://github.com/panda4556/maintainer-compass/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Maintainer Compass is a zero-dependency CLI that audits an open-source
repository for maintenance readiness. It turns common maintainer work into a
small, repeatable report: onboarding files, governance docs, CI, tests, release
signals, and contributor workflows.

It is built for maintainers who want a practical answer to: "What should we fix
next so this repository is easier to contribute to, safer to maintain, and more
ready for releases?"

The project is designed for small and mid-sized OSS maintainers who want a
clear, automated way to answer:

- Can a new contributor understand how to help?
- Are maintenance expectations visible?
- Do pull requests have enough automation around them?
- What should the maintainer fix first?

## 中文说明

Maintainer Compass 是一个零运行时依赖的开源项目维护健康度检查工具。
它会扫描本地仓库，并生成 Markdown 或 JSON 报告，帮助维护者快速了解
README、许可证、贡献指南、安全策略、Issue/PR 模板、CI、测试、文档、
示例和发布准备情况。

这个项目适合个人维护者、小型开源团队和贡献者使用：你可以在提交前检查
仓库维护基础设施，也可以把它放进 GitHub Actions，定期生成项目健康报告。
它的目标不是给项目“打分羞辱”，而是指出下一步最值得补齐的维护工作。

这个仓库也会作为 Claude for OSS 申请项目持续维护。未来的 AI 功能会保持
可选、透明和安全：核心扫描仍然本地运行，AI 只用于帮助维护者整理 issue、
生成发布说明、改写建议和减少重复 triage 工作。

## Features

- Local repository audit with no network required.
- Optional GitHub metadata lookup for public repositories.
- Markdown, JSON, or SARIF output for humans, bots, and GitHub Actions.
- Weighted score across onboarding, governance, automation, and release
  readiness.
- Actionable recommendations instead of vague pass/fail messages.
- CI-friendly quality gate with `--fail-under`.
- Maintainer-focused docs for support, triage, releases, and roadmap planning.
- Package build validation and typed package metadata.
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

Generate SARIF for GitHub Code Scanning or security dashboards:

```bash
python -m maintainer_compass audit . --format sarif --output maintainer-compass.sarif
```

Fail CI if a repository falls below a score threshold:

```bash
python -m maintainer_compass audit . --fail-under 80
```

Print the installed version:

```bash
python -m maintainer_compass --version
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
      - run: python -m maintainer_compass audit . --format sarif --output maintainer-compass.sarif
      - uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: maintainer-compass.sarif
      - uses: actions/upload-artifact@v4
        with:
          name: maintainer-compass-report
          path: |
            maintainer-compass-report.md
            maintainer-compass.sarif
```

## What gets checked

Maintainer Compass looks for practical OSS maintenance signals:

- README, license, contribution guide, security policy, code of conduct.
- Support policy, maintainer guide, issue label taxonomy, issue templates,
  pull request template.
- CI workflows, dependency automation, tests, package metadata.
- Changelog, release workflow, docs, examples, roadmap, release and version files.
- Language-specific signals for Python, Node.js, Rust, Go, Java, and .NET.

The score is not meant to shame a project. It is a map for the next few
maintenance improvements.

## Roadmap

See [ROADMAP.md](ROADMAP.md) for planned work, including score history,
ecosystem-specific checks, and optional AI-assisted maintainer workflows.

## Documentation

- [Usage guide](docs/usage.md)
- [Scoring model](docs/scoring.md)
- [AI-assisted maintainer workflows](docs/ai-maintainer-workflows.md)
- [Security design notes](docs/security-design.md)
- [Packaging](docs/packaging.md)
- [Claude for OSS application notes](docs/claude-for-oss-application.md)
- [Maintainer guide](MAINTAINERS.md)
- [Support policy](SUPPORT.md)

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md)
before opening a pull request.

## License

MIT. See [LICENSE](LICENSE).

## Downloads

[![GitHub downloads](https://img.shields.io/github/downloads/panda4556/maintainer-compass/total.svg?label=GitHub%20downloads)](https://github.com/panda4556/maintainer-compass/releases)
