# Roadmap

Maintainer Compass focuses on practical, low-maintenance checks that help small
open-source projects become easier to contribute to and safer to maintain.

## Near Term

- Add more report rendering tests for Markdown and JSON output.
- Improve SARIF grouping and baseline support for GitHub Code Scanning.
- Add a release checklist generator from failed audit checks.
- Improve GitHub metadata summaries without making network access required.
- Add example repositories that demonstrate high, medium, and low scores.

## Medium Term

- Add optional issue triage helpers that summarize audit failures into GitHub
  issue drafts.
- Add ecosystem-specific checks for Python packaging, Node.js package metadata,
  Rust crates, Go modules, and Java build files.
- Track score history over time for maintainers who run the tool in CI.
- Provide suggested labels and milestones from audit categories.

## AI-Assisted Maintainer Work

Future AI features should be opt-in and clearly separated from the deterministic
local audit. Candidate workflows include:

- Summarizing new issues into maintainer action items.
- Drafting pull request review checklists from changed audit categories.
- Turning failed checks into contributor-friendly issue templates.
- Preparing release notes from changelog entries and merged pull requests.

The core scanner should remain useful without API keys, network access, or paid
services.
