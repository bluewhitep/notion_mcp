# CLI 测试文档

本文档面向开发者，记录 Stage 3 CLI 测试目标和验证命令。

## 测试文件

- `tests/v2/cli/test_init.py`
  - 验证 `notion-mcp init` 非交互模式、Core 配置写入、token 脱敏、用户 UUID 校验和文件权限。
- `tests/v2/cli/test_config_commands.py`
  - 验证 `config get/set/unset/list` 和 token 默认脱敏。
- `tests/v2/cli/test_status.py`
  - 验证普通状态输出和 `--json` 稳定结构。
- `tests/v2/cli/test_resource_commands.py`
  - 验证 page、block、database 命令通过 Core service mock 调用。
  - 验证 CLI 命令模块不导入 Notion SDK。
- `tests/v2/cli/test_dry_run.py`
  - 验证 page create dry-run 不调用写操作。
  - 验证 `notion-mcp mcp serve --help` 可用。
- `tests/v2/cli/test_stage8_extended_resource_commands.py`
  - 验证 data-source、user、comment、view、file-upload、search、custom-emoji、raw-api 命令组注册。
  - 验证新增资源命令通过 Core service mock 调用。
  - 验证扩展 CLI 命令模块不导入 Notion SDK。

## 验证命令

Stage 3 focused tests：

```bash
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uvcache_stage3 uv run --no-project --with pytest --with typer --with 'pydantic>=2.0' --with notion-client pytest -q -p no:cacheprovider tests/v2/cli
```

当前结果：

```text
23 passed
```

全量当前测试：

```bash
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_full_stage3 uv run --no-project --with fastapi --with 'uvicorn[standard]' --with typer --with 'pydantic>=2.0' --with notion-client --with pytest --with pytest-asyncio --with httpx pytest -q -p no:cacheprovider
```

当前结果：

```text
55 passed, 1 warning
```

隔离安装验收：

```bash
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_stage3_help uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp --help
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_stage3_status uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp status --json
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_stage3_mcp_help uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp mcp serve --help
```

当前结果：三条命令均通过。
