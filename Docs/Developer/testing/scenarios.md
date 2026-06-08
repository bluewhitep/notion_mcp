# 场景测试文档

本文档面向开发者，记录离线场景测试和 fake Notion client 的使用方式。

## Fake Notion Client

测试 fixture：

- `tests/v2/fixtures/fake_notion.py`

用途：

- 模拟 `users.me()`。
- 模拟 `pages.create/retrieve/update`。
- 记录调用序列，验证 CLI/MCP 是否通过 Core service 到达 fake client。

## 场景测试

- `tests/v2/scenarios/test_full_local_config_flow.py`
  - 覆盖 `init`、`status --json`、`auth validate --json`。
- `tests/v2/scenarios/test_cli_to_core_to_fake_notion.py`
  - 覆盖 CLI `page create` -> Core `PagesService` -> fake Notion client。
- `tests/v2/scenarios/test_mcp_to_core_to_fake_notion.py`
  - 覆盖 MCP `page_create` -> Core `PagesService` -> fake Notion client。
- `tests/v2/scenarios/test_install_and_run.py`
  - 覆盖隔离安装后的 `notion-mcp --help` 和 `notion-mcp mcp serve --help`。

## 验证命令

```bash
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uvcache_stage6 uv run --no-project --with pytest --with pytest-asyncio --with mcp --with typer --with 'pydantic>=2.0' --with notion-client pytest -q -p no:cacheprovider tests/v2/scenarios/test_full_local_config_flow.py tests/v2/scenarios/test_cli_to_core_to_fake_notion.py tests/v2/scenarios/test_mcp_to_core_to_fake_notion.py tests/v2/scenarios/test_install_and_run.py
```

当前结果：

```text
4 passed
```
