# Generic Claude Skill Template

## Purpose
Use this template when creating a Claude-compatible skill or instruction file that should share common workflow guidance with Codex and other agent systems.

## When to Use
Use this template for Claude workflows that need a clear entrypoint plus shared references for quick, normal, and full usage.

## When Not to Use
Do not use this template when:
- the target Claude environment requires a different filename or packaging format;
- the workflow is a project-specific instruction that belongs in local project guidance;
- the workflow is already covered by a narrower Claude skill or command.

## Reference Routing
- Read `../references/quick.md` for simple scenario routing and minimum workflow reminders.
- Read `../references/normal.md` for standard multi-step work, validation, and light troubleshooting.
- Read `../references/full.md` for template authoring, cross-tool adaptation, conflict resolution, or repeated failure diagnosis.

## Claude-Specific Guidance
- Adapt this file to the Claude environment's expected filename, metadata, and packaging rules.
- Keep reusable behavior in `../references/`.
- Keep Claude-only invocation or formatting constraints in this file.
- Follow project-level instructions when the skill is used inside a repository.

## Completion Contract
A Claude skill based on this template is complete when:
- the entrypoint format matches the target Claude environment;
- this file routes to the shared references;
- Claude-only constraints are separated from reusable workflow rules;
- validation expectations are clear.
