# Live Tests

この文書は real Notion tests の gate と safety rules を記録します。

## Default behavior

Live tests は default skip であり、通常の test runs では Notion にアクセスしません。

Current live tests:

- `tests/live/test_live_auth_validate.py`
  - Skip reason: real token が必要。
  - Enable with: `NOTION_MCP_LIVE=1` and `NOTION_MCP_TOKEN`。
  - Optional: token identity 確認用の `NOTION_MCP_USER_ID`。
- `tests/live/test_live_content_consistency_e2e.py`
  - Skip reason: real Notion test page/data source に temporary objects を create/modify/trash します。
  - Enable with: `NOTION_MCP_LIVE_E2E=1`。
  - Optional: `NOTION_MCP_LIVE_PARENT_PAGE_ID` and `NOTION_MCP_LIVE_DATA_SOURCE_ID`。
  - Optional IDs がない場合、current project `.notion_mcp` context の page/database attachments を読み取ろうとします。
  - Flow: create -> read/compare -> update -> read/compare -> trash -> verify。
- `tests/live/test_live_mcp_server_http_e2e.py`
  - Skip reason: local MCP HTTP server を起動し、real Notion test page/data source に temporary objects を create/modify/search/trash します。
  - Enable with: `NOTION_MCP_LIVE_SERVER_E2E=1`。
  - Optional: `NOTION_MCP_LIVE_PARENT_PAGE_ID` and `NOTION_MCP_LIVE_DATA_SOURCE_ID`。
  - Flow: server start -> JSON-RPC initialize -> tools/list -> create page/block/database entry -> read/compare -> search -> update -> read/compare -> trash -> verify -> server stop/remove。

## Enable live tests

```bash
NOTION_MCP_LIVE=1 \
NOTION_MCP_TOKEN=ntn_xxx \
NOTION_MCP_USER_ID=01234567-89ab-cdef-0123-456789abcdef \
uv run pytest -q tests/live
```

Strict content consistency E2E:

```bash
NOTION_MCP_LIVE_E2E=1 \
NOTION_MCP_LIVE_PARENT_PAGE_ID=<test_page_id> \
NOTION_MCP_LIVE_DATA_SOURCE_ID=<test_data_source_id> \
uv run pytest -q tests/live/test_live_content_consistency_e2e.py
```

MCP HTTP server live regression:

```bash
NOTION_MCP_LIVE_SERVER_E2E=1 \
NOTION_MCP_LIVE_PARENT_PAGE_ID=<test_page_id> \
NOTION_MCP_LIVE_DATA_SOURCE_ID=<test_data_source_id> \
uv run pytest -q tests/live/test_live_mcp_server_http_e2e.py
```

## Safety requirements

- Live tests must not modify production data.
- Write-operation live tests may use only dedicated test workspaces, pages, or data sources.
- Missing tokens, permissions, paid-plan features, or test workspaces must lead to skips, not fake passes.
