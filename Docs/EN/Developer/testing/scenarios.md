# Scenario Tests

This document describes offline scenario tests and the fake Notion client.

## Fake Notion Client

The fake Notion client verifies CLI/MCP/Core call chains without accessing a real Notion workspace.

Main uses:

- Simulate `users.me()`.
- Simulate page retrieve/create/update, block children/append/update/trash, and database/data source queries.
- Record call sequences to verify that CLI and MCP tools reach the fake client through Core services.
- Verify that dry-run paths do not call real write branches.

## Scenario Coverage

- Global configuration flow: set token, show status, validate auth.
- CLI -> Core -> fake Notion: human CLI commands go through Core services.
- MCP -> Core -> fake Notion: MCP tool calls go through Core services.
- Install and help: isolated root help, resource help, and MCP server help.
- Project context: `.notion_mcp/` initialization, project-root discovery from subdirectories, and page/database attachment defaulting.
- Page content editing: page content, insert-after, append, update, and remove workflow coverage.
- Database/DataSource: database attachment, active data source defaulting, query, page create/update, and property rename.
- Live content consistency: after explicit opt-in, real Notion page, block, and data source entry create/read/compare/update/read/compare/trash/verify.

## Common Commands

Scenario tests can run with the full local suite:

```bash
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/nilo_uv_scenarios uv run pytest -q -p no:cacheprovider
```

## Notes

- Scenario tests use the fake client by default and do not need a real token.
- Real Notion workspace scenarios must use live/integration markers and be skipped by default.
- Strict content consistency live E2E is in `tests/live/test_live_content_consistency_e2e.py`. Before running it, confirm the target is a dedicated test page/data source and enable it explicitly:

```bash
env \
  PYTHONDONTWRITEBYTECODE=1 \
  UV_CACHE_DIR=/private/tmp/nilo_uv_live_e2e \
  NOTION_MCP_LIVE_E2E=1 \
  NOTION_MCP_LIVE_PARENT_PAGE_ID=<test_page_id> \
  NOTION_MCP_LIVE_DATA_SOURCE_ID=<test_data_source_id> \
  uv run pytest -q -p no:cacheprovider tests/live/test_live_content_consistency_e2e.py
```
