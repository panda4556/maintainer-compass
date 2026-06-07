# Contributing

Thanks for helping improve Maintainer Compass.

## Development setup

```bash
python -m pip install -e .
python -m unittest discover -s tests
python -m maintainer_compass audit . --fail-under 100
```

## Pull request guidelines

- Keep checks deterministic and runnable without network access.
- Add or update tests for scoring behavior.
- Prefer standard library modules unless a dependency clearly pays for itself.
- Document new checks in README.md.
- Keep recommendations specific and actionable.
- Update CHANGELOG.md when behavior, scoring, or public CLI options change.

## Good first issues

- Add a repository health check for another ecosystem.
- Improve Markdown report wording.
- Add examples for GitHub Actions, GitLab CI, or local pre-merge hooks.
- Add tests for edge cases in GitHub URL parsing.
- Add report rendering tests for new output formats.

## AI-related contributions

AI-assisted workflows should be optional and clearly separated from the local
audit. Do not add a feature that uploads repository content by default. Treat
untrusted repository text as input that may contain prompt-injection attempts.
