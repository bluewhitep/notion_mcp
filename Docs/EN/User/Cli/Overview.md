# CLI Overview

This page summarizes global CLI behavior.

## Common Rules

- `-h` and `--help` are equivalent, for example `nilo -h` and `nilo page -h`.
- Most read commands support `--json` for scripts and agents.
- Commands with side effects, such as write, update, send, complete, and trash commands, should be previewed with `--dry-run` when available.
- JSON input is passed through `--payload`, `--properties`, or `--arguments`. The value must be a JSON object.
- Plural forms such as `page/pages`, `block/blocks`, and `database/databases` are aliases. User documentation uses the singular form by default.
- Before real Notion calls, set a global token with `nilo config --global user.token <token>` and share the target content with the Notion connection.

## JSON Input Examples

```bash
nilo page update <page_id> --payload '{"properties": {}}'
nilo database query --payload '{"page_size": 10}'
nilo raw-api invoke search --arguments '{"query": "Tasks"}' --json
```

## Preview Side Effects

```bash
nilo block append <block_id> --payload '{"children": []}' --dry-run --json
nilo block trash <block_id> --dry-run
```
