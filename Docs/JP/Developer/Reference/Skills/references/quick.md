# Quick Skill Reference

## Purpose
Use this reference when you need the fastest path from a work scenario to the right skill behavior.

This level only answers:
- when to use a skill;
- which reference depth to read;
- what the minimum safe workflow is.

## Scenario Routing
- Use a skill when a task clearly matches a reusable workflow, such as source writing, documentation maintenance, project setup, remote operations, or tool-specific procedures.
- Use the tool-specific `SKILL.md` first when the agent framework requires a particular entrypoint.
- Use this quick reference for simple, familiar tasks with low ambiguity.
- Escalate to `normal.md` when the task has multiple steps, unclear scope, or needs validation guidance.
- Escalate to `full.md` when the task has edge cases, failures, custom template work, or cross-tool adaptation.

## Minimum Workflow
1. Identify the task type and whether a skill applies.
2. Read the tool-specific `SKILL.md` entrypoint.
3. Follow the routing rule in that file.
4. Read only the reference depth required for the task.
5. Execute the task using the repository or tool's own rules as the source of truth.

## Stop Conditions
Stop and read `normal.md` or `full.md` when:
- the task changes public behavior, dependencies, structure, or compatibility;
- the correct skill or reference level is ambiguous;
- existing documentation, code, or tool output conflicts;
- the operation is destructive, broad, remote, or hard to reverse;
- validation expectations are not obvious.
