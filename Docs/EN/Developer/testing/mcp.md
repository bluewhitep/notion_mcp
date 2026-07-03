# MCP Tests

This document describes MCP server and MCP tool test coverage.

## Coverage Goals

- Server lifecycle: the server can be created, started, and exposes the expected server name.
- Tool inventory: tools cover config, auth, pages, blocks, databases, data sources, users, comments, views, file uploads, search, custom emojis, and Raw API.
- Tool schema: each tool has a description, input schema, and structured output.
- Tool calls: MCP tools call Core services, do not call CLI, and do not create Notion SDK clients directly.
- Dangerous tools: trash/delete-style tools carry warnings and enforce confirmation guards.
- Client flow: list-tools and call-tool flows match MCP client expectations.

## Common Commands

MCP-focused verification:

```bash
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/nilo_uv_mcp uv run pytest -q -p no:cacheprovider
```

Isolated install MCP help check:

```bash
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/nilo_uv_mcp_install uv run --no-project --with . nilo server run --help
```

## Notes

- MCP tools and CLI share Core, not command strings.
- Raw API is an advanced fallback and should not become the default page/database workflow.
- Real Notion live verification requires explicit token and safe test resources.
- The MCP HTTP server live regression is `tests/live/test_live_mcp_server_http_e2e.py`. It verifies JSON-RPC tool calls over the server path, not CLI command behavior.
