# MCP 测试文档

本文档面向开发者，记录 Stage 4 MCP server 和 MCP tools 的测试目标与验证命令。

## 测试文件

- `tests/v2/mcp_server/test_server_lifecycle.py`
  - 验证 `create_mcp_server()` 返回 `FastMCP`，server 名称为 `notion-mcp`，并能列出 tools。
  - 验证支持 `stdio` 和 `streamable-http`。
- `tests/v2/mcp_server/test_tool_inventory.py`
  - 验证工具清单覆盖 config、auth、pages、blocks、databases、data_sources、users、comments、views、file_uploads、search、custom_emojis、raw_api。
  - 验证每个 tool 有 description 和 input schema。
- `tests/v2/mcp_server/test_tool_calls.py`
  - 验证 MCP tool 调用 Core service mock，不调用 CLI。
  - 验证 `config_status` 返回结构化状态。
- `tests/v2/mcp_server/test_dangerous_tools.py`
  - 验证 `page_trash`、`block_trash` 有 `destructiveHint`。
  - 验证缺少 `confirm=true` 时返回 `confirmation_required`。
- `tests/v2/scenarios/test_mcp_client_flow.py`
  - 验证 MCP client 风格的 list tools 和 call tool 流程。
- `tests/v2/mcp_server/test_stage5_tool_coverage.py`
  - 验证 Stage 5 扩展工具清单、分页参数透传和 raw API 扩展登记表。

## 验证命令

Stage 4 focused tests：

```bash
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uvcache_stage4 uv run --no-project --with pytest --with pytest-asyncio --with mcp --with 'pydantic>=2.0' --with typer --with notion-client pytest -q -p no:cacheprovider tests/v2/mcp_server tests/v2/scenarios/test_mcp_client_flow.py
```

当前结果：

```text
10 passed
```

全量当前测试：

```bash
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_full_stage4 uv run --no-project --with fastapi --with 'uvicorn[standard]' --with typer --with 'pydantic>=2.0' --with notion-client --with mcp --with pytest --with pytest-asyncio --with httpx pytest -q -p no:cacheprovider
```

当前结果：

```text
65 passed, 1 warning
```

隔离安装 MCP 枚举验收：

```bash
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_stage4_mcp_import3 uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project python -c 'import asyncio; from notion_mcp.mcp_server.server import create_mcp_server; tools = asyncio.run(create_mcp_server().list_tools()); print(len(tools)); print(any(t.name == "config_status" for t in tools))'
```

当前结果：

```text
35
True
```

## 备注

`FastMCP.call_tool()` 在当前 SDK 版本中可能返回 `(content, structured)`。`NotionFastMCP` 会标准化为 content list，方便测试和本地调用保持一致。
