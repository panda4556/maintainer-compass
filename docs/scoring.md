# Scoring Model

Maintainer Compass uses weighted checks across four categories. The score is a
maintenance readiness signal, not a judgment of project quality.

## Onboarding

Onboarding checks measure whether new users and contributors can understand the
project without private context.

- README
- License
- Contribution guide
- Documentation
- Examples
- Roadmap

## Governance

Governance checks measure whether collaboration expectations and support paths
are visible.

- Code of conduct
- Security policy
- Support policy
- Maintainer guide
- Issue templates
- Pull request template

## Automation

Automation checks measure whether maintainers have basic guardrails around
review and dependency work.

- Continuous integration
- Dependency automation
- Tests
- Git ignore rules

## Release Readiness

Release readiness checks measure whether users can install, upgrade, and audit
changes.

- Package metadata
- Changelog
- Release workflow

## Design Notes

- Empty signal directories do not pass checks.
- The local audit avoids network access by default.
- Recommendations should be specific enough to become an issue or pull request.
- New checks should include tests for positive and negative cases.
- SARIF output reports failed checks as warnings so maintainers can track them
  in GitHub Code Scanning without treating every gap as a security bug.
