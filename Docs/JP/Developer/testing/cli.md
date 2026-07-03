# CLI Tests

この文書は CLI test coverage とよく使う verification commands を説明します。

## Coverage goals

- Root commands: `init`、`pwd`、`version`、server lifecycle commands、help text。
- Config commands: `config --global`、`config --local --show`、project-local reads、token redaction。
- Project context: `.notion_mcp/` initialization、status reads、root resolution、hidden compatibility entries。
- Page commands: attach、status、refresh、detach、retrieve、blocks、create、update、hidden compatibility aliases。
- Block commands: append、insert-after、update、trash、children reads。
- Database/DataSource commands: database container commands、data source table commands、shortcuts、active data source defaulting。
- Raw API: registered operations が呼び出せること、Raw API が advanced fallback として位置付けられていること。
- Output contract: prompts、HTTP error details、schema descriptions、`--json` output の安定性。
- Boundary contract: CLI commands は Core services を呼び、Notion SDK を直接 import しません。

## Common commands

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

- Real Notion workspace verification は明示的に有効化し、安全な test pages/databases を使います。
- CLI behavior が user-facing docs に影響する場合は `Docs/JP/User/Cli.md` も同期します。
- Configuration、tokens、attachment state、Notion permissions に関わる command は `Docs/JP/User/Configuration.md` も更新します。
