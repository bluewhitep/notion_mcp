# Normal Skill Reference

## Purpose
Use this reference for standard skill work where the task is bigger than a quick lookup but does not require exhaustive edge-case handling.

This level covers:
- common skill routing;
- standard implementation and documentation workflows;
- expected validation;
- light troubleshooting.

## Skill Routing
1. Start from the task intent, not the file type alone.
2. Prefer the most specific skill that covers the requested work.
3. Combine skills only when responsibilities are genuinely split, such as source implementation plus formal documentation sync.
4. Follow repository-level instructions over global defaults when both apply.
5. Do not spawn subagents unless the user or environment explicitly requires that workflow.

## Reference Depth Selection
- Use `quick.md` for simple usage, reminders, and low-risk one-step work.
- Use `normal.md` for multi-step repository work, moderate ambiguity, or expected validation.
- Use `full.md` for template authoring, policy decisions, failure diagnosis, migration, or cross-agent compatibility.

## Standard Workflow
1. Inspect the relevant repository, docs, configs, or tool metadata before changing files.
2. Identify the active rules from global instructions, project instructions, and the selected skill.
3. Define the scope of files or behavior the task should affect.
4. Make small, reversible changes that match existing conventions.
5. Run focused validation that proves the affected behavior or documentation is correct.
6. Report commands run, files changed, verification results, and remaining risks.

## Documentation Work
For formal repository documentation:
- prefer existing docs structure before adding new locations;
- keep user-facing docs separate from developer-facing docs when the repository already uses that split;
- document complete command or API surfaces when the docs act as a contract;
- avoid example-only coverage when users asked for exhaustive operation coverage;
- update changelogs or task plans when the repository requires them.

## Source Work
For source implementation:
- inspect the current module boundaries before editing;
- use existing helper APIs and patterns;
- keep behavior changes scoped to the request;
- update tests and documentation when public behavior changes;
- avoid broad refactors unless they are required to complete the task safely.

## Light Troubleshooting
When results conflict:
- verify the current source of truth instead of relying on memory or old docs;
- compare tool output against docs and tests;
- check whether generated files, caches, or environment noise are misleading;
- narrow the failing scenario before applying a broad fix.

When a command fails:
- preserve the exact command and error summary;
- decide whether the failure is environmental, dependency-related, or caused by the change;
- retry only when the retry changes one meaningful condition.
