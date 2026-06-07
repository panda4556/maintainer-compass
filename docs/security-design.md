# Security Design Notes

Maintainer Compass inspects repository structure and selected metadata. It
should remain conservative because repositories can contain untrusted content.

## Current Boundaries

- The default audit does not require network access.
- The scanner checks file and directory presence instead of parsing arbitrary
  repository content.
- GitHub metadata fetching is optional and limited to the public repository API.
- Reports render fixed check metadata and paths from the local audit.
- SARIF output reports failed maintenance checks as warnings and does not parse
  repository file contents.

## Risks to Watch

- Path handling bugs when scanning unusual repository layouts.
- Overly broad recursive scans on large repositories.
- Future workflow parsing that treats untrusted YAML as instructions.
- Future AI features that expose repository text to prompts without user
  consent.
- Report rendering that could accidentally include sensitive local paths or
  repository content.
- Code scanning uploads that expose local report paths. Prefer running SARIF in
  CI from the repository root.

## Future Requirements

- Keep AI workflows opt-in.
- Keep deterministic local behavior available without API keys.
- Add tests for path traversal-like layouts before expanding file reads.
- Clearly document what data an optional network or AI workflow sends.
- Review new automation against supply-chain and prompt-injection risks.
