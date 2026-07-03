# CLI Tests

This document describes CLI test coverage and common verification commands.

## Coverage Goals

- Root commands: `init`, `pwd`, `version`, server lifecycle commands, and help text.
- Config commands: `config --global`, `config --local --show`, project-local reads, and token redaction.
- Project context: `.notion_mcp/` initialization, status reads, root resolution, and hidden compatibility entries.
- Page commands: attach, status, refresh, detach, retrieve, blocks, create, update, and hidden compatibility aliases.
- Block commands: append, insert-after, update, trash, and children reads.
- Database/DataSource commands: database container commands, data source table commands, shortcuts, and active data source defaulting.
- Raw API: registered operations remain callable and Raw API stays positioned as an advanced fallback.
- Output contract: prompts, HTTP error details, schema descriptions, and `--json` output remain stable.
- Boundary contract: CLI commands call Core services and do not directly import the Notion SDK.

## Common Commands

Focused CLI verification:

```bash
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/nilo_uv_cli_docs uv run pytest -q -p no:cacheprovider
```

Documentation inventory and user-doc boundary checks:

```bash
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/nilo_uv_docs uv run pytest -q -p no:cacheprovider
```

Isolated install acceptance:

```bash
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/nilo_uv_install uv run --no-project --with . nilo --help
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/nilo_uv_install uv run --no-project --with . nilo config --global --show --json
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/nilo_uv_install uv run --no-project --with . nilo server run --help
```

## Notes

- Real Notion workspace verification must be explicitly enabled and must use safe test pages or databases.
- When CLI behavior changes user-facing docs, update `Docs/EN/User/Cli.md`.
- When a command touches configuration, tokens, attachment state, or Notion permissions, update `Docs/EN/User/Configuration.md`.
