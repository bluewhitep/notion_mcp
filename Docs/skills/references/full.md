# Full Skill Reference

## Purpose
Use this reference as the complete manual for designing, adapting, maintaining, and troubleshooting skill templates across Codex, Claude, and other agent systems.

This level should be read when:
- creating a new skill template;
- adapting a skill to a new agent framework;
- resolving conflicts between global, project, and skill-level instructions;
- diagnosing repeated failures;
- planning work with public behavior, dependency, validation, or compatibility impact.

## Core Model
A skill is a reusable workflow contract. It should tell an agent:
- when the skill applies;
- when it does not apply;
- which facts to inspect first;
- what workflow to follow;
- which files, commands, APIs, or references are authoritative;
- what validation proves the work is complete;
- what risks or stop conditions require escalation.

Tool-specific `SKILL.md` files should be thin routing layers. Shared references should hold reusable policy and workflow detail.

## Three-Level Reference Pattern
Use three shared reference levels:

- Quick: scenario mapping and minimum safe actions.
- Normal: standard workflow, common validation, and light troubleshooting.
- Full: complete coverage, template adaptation, conflict resolution, and deeper troubleshooting.

The levels should be progressive. The quick reference must not repeat the full manual. The full reference may restate important rules when needed for standalone use.

## Template Structure
Recommended shared structure:
```text
skills/
  references/
    quick.md
    normal.md
    full.md
  <tool-name>/
    SKILL.md
```

For this layout, a tool-specific wrapper should resolve `../references/quick.md` from the directory that contains its own `SKILL.md`. That means the references are siblings of the wrapper directory, not nested under it. If an agent first checks `<skill>/references/` and it does not exist, it should retry the sibling `../references/` path before treating the reference as missing.

Recommended tool-specific `SKILL.md` sections:
- metadata or frontmatter required by the tool;
- purpose;
- when to use;
- when not to use;
- routing to quick, normal, and full references;
- tool-specific constraints;
- output or completion contract.

## Routing Rules
Use the narrowest reference depth that can safely complete the task.

Read `quick.md` when:
- the task is simple;
- the skill match is obvious;
- validation is trivial or already defined elsewhere.

Read `normal.md` when:
- the task spans multiple files or steps;
- the task needs validation;
- there are common edge cases;
- existing docs or behavior need consistency checks.

Read `full.md` when:
- the task creates or changes a skill template;
- the tool framework has its own required file format;
- global and project-level instructions conflict;
- public behavior, compatibility, dependencies, or validation policy changes;
- repeated failures need diagnosis.

## Instruction Precedence
When instructions overlap, apply them in this order:
1. System and platform safety rules.
2. Current runtime and tool permissions.
3. Project-level repository instructions.
4. User's explicit request.
5. Tool-specific `SKILL.md`.
6. Shared references.
7. Global personal defaults.

If a lower-priority instruction conflicts with a higher-priority instruction, follow the higher-priority instruction and note the conflict when it affects the outcome.

## Cross-Tool Adaptation
When adapting a skill to another tool:
- preserve the workflow intent;
- change only the wrapper format, metadata, or invocation mechanics required by that tool;
- keep shared references reusable;
- avoid copying large manual sections into the tool-specific wrapper;
- add tool-specific examples only when they cannot live in shared references.

## Server And CLI Surfaces
When one skill covers both server and CLI usage, split the guidance inside the references before creating multiple top-level skills.

Use separate reference sections for:
- server or MCP tool routes;
- manual server request fallback routes;
- CLI command routes;
- manual CLI fallback routes.

Create separate top-level skills only when:
- the trigger descriptions conflict;
- one surface has different safety rules;
- one surface needs different validation or setup;
- agents repeatedly choose the wrong route from a combined wrapper.

## Validation
A skill template change is complete when:
- each tool-specific entrypoint routes to the correct shared reference levels;
- shared references have distinct depth and do not contradict each other;
- paths and relative links are correct;
- the template states when to use and when not to use the skill;
- the template states how to validate or report completion;
- no repository-specific claims are included unless the skill is intentionally repository-specific.

## Troubleshooting
If a skill is too vague:
- add concrete triggers and non-triggers;
- define the first files, commands, docs, or APIs to inspect;
- add completion criteria.

If a skill duplicates too much content:
- move common behavior into shared references;
- keep the tool-specific file as a router;
- preserve only tool-required metadata and tool-specific constraints in the wrapper.

If a skill conflicts with repository rules:
- make the repository rules authoritative for that repository;
- update the skill to say which local rules must be inspected;
- avoid encoding stale project assumptions in a generic template.

If users keep asking the same clarification:
- add a routing rule or stop condition;
- add a short decision table only when it prevents repeated ambiguity;
- keep examples minimal and aligned with current tool behavior.

If an actual-agent regression is required:
- do not use unit tests alone as proof that the agent followed the skill;
- run the real agent surface, such as a child `codex exec` session when testing Codex;
- capture both the agent's route report and an external operation log;
- for safe fake MCP tools in noninteractive agents, configure approval as `approve` rather than `prompt`, otherwise the tool call can be cancelled before route behavior is tested.
