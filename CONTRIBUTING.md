# Contributing

Thanks for helping improve Maintainer Compass.

## Development setup

```bash
python -m pip install -e .
python -m unittest discover -s tests
```

## Pull request guidelines

- Keep checks deterministic and runnable without network access.
- Add or update tests for scoring behavior.
- Prefer standard library modules unless a dependency clearly pays for itself.
- Document new checks in README.md.
- Keep recommendations specific and actionable.

## Good first issues

- Add a repository health check for another ecosystem.
- Improve Markdown report wording.
- Add examples for GitHub Actions, GitLab CI, or local pre-merge hooks.
- Add tests for edge cases in GitHub URL parsing.

