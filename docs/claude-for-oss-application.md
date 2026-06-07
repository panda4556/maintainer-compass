# Claude for OSS Application Notes

These notes are for applying to Claude for OSS with the public repository:

```text
https://github.com/panda4556/maintainer-compass
```

Use honest, current project metrics. Do not claim stars, downloads, users, or
production adoption that the repository does not currently have.

## Current Public Metrics

Checked on 2026-06-07:

- GitHub stars: 1
- Forks: 0
- Open Dependabot pull requests: 3
- Recent maintenance activity: active commits and CI updates on 2026-06-07

This repository does not currently meet a large-project threshold such as 5,000
GitHub stars or 1M monthly npm downloads. Apply through the maintainer impact
angle: the project is an OSS maintenance tool that helps many small projects
improve contribution readiness, security reporting, CI hygiene, and release
processes.

## Maintainer Role

Primary maintainer.

## Short Project Description

```text
Maintainer Compass is a zero-dependency CLI that audits open-source repositories for maintenance readiness. It checks onboarding files, governance docs, issue and pull request workflows, CI, tests, release readiness, and maintainer support signals, then produces Markdown or JSON reports for humans and automation.
```

## Why This Project Matters

```text
Small open-source maintainers often know they need better onboarding, triage, CI, security reporting, and release hygiene, but they do not have a repeatable way to measure what is missing. Maintainer Compass turns that work into a local, deterministic audit that contributors can run before opening a pull request and maintainers can run in CI. The project helps reduce review back-and-forth, makes maintenance gaps visible, and gives contributors concrete next steps.
```

## Why Claude for OSS Would Help

```text
Claude would help turn repository health results into maintainer-ready work: drafting issue descriptions from failed checks, summarizing triage patterns, generating release notes, reviewing documentation for clarity, and designing safer optional automations around untrusted repository content. The core scanner will stay local and dependency-free, while Claude can support opt-in workflows that reduce repetitive maintainer labor.
```

## Short Application Answer

```text
I maintain Maintainer Compass, a zero-dependency CLI that helps open-source maintainers audit repository readiness: onboarding, governance, support, issue/PR workflows, CI, tests, roadmap, and release hygiene. Claude for OSS would help convert audit results into clearer issues, release notes, documentation improvements, and safer opt-in maintainer automations while keeping the core scanner local and deterministic.
```

## Chinese Draft

```text
Maintainer Compass 是一个零运行时依赖的开源维护健康度检查工具。它帮助维护者扫描 README、许可证、贡献指南、安全策略、Issue/PR 模板、CI、测试、文档、路线图和发布准备情况，并生成 Markdown 或 JSON 报告。Claude for OSS 可以帮助项目把检查结果转化成 issue 草稿、发布说明、贡献者清单和维护者决策摘要，让小型开源项目更容易持续维护。
```

## Responsible AI Boundary

- The default audit must remain deterministic and work without network access.
- AI-assisted features should be opt-in.
- Reports should avoid uploading repository contents unless the user explicitly
  chooses an AI workflow.
- Prompt-injection and untrusted repository text should be treated as security
  risks in future automation.

## Application Strengthening Checklist

- Keep the repository public.
- Keep CI passing on supported Python versions.
- Add tagged releases when user-facing functionality changes.
- Keep `README.md`, `CONTRIBUTING.md`, `SUPPORT.md`, `MAINTAINERS.md`,
  `ROADMAP.md`, and `CHANGELOG.md` current.
- Open issues for roadmap items so contributors can see real work.
- Use honest metrics and explain ecosystem impact instead of overstating
  downloads or stars.
