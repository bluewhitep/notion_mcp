# Live Tests

This document records how real Notion tests are gated and what safety rules apply.

## Default Behavior

Live tests are skipped by default and do not access Notion during normal test runs.

Current live tests:

- `tests/live/test_live_auth_validate.py`
  - Skip reason: requires a real token.
  - Enable with: `NOTION_MCP_LIVE=1` and `NOTION_MCP_TOKEN`.
  - Optional: `NOTION_MCP_USER_ID` for checking token identity.
- `tests/live/test_live_content_consistency_e2e.py`
  - Skip reason: creates, modifies, and trashes temporary objects in a real Notion test page/data source.
  - Enable with: `NOTION_MCP_LIVE_E2E=1`.
  - Optional: `NOTION_MCP_LIVE_PARENT_PAGE_ID` and `NOTION_MCP_LIVE_DATA_SOURCE_ID`.
  - If optional IDs are absent, the test tries to read page/database attachments from the current project `.notion_mcp` context.
  - Flow: create -> read/compare -> update -> read/compare -> trash -> verify.
- `tests/live/test_live_mcp_server_http_e2e.py`
  - Skip reason: starts the local MCP HTTP server and creates, modifies, searches, and trashes temporary objects in a real Notion test page/data source.
  - Enable with: `NOTION_MCP_LIVE_SERVER_E2E=1`.
  - Optional: `NOTION_MCP_LIVE_PARENT_PAGE_ID` and `NOTION_MCP_LIVE_DATA_SOURCE_ID`.
  - If optional IDs are absent, the test tries to read page/database attachments from the current project `.notion_mcp` context.
  - Flow: server start -> JSON-RPC initialize -> tools/list -> create page/block/database entry -> read/compare -> search -> update -> read/compare -> trash -> verify -> server stop/remove.
  - This test validates MCP HTTP tool calls only. It does not call CLI page/database/block commands.

## Enable Live Tests

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

## Safety Requirements

- Live tests must not modify production data.
- Write-operation live tests may use only dedicated test workspaces, pages, or data sources.
- Missing tokens, permissions, paid-plan features, or test workspaces must lead to skips, not fake passes.
