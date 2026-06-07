# Maintainers

Maintainer Compass is currently maintained by `panda4556`.

## Operating Principles

- Keep the core audit deterministic and runnable without network access.
- Prefer standard library APIs unless a dependency clearly improves reliability.
- Treat every check as a maintainer workload signal, not a vanity metric.
- Keep recommendations specific enough that a contributor can act on them.
- Add tests for scoring behavior, CLI exit codes, and report rendering changes.

## Triage Workflow

1. Confirm whether the issue is a bug, feature request, documentation gap, or
   application/support note.
2. Ask for a minimal repository layout when a scoring result is surprising.
3. Prefer small checks that can be explained in one sentence.
4. Close requests that require network access for the default local audit unless
   they are explicitly optional.

## Review Checklist

- Does the change preserve zero runtime dependencies?
- Does it keep local audits deterministic?
- Does it avoid reading more repository content than needed?
- Are new checks documented in `README.md`?
- Are tests included for pass and fail cases?

## Release Checklist

1. Run `python -m unittest discover -s tests`.
2. Run `python -m maintainer_compass audit . --fail-under 100`.
3. Update `CHANGELOG.md`.
4. Tag the release with `vX.Y.Z`.
5. Publish release notes that describe user-visible changes.

