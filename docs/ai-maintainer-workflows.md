# AI-Assisted Maintainer Workflows

Maintainer Compass is intentionally useful without AI. Future AI features should
reduce repetitive maintainer work while keeping the deterministic audit local
and easy to trust.

## Good Fit

- Summarize failed checks into contributor-friendly issue drafts.
- Draft pull request review checklists from audit results.
- Generate release note outlines from changelog updates.
- Rewrite recommendations for different contributor experience levels.
- Help maintainers compare score history and prioritize work.

## Boundaries

- AI features should be opt-in.
- Repository content should not be uploaded without an explicit user action.
- Prompt-injection risks from untrusted repository text should be documented and
  tested before any automated agent workflow is added.
- Maintainers should remain responsible for publishing issues, labels, release
  notes, and security guidance.

## Claude for OSS Fit

Claude for OSS would help explore these workflows safely: turning audit findings
into clear next actions, improving documentation quality, and reviewing future
agentic features before they touch untrusted repository content.

