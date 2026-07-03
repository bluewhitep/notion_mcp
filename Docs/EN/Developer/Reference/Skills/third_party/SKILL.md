# Generic Third-Party Skill Template

## Purpose
Use this template when adapting the shared skill reference pattern to another agent, automation tool, or standards system.

## When to Use
Use this template for tools that need their own skill entrypoint but can reuse the shared quick, normal, and full reference manuals.

## When Not to Use
Do not use this template when:
- the tool cannot load local reference files;
- the target format requires a generated artifact rather than a Markdown template;
- the workflow is specific enough to deserve its own named tool directory.

## Reference Routing
- Read `../references/quick.md` for simple scenario routing and minimum workflow reminders.
- Read `../references/normal.md` for standard workflows, validation expectations, and light troubleshooting.
- Read `../references/full.md` for tool adaptation, complete usage coverage, and deeper troubleshooting.

## Adaptation Checklist
- Rename or wrap this file according to the target tool's required entrypoint.
- Preserve the three-level reference routing.
- Keep shared workflow rules in `../references/`.
- Keep only tool-specific metadata, invocation rules, and limitations in this file.
- Confirm relative links still work after moving or packaging the template.

## Completion Contract
A third-party skill based on this template is complete when:
- the target tool can identify the skill entrypoint;
- the entrypoint routes to quick, normal, and full references;
- tool-specific constraints are explicit;
- reusable guidance remains shared rather than duplicated.
