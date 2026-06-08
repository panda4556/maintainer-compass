# Packaging

Maintainer Compass is packaged as a standard Python project with `setuptools`.
It has no runtime dependencies.

## Local Build

```bash
python -m pip install --upgrade build
python -m build
```

The build creates a source distribution and wheel under `dist/`.

## Release Flow

1. Update `CHANGELOG.md`.
2. Update the version in `pyproject.toml` and `src/maintainer_compass/__init__.py`.
3. Run tests and the repository audit.
4. Push a tag such as `v0.4.0`.
5. GitHub Actions builds package artifacts and attaches them to the release.

## Typing

The package includes `py.typed` so type checkers can treat exported type
annotations as intentional public package metadata.

