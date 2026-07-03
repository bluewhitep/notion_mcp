---
name: generic-codex-skill-template
description: Template for Codex skills that route to shared quick, normal, and full references.
---

# Generic Codex Skill Template

## Purpose
Use this template when creating a Codex skill that should share common workflow guidance with Claude and other agent systems.

## When to Use
Use this template for Codex workflows that need reusable routing, validation, and troubleshooting guidance without duplicating the full manual in every skill.

## When Not to Use
Do not use this template when:
- the skill is only a one-off repository note;
- the tool requires a different entrypoint format and cannot read `SKILL.md`;
- the workflow is already fully covered by a more specific Codex skill.

## Reference Routing
- Resolve reference paths from this `SKILL.md` file's directory. In the recommended layout, `../references/` is a sibling directory shared by multiple tool wrappers; do not assume `references/` is nested inside the skill directory.
- Read `../references/quick.md` for simple scenario routing and minimum workflow reminders.
- Read `../references/normal.md` for common multi-step work, documentation sync, source-work coordination, or light troubleshooting.
- Read `../references/full.md` for creating or adapting skill templates, resolving instruction conflicts, or diagnosing repeated failures.

## Codex-Specific Guidance
- Keep required Codex frontmatter at the top of this file.
- Keep this file small and focused on routing.
- Put reusable guidance in `../references/`.
- Follow project-level `AGENTS.md` when working inside a repository.
- Use tool calls and validation commands that match the active Codex permissions.

## Completion Contract
A Codex skill based on this template is complete when:
- the frontmatter describes the skill's actual trigger scope;
- this file routes to the correct shared reference levels;
- any Codex-only constraints are listed here;
- reusable guidance is not duplicated from the shared references.
