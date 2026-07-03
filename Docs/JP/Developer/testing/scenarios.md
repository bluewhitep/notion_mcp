# Scenario Tests

この文書は offline scenario tests と fake Notion client を説明します。

## Fake Notion client

Fake Notion client は real Notion workspace にアクセスせず、CLI/MCP/Core call chain を検証します。

主な用途:

- `users.me()` の simulate。
- page retrieve/create/update、block children/append/update/trash、database/data source queries の simulate。
- CLI と MCP tools が Core services 経由で fake client に到達するか検証します。
- dry-run path が real write branch を呼ばないことを検証します。

## Scenario coverage

- Global configuration flow: token set、status show、auth validate。
- CLI -> Core -> fake Notion。
- MCP -> Core -> fake Notion。
- Install and help: isolated root help、resource help、MCP server help。
- Project context: `.notion_mcp/` initialization、subdirectory からの project-root discovery、page/database attachment defaulting。
- Page content editing: page content、insert-after、append、update、remove workflow。
- Database/DataSource: database attachment、active data source defaulting、query、page create/update、property rename。
- Live content consistency: explicit opt-in 後に real Notion page/block/data source entry の create/read/compare/update/read/compare/trash/verify を実行します。

## Common commands

Scenario tests は full local suite と一緒に実行できます。

```bash
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/nilo_uv_scenarios uv run pytest -q -p no:cacheprovider
```

## Notes

- Scenario tests は default で fake client を使い、real token は不要です。
- Real Notion workspace scenarios は live/integration markers を使い、default skip にします。
- Strict content consistency live E2E は `tests/live/test_live_content_consistency_e2e.py` にあります。実行前に dedicated test page/data source を確認し、明示的に有効化してください。
