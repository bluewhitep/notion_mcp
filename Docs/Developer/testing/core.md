# Core 测试文档

本文档面向开发者，记录 Stage 2 Core 层的测试目标和验证命令。

## 测试文件

- `tests/v2/core/test_config.py`
  - 验证配置初始化、读取、更新、路径覆盖、`0600` 权限、token 脱敏、UUID 校验和默认 Notion API version。
- `tests/v2/core/test_errors.py`
  - 验证 Core 错误结构和错误 code。
- `tests/v2/core/test_client.py`
  - 验证 Notion SDK client factory 注入 token、version、timeout、retry，并支持 fake client。
- `tests/v2/core/test_auth.py`
  - 验证 `users.me()` token 校验、配置用户 UUID 匹配和错误包装。
- `tests/v2/core/test_services_and_raw_api.py`
  - 验证 pages/blocks service 包装、2026 block append `position` 参数、service 不导入 CLI/MCP、raw API 登记表。
- `tests/v2/core/test_audit.py`
  - 验证 JSONL 审计记录和敏感字段清理。

## 验证命令

Stage 2 focused tests：

```bash
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uvcache_stage2 uv run --no-project --with pytest --with 'pydantic>=2.0' --with notion-client pytest -q -p no:cacheprovider tests/v2/core
```

当前结果：

```text
21 passed
```

全量当前测试：

```bash
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_full_stage2b uv run --no-project --with fastapi --with 'uvicorn[standard]' --with typer --with 'pydantic>=2.0' --with notion-client --with pytest --with pytest-asyncio --with httpx pytest -q -p no:cacheprovider
```

当前结果：

```text
43 passed, 1 warning
```

警告来自外部 FastAPI/TestClient 依赖，不是当前 Core 实现失败。

## 测试包 marker

已新增以下 package marker：

- `tests/__init__.py`
- `tests/v2/__init__.py`
- `tests/v2/core/__init__.py`
- `tests/v2/scenarios/__init__.py`

原因：legacy `tests/test_config.py` 与 v2 `tests/v2/core/test_config.py` 同名。全量 pytest 收集时会发生 import mismatch。marker 只用于让 pytest 以分层模块名导入测试，不修改任何既有测试断言。
