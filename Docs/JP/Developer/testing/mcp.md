# MCP Tests

この文書は MCP server と MCP tool test coverage を説明します。

## Coverage goals

- Server lifecycle: server を作成・起動でき、期待する server name を expose します。
- Tool inventory: config、auth、pages、blocks、databases、data sources、users、comments、views、file uploads、search、custom emojis、Raw API を cover します。
- Tool schema: 各 tool が description、input schema、structured output を持ちます。
- Tool calls: MCP tools は Core services を呼び、CLI を呼ばず、Notion SDK clients を直接作成しません。
- Dangerous tools: trash/delete 系 tools は warnings と confirmation guards を持ちます。
- Client flow: list-tools と call-tool flows が MCP client expectations に合います。

## Common commands

MCP-focused verification:

```bash
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/nilo_uv_mcp uv run pytest -q -p no:cacheprovider
```

Isolated install MCP help check:

```bash
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/nilo_uv_mcp_install uv run --no-project --with . nilo server run --help
```

## Notes

- MCP tools と CLI は Core を共有します。command strings は共有しません。
- Raw API は advanced fallback であり、default page/database workflow にしてはいけません。
- Real Notion live verification には explicit token と safe test resources が必要です。
- MCP HTTP server live regression は `tests/live/test_live_mcp_server_http_e2e.py` です。server 経由の JSON-RPC tool calls を検証し、CLI command behavior は検証しません。
