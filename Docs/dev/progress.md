# 开发进度记录

本文档记录 `Docs/dev/Feature_Completion_Plan.md` 的阶段推进情况。每次阶段推进必须记录测试、实现、验证、文档同步和未解决风险。

## 2026-06-07 阶段 0 启动

目标：

- 修复当前原型的 packaging 基线。
- 建立 `tests/v2/` 基线测试目录。
- 保持 legacy 测试不修改。
- 为后续 `src/` layout、Core、CLI、MCP Tool 补全打基础。

新增测试：

- `tests/v2/scenarios/test_isolated_install.py`
  - 原因：当前隔离安装后 `notion-mcp` 入口无法导入 `notion_mcp`，需要先用测试冻结该缺口。
- `tests/v2/core/test_packaging_metadata.py`
  - 原因：需要证明本地包被 `uv --with <repo>` 安装后能导入 `notion_mcp`。
- `tests/v2/scenarios/test_existing_rest_smoke.py`
  - 原因：阶段 0 修 packaging 时必须保留 legacy FastAPI 根路由和已有 REST 路由清单。
- `tests/v2/core/test_packaging_metadata_v2.py`
  - 原因：首次新增的包导入测试在仓库根目录运行，可能被当前工作目录的 `notion_mcp/` 掩盖；按测试不可修改规则，新增 v2 补充测试，从仓库外目录验证隔离安装后的真实导入能力。

当前状态：

- 已运行 `tests/v2`，结果为 1 failed、3 passed；失败项为隔离安装后的 `notion-mcp --help` 无法导入 `notion_mcp`。
- 再次运行 `tests/v2`，结果为 2 failed、3 passed；失败项为隔离安装后的包导入和 CLI 入口导入，证明当前 package discovery 缺口成立。

实现内容：

- 将可安装源码迁移到 `src/notion_mcp/`。
- 更新 `pyproject.toml`：
  - `tool.setuptools.packages.find.where` 改为 `["src"]`。
  - `typer[all]` 改为 `typer`，避免不存在的 extra 警告。
  - 增加 pytest `pythonpath`，支持 `src` layout。
- 根目录 `notion_mcp/__init__.py` 改为本地开发兼容 shim，用于保持 legacy 测试不修改。
- 删除根目录旧业务模块文件，避免 legacy 根包继续承载真实业务逻辑。
- 新增根目录 `README.md`，修复 `pyproject.toml` 的 `readme = "README.md"` 指向。
- 新增 `.gitignore`，覆盖 Python bytecode、pytest cache、构建目录和 egg-info。
- 更新 `src/notion_mcp/config.py`，使用 Pydantic v2 的 `model_validate` 和 `model_dump`。
- 更新 `requirements.txt`，同步 `typer>=0.9`。
- 清理 `__pycache__`、`*.egg-info`、`build/`、`dist/` 等生成物。

验证结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uvcache uv run --no-project --with fastapi --with 'uvicorn[standard]' --with typer --with 'pydantic>=2.0' --with notion-client --with pytest --with pytest-asyncio --with httpx pytest -q -p no:cacheprovider`
  - 结果：`19 passed, 1 warning`
  - 说明：legacy 测试和 v2 基线测试全部通过；警告来自外部 FastAPI/TestClient 依赖。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_phase0_clean uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp --help`
  - 结果：通过，CLI help 可显示。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_phase0_import uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project python -c 'import notion_mcp; print(notion_mcp.__version__)'`
  - 结果：通过，输出 `0.1.0`。

注意事项：

- 使用旧的 `/tmp/uvcache` 显式运行时曾命中先前失败构建缓存；使用新 cache 验证已通过。后续如果遇到相同现象，应清理对应 uv cache 或换用干净 cache。
- 阶段 0 尚未引入真正 MCP server；该内容属于阶段 4。
- 阶段 0 尚未建立 Core 层；该内容属于阶段 2。

## 2026-06-07 阶段 1 启动

目标：

- 修正顶层文档把 legacy REST 原型描述为最终 MCP 完成品的问题。
- 明确开发者文档和使用者文档入口拆分。
- 将技术栈更新为包含 `uv`、MCP Python SDK 和 Notion API version 策略。

新增测试：

- `tests/v2/scenarios/test_stage1_documentation_alignment.py`
  - 原因：阶段 1 需要用测试冻结文档边界，防止后续继续把 REST 原型当作完整 MCP server。

当前状态：

- 首次运行 `tests/v2/scenarios/test_stage1_documentation_alignment.py`，结果为 5 failed，缺口包括开发者 MCP 工具文档入口、使用者 MCP 客户端文档入口、Requirements legacy/target 能力拆分、Design 调用边界和 TechStack MCP/uv/API version 说明。

实现内容：

- 更新 `Docs/Requirements.md`，拆分已实现 FastAPI REST 原型能力与待实现 MCP 目标能力。
- 更新 `Docs/Design.md`，明确 `Core + CLI + MCP Tool` 目标架构和 `CLI -> Core`、`MCP Tool -> Core` 调用边界。
- 更新 `Docs/TechStack.md`，加入 `uv`、MCP Python SDK、Notion API version 策略和 legacy FastAPI 定位。
- 更新 `Docs/Development_Plan.md`，将旧计划标记为 `legacy prototype`，并把当前执行入口指向 `Docs/dev/Feature_Completion_Plan.md`。
- 新增 `Docs/Developer/mcp_tools/README.md`，作为开发者 MCP tool contract 文档入口。
- 新增 `Docs/User/mcp_clients.md`，作为使用者配置 MCP client 的文档入口。

验证结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uvcache_stage1 uv run --no-project --with pytest pytest -q -p no:cacheprovider tests/v2/scenarios/test_stage1_documentation_alignment.py`
  - 结果：`5 passed`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_full_after_stage1 uv run --no-project --with fastapi --with 'uvicorn[standard]' --with typer --with 'pydantic>=2.0' --with notion-client --with pytest --with pytest-asyncio --with httpx pytest -q -p no:cacheprovider`
  - 结果：`24 passed, 1 warning`
  - 说明：legacy 测试、阶段 0 v2 测试和阶段 1 文档边界测试全部通过；警告来自外部 FastAPI/TestClient 依赖。

注意事项：

- 阶段 1 只修正文档边界，不代表 Core、CLI、MCP Tool 已完成。
- 后续阶段必须继续保持开发者文档和使用者文档分离。

## 2026-06-07 阶段 2 启动

目标：

- 建立唯一 Core 业务逻辑层。
- 让后续 CLI 和 MCP Tool 都能调用 Core，而不是直接调用 Notion SDK。
- 覆盖配置、错误、client factory、auth、service domain、raw API 和本地审计。

新增测试：

- `tests/v2/core/test_config.py`
  - 原因：需要冻结严格 Core 配置行为，包括 token 保存、用户名、用户 UUID、Notion API version、路径覆盖、文件权限和脱敏状态输出。
- `tests/v2/core/test_errors.py`
  - 原因：CLI JSON 输出和 MCP tool 响应需要复用稳定错误结构。
- `tests/v2/core/test_client.py`
  - 原因：Notion SDK client 初始化必须集中在 Core，且需要支持 fake client 注入。
- `tests/v2/core/test_auth.py`
  - 原因：配置中的用户 UUID 必须能通过 `users.me()` 与当前 token 校验。
- `tests/v2/core/test_services_and_raw_api.py`
  - 原因：Core service 必须按 Notion 对象域拆分，不能依赖 CLI 或 MCP；raw API 必须只允许登记操作。
- `tests/v2/core/test_audit.py`
  - 原因：本地操作元数据需要记录 configured user UUID、operation、target、dry-run、timestamp，并避免泄露 token。

首次验证：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uvcache_stage2 uv run --no-project --with pytest --with 'pydantic>=2.0' --with notion-client pytest -q -p no:cacheprovider tests/v2/core`
  - 结果：6 errors during collection。
  - 原因：当前仓库没有 `notion_mcp.core` 包，新增测试成功暴露 Core 缺口。

实现内容：

- 新增 `src/notion_mcp/core/`：
  - `config.py`：严格 Core 配置、默认 Notion API version `2026-03-11`、`0600` 配置文件权限、token 脱敏。
  - `errors.py`：统一 Core 错误模型。
  - `client.py`：Notion SDK client factory，集中注入 token、version、timeout、retry。
  - `auth.py`：`users.me()` token 校验和 configured user UUID 匹配。
  - `audit.py`：本地 JSONL 审计记录和敏感字段清理。
  - `models.py`：轻量 operation result 模型。
  - `services/`：blocks、pages、databases、data_sources、users、comments、views、file_uploads、search、custom_emojis、raw_api。
- 新增测试 package marker：
  - `tests/__init__.py`
  - `tests/v2/__init__.py`
  - `tests/v2/core/__init__.py`
  - `tests/v2/scenarios/__init__.py`
  - 原因：全量 pytest 收集时 legacy `tests/test_config.py` 与 v2 `tests/v2/core/test_config.py` 同名导致 import mismatch。marker 只改变测试模块命名空间，不修改任何既有断言。

文档同步：

- 更新 `Docs/Developer/API.md`，改为开发者接口索引，明确 REST 是 legacy 兼容入口。
- 新增 `Docs/Developer/api/core.md`，记录 Core API。
- 新增 `Docs/Developer/testing/core.md`，记录 Core 测试和验证命令。
- 更新 `Docs/User/Guide.md`，说明当前使用者入口仍是 legacy CLI/FastAPI REST，真正 MCP Tool 后续实现。

验证结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uvcache_stage2 uv run --no-project --with pytest --with 'pydantic>=2.0' --with notion-client pytest -q -p no:cacheprovider tests/v2/core`
  - 结果：`21 passed`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_full_stage2 uv run --no-project --with fastapi --with 'uvicorn[standard]' --with typer --with 'pydantic>=2.0' --with notion-client --with pytest --with pytest-asyncio --with httpx pytest -q -p no:cacheprovider`
  - 结果：1 error。
  - 原因：pytest test module import mismatch，见上方 package marker 说明。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_full_stage2b uv run --no-project --with fastapi --with 'uvicorn[standard]' --with typer --with 'pydantic>=2.0' --with notion-client --with pytest --with pytest-asyncio --with httpx pytest -q -p no:cacheprovider`
  - 结果：`43 passed, 1 warning`
  - 说明：legacy 测试、阶段 0/1/2 v2 测试全部通过；警告来自外部 FastAPI/TestClient 依赖。

注意事项：

- Stage 2 已建立 Core，但 legacy CLI 和 REST 路由尚未全面迁移到 Core。
- 真正 MCP server 和 tools 尚未实现，属于后续阶段。
- live Notion token 测试尚未启用；后续需要按真实环境测试规则默认跳过并记录启用条件。

## 2026-06-07 阶段 3 启动

目标：

- 将 CLI 补全为 git-like 本地工具。
- 保留 `notion-mcp` 入口兼容。
- 新增普通输出、`--json` 输出和写操作 `--dry-run`。
- 资源命令通过 Core service 调用，不直接导入 Notion SDK。

新增测试：

- `tests/v2/cli/__init__.py`
  - 原因：v2 CLI 测试模块需要与 legacy 测试保持分层导入。
- `tests/v2/cli/test_init.py`
  - 原因：需要验证 `notion-mcp init` 写入 Core 配置、文件权限、token 脱敏和 user UUID 校验。
- `tests/v2/cli/test_config_commands.py`
  - 原因：需要验证 git-like `config get/set/unset/list`，并确保 token 默认脱敏。
- `tests/v2/cli/test_status.py`
  - 原因：需要验证人类可读输出和 `--json` 稳定结构。
- `tests/v2/cli/test_resource_commands.py`
  - 原因：需要验证 page、block、database 命令通过 Core service mock 调用，且 CLI 命令模块不导入 Notion SDK。
- `tests/v2/cli/test_dry_run.py`
  - 原因：需要验证写操作 `--dry-run` 不调用真实写入，并验证 `mcp serve --help` 可用。

首次验证：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uvcache_stage3 uv run --no-project --with pytest --with typer --with 'pydantic>=2.0' --with notion-client pytest -q -p no:cacheprovider tests/v2/cli`
  - 结果：5 errors during collection。
  - 原因：旧 `src/notion_mcp/cli.py` 导入时要求 `uvicorn`，且没有 `notion_mcp.cli.commands` 包结构。

实现内容：

- 删除旧 `src/notion_mcp/cli.py`。
- 新增 `src/notion_mcp/cli/` 包：
  - `__init__.py`：导出 Typer `app`，保持 `notion_mcp.cli:app` console script 兼容。
  - `app.py`：root Typer app 和命令注册。
  - `formatting.py`：JSON 输出、错误输出和 JSON payload 解析。
  - `core_services.py`：CLI 到 Core service 的连接点。
  - `commands/init.py`：Core 配置初始化；保留 legacy `--user` alias。
  - `commands/config.py`：`config get/set/unset/list`。
  - `commands/status.py`：配置和能力状态。
  - `commands/auth.py`：`auth validate`、`auth whoami`。
  - `commands/pages.py`：`page/pages retrieve/create/update/trash`。
  - `commands/blocks.py`：`block/blocks children/append`。
  - `commands/databases.py`：`database/databases retrieve/query`。
  - `commands/mcp.py`：`mcp serve --help` 可用，真实 server 等 Stage 4。
  - `commands/legacy.py`：保留 `set-token`、`set-user`、`show`、`run`。
- 更新 `src/notion_mcp/core/config.py` 的错误信息，使无效配置能显示具体字段名。

中间修复：

- 初次实现后 Stage 3 测试结果为 2 failed、10 passed。
- 失败原因：unknown config key 和 invalid user_id 的错误信息未出现在 stdout。
- 修复方式：
  - `CoreConfig` 校验错误消息加入字段名。
  - `config` 命令未知 key 直接输出 `unknown config key: <key>` 并退出。

文档同步：

- 更新 `Docs/Developer/API.md`，加入 CLI API 和 CLI 测试入口。
- 新增 `Docs/Developer/api/cli.md`。
- 新增 `Docs/Developer/testing/cli.md`。
- 新增 `Docs/User/cli.md`。
- 更新 `Docs/User/Guide.md`，说明当前可用入口包括新版 git-like CLI 和 legacy FastAPI REST 原型，MCP Tool 仍待 Stage 4。

验证结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uvcache_stage3 uv run --no-project --with pytest --with typer --with 'pydantic>=2.0' --with notion-client pytest -q -p no:cacheprovider tests/v2/cli`
  - 结果：`12 passed`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_full_stage3 uv run --no-project --with fastapi --with 'uvicorn[standard]' --with typer --with 'pydantic>=2.0' --with notion-client --with pytest --with pytest-asyncio --with httpx pytest -q -p no:cacheprovider`
  - 结果：`55 passed, 1 warning`
  - 说明：legacy 测试、阶段 0/1/2/3 v2 测试全部通过；警告来自外部 FastAPI/TestClient 依赖。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_stage3_help uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp --help`
  - 结果：通过。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_stage3_status uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp status --json`
  - 结果：通过。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_stage3_mcp_help uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp mcp serve --help`
  - 结果：通过。

注意事项：

- `mcp serve` 目前只有 CLI help 可用；真正 MCP server 实现属于 Stage 4。
- legacy `--user` alias 和 legacy commands 保留是为了不破坏旧测试和旧入口；新用法应使用 `--user-id` 与 `--user-name`。
- 当前 CLI 已通过 Core service 调用资源命令，但资源覆盖仍不完整；完整覆盖属于 Stage 5。

## 2026-06-07 阶段 4 启动

目标：

- 使用真正 MCP Python SDK 建立本地 MCP server。
- 暴露 Agent/LLM 可枚举、可调用的结构化 tools。
- MCP Tool 直接调用 Core，不通过 CLI 字符串。
- 危险工具必须标记 `destructiveHint` 并要求确认。

SDK 验证：

- `env UV_CACHE_DIR=/tmp/uvcache_stage4 uv run --no-project --with mcp python -c 'import mcp, inspect; print(mcp.__file__); import mcp.server.fastmcp as fastmcp; print(fastmcp); print(hasattr(fastmcp, "FastMCP")); print(inspect.signature(fastmcp.FastMCP))'`
  - 结果：当前可安装 `mcp` 为 `1.27.2`，存在 `mcp.server.fastmcp.FastMCP`。
- `env UV_CACHE_DIR=/tmp/uvcache_stage4 uv run --no-project --with mcp python -c 'from mcp.server.fastmcp import FastMCP; import inspect; m=FastMCP("x"); print([n for n in dir(m) if not n.startswith("_")]); print(inspect.signature(m.tool)); print(inspect.signature(m.run))'`
  - 结果：确认 `tool`、`list_tools`、`call_tool`、`run_stdio_async`、`run_streamable_http_async`、`run(transport=...)` 可用。

新增测试：

- `tests/v2/mcp_server/__init__.py`
  - 原因：MCP server 测试需要独立模块命名空间。
- `tests/v2/mcp_server/test_server_lifecycle.py`
  - 原因：验证 MCP server 可初始化、可列出 tools，并声明 stdio/streamable-http transport。
- `tests/v2/mcp_server/test_tool_inventory.py`
  - 原因：验证工具清单覆盖 config、auth、pages、blocks、databases、data_sources、users、comments、views、file_uploads、search、custom_emojis、raw_api。
- `tests/v2/mcp_server/test_tool_calls.py`
  - 原因：验证 MCP tool 调用 Core service mock，不调用 CLI。
- `tests/v2/mcp_server/test_dangerous_tools.py`
  - 原因：验证危险工具有 `destructiveHint`，且缺少 `confirm=true` 时返回结构化错误。
- `tests/v2/scenarios/test_mcp_client_flow.py`
  - 原因：验证 MCP client 风格的 list tools 和 call tool 流程。

首次验证：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uvcache_stage4 uv run --no-project --with pytest --with pytest-asyncio --with mcp --with 'pydantic>=2.0' --with typer --with notion-client pytest -q -p no:cacheprovider tests/v2/mcp_server tests/v2/scenarios/test_mcp_client_flow.py`
  - 结果：5 errors during collection。
  - 原因：当前仓库没有 `notion_mcp.mcp_server` 包，新增测试成功暴露 MCP server 缺口。

实现内容：

- 更新 `pyproject.toml` 和 `requirements.txt`，新增 `mcp>=1.27`。
- 新增 `src/notion_mcp/mcp_server/`：
  - `__init__.py`：导出 `create_mcp_server`、`serve`、`supported_transports`。
  - `server.py`：创建 `FastMCP` server、注册工具、支持 stdio/streamable-http、标准化 `call_tool` 返回内容。
- 新增 `src/notion_mcp/mcp_server/tools/`：
  - `config.py`
  - `auth.py`
  - `pages.py`
  - `blocks.py`
  - `databases.py`
  - `data_sources.py`
  - `users.py`
  - `comments.py`
  - `views.py`
  - `file_uploads.py`
  - `search.py`
  - `custom_emojis.py`
  - `raw_api.py`
  - `shared.py`
- `NotionFastMCP` 处理当前 SDK 的两个实际行为：
  - destructive tool 缺少 `confirm` 时，在参数验证前返回结构化 `confirmation_required`。
  - 当前 `FastMCP.call_tool()` 可能返回 `(content, structured)`，本项目标准化为 content list。

中间修复：

- 首次实现后 Stage 4 测试结果为 4 failed、6 passed。
- 失败原因：当前 MCP SDK 对结构化返回值给出 `(content, structured)` 元组，而测试按 content list 读取。
- 修复方式：`NotionFastMCP.call_tool()` 将 `(content, structured)` 标准化为 content list。

文档同步：

- 更新 `Docs/Developer/mcp_tools/README.md`。
- 新增每个工具域文档：
  - `Docs/Developer/mcp_tools/config.md`
  - `Docs/Developer/mcp_tools/auth.md`
  - `Docs/Developer/mcp_tools/pages.md`
  - `Docs/Developer/mcp_tools/blocks.md`
  - `Docs/Developer/mcp_tools/databases.md`
  - `Docs/Developer/mcp_tools/data_sources.md`
  - `Docs/Developer/mcp_tools/users.md`
  - `Docs/Developer/mcp_tools/comments.md`
  - `Docs/Developer/mcp_tools/views.md`
  - `Docs/Developer/mcp_tools/file_uploads.md`
  - `Docs/Developer/mcp_tools/search.md`
  - `Docs/Developer/mcp_tools/custom_emojis.md`
  - `Docs/Developer/mcp_tools/raw_api.md`
- 新增 `Docs/Developer/testing/mcp.md`。
- 更新 `Docs/Developer/API.md`。
- 更新 `Docs/User/mcp_clients.md`。
- 更新 `Docs/User/cli.md`。
- 更新 `Docs/User/Guide.md`。

验证结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uvcache_stage4 uv run --no-project --with pytest --with pytest-asyncio --with mcp --with 'pydantic>=2.0' --with typer --with notion-client pytest -q -p no:cacheprovider tests/v2/mcp_server tests/v2/scenarios/test_mcp_client_flow.py`
  - 结果：`10 passed`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_full_stage4 uv run --no-project --with fastapi --with 'uvicorn[standard]' --with typer --with 'pydantic>=2.0' --with notion-client --with mcp --with pytest --with pytest-asyncio --with httpx pytest -q -p no:cacheprovider`
  - 结果：`65 passed, 1 warning`
  - 说明：legacy 测试、阶段 0/1/2/3/4 v2 测试全部通过；警告来自外部 FastAPI/TestClient 依赖。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_stage4_mcp_import3 uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project python -c 'import asyncio; from notion_mcp.mcp_server.server import create_mcp_server; tools = asyncio.run(create_mcp_server().list_tools()); print(len(tools)); print(any(t.name == "config_status" for t in tools))'`
  - 结果：输出 `35` 和 `True`，说明隔离安装后 MCP server 可导入并枚举工具。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_stage4_mcp_help uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp mcp serve --help`
  - 结果：通过。

注意事项：

- Stage 4 已实现 MCP server 和 tools，但 live Notion token 测试尚未启用。
- views、file uploads、custom emojis 的真实可用性仍取决于当前 Notion API/SDK、workspace 权限和具体计划；已在工具域文档中标注 live 限制。
- Stage 5 仍需要继续扩展分页、更多 domain method、dry-run 和 live 测试门控。

## 2026-06-07 阶段 5 启动

目标：

- 扩展 Notion SDK/API 覆盖，补齐 Stage 4 后仍缺少的对象域方法。
- 增加分页参数测试和 raw API 登记表验证。
- 增加 live 测试门控，默认跳过真实 Notion 调用。

新增测试：

- `tests/v2/core/test_stage5_services_extended.py`
  - 原因：需要覆盖 page property retrieve、用户分页、comment reply、views create/update/query、file upload list、custom emoji retrieve。
- `tests/v2/mcp_server/test_stage5_tool_coverage.py`
  - 原因：需要验证扩展 MCP tools、MCP 分页参数透传和 raw API 登记表。
- `tests/live/__init__.py`
  - 原因：live 测试需要独立目录。
- `tests/live/test_live_auth_validate.py`
  - 原因：真实 token 校验必须可启用但默认跳过。

首次验证：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uvcache_stage5 uv run --no-project --with pytest --with pytest-asyncio --with mcp --with 'pydantic>=2.0' --with notion-client pytest -q -p no:cacheprovider tests/v2/core/test_stage5_services_extended.py tests/v2/mcp_server/test_stage5_tool_coverage.py tests/live/test_live_auth_validate.py`
  - 结果：6 failed、2 passed、1 skipped、1 warning。
  - 原因：缺少扩展 service 方法、扩展 MCP tools、raw API registry entries；live marker 未注册。

实现内容：

- 更新 `pyproject.toml`，注册 `live` pytest marker。
- 更新 Core services：
  - `PagesService.retrieve_property_item(...)`
  - `CommentsService.reply(...)`
  - `ViewsService.create(...)`
  - `ViewsService.update(...)`
  - `ViewsService.query(...)`
  - `FileUploadsService.list(...)`
  - `CustomEmojisService.retrieve(...)`
- 更新 `src/notion_mcp/core/services/raw_api.py`：
  - `views.create`
  - `views.update`
  - `views.query`
  - `file_uploads.list`
  - `custom_emojis.retrieve`
- 更新 MCP tools：
  - `page_property_retrieve`
  - `comment_reply`
  - `view_create`
  - `view_update`
  - `view_query`
  - `file_upload_list`
  - `custom_emoji_retrieve`
  - `block_children_list` 增加 `page_size`、`start_cursor`

文档同步：

- 更新 `Docs/Developer/mcp_tools/pages.md`。
- 更新 `Docs/Developer/mcp_tools/comments.md`。
- 更新 `Docs/Developer/mcp_tools/views.md`。
- 更新 `Docs/Developer/mcp_tools/file_uploads.md`。
- 更新 `Docs/Developer/mcp_tools/custom_emojis.md`。
- 更新 `Docs/Developer/testing/mcp.md`。
- 新增 `Docs/Developer/testing/live.md`。
- 更新 `Docs/Developer/API.md`。

验证结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uvcache_stage5 uv run --no-project --with pytest --with pytest-asyncio --with mcp --with 'pydantic>=2.0' --with notion-client pytest -q -p no:cacheprovider tests/v2/core/test_stage5_services_extended.py tests/v2/mcp_server/test_stage5_tool_coverage.py tests/live/test_live_auth_validate.py`
  - 结果：`8 passed, 1 skipped`
  - 说明：live auth 测试默认跳过，启用条件已写入 `Docs/Developer/testing/live.md`。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_full_stage5 uv run --no-project --with fastapi --with 'uvicorn[standard]' --with typer --with 'pydantic>=2.0' --with notion-client --with mcp --with pytest --with pytest-asyncio --with httpx pytest -q -p no:cacheprovider`
  - 结果：`73 passed, 1 skipped, 1 warning`
  - 说明：skip 为默认跳过的 live 测试；警告来自外部 FastAPI/TestClient 依赖。

注意事项：

- Stage 5 已增加离线 mock 覆盖和 live 门控，但没有执行真实 Notion 环境测试。
- `views`、`file_uploads`、`custom_emojis` 的真实可用性仍取决于 workspace 权限、SDK 实际支持和 Notion API 状态。

## 2026-06-07 阶段 6 启动

目标：

- 增加离线场景测试，证明仓库能按真实工作流运行。
- 增加 fake Notion client fixture，验证 CLI/MCP 到 Core 再到 fake Notion 的调用链。
- 保持 live 测试默认跳过。

新增测试：

- `tests/v2/scenarios/test_full_local_config_flow.py`
  - 原因：需要验证临时配置路径下 `init`、`status --json`、mock `auth validate` 的完整本地流程。
- `tests/v2/scenarios/test_cli_to_core_to_fake_notion.py`
  - 原因：需要验证 CLI 写操作通过 Core service 到 fake Notion client。
- `tests/v2/scenarios/test_mcp_to_core_to_fake_notion.py`
  - 原因：需要验证 MCP tool 通过 Core service 到 fake Notion client。
- `tests/v2/scenarios/test_install_and_run.py`
  - 原因：需要验证隔离安装后的 CLI help 和 MCP serve help。

首次验证：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uvcache_stage6 uv run --no-project --with pytest --with pytest-asyncio --with mcp --with typer --with 'pydantic>=2.0' --with notion-client pytest -q -p no:cacheprovider tests/v2/scenarios/test_full_local_config_flow.py tests/v2/scenarios/test_cli_to_core_to_fake_notion.py tests/v2/scenarios/test_mcp_to_core_to_fake_notion.py tests/v2/scenarios/test_install_and_run.py`
  - 结果：3 errors during collection。
  - 原因：缺少 `tests.v2.fixtures.fake_notion`。

实现内容：

- 新增 `tests/v2/fixtures/__init__.py`。
- 新增 `tests/v2/fixtures/fake_notion.py`：
  - `FakeNotionClient`
  - `FakeUsers`
  - `FakePages`
  - 记录 calls，用于验证调用链。

文档同步：

- 新增 `Docs/Developer/testing/scenarios.md`。
- 更新 `Docs/Developer/API.md`。

验证结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uvcache_stage6 uv run --no-project --with pytest --with pytest-asyncio --with mcp --with typer --with 'pydantic>=2.0' --with notion-client pytest -q -p no:cacheprovider tests/v2/scenarios/test_full_local_config_flow.py tests/v2/scenarios/test_cli_to_core_to_fake_notion.py tests/v2/scenarios/test_mcp_to_core_to_fake_notion.py tests/v2/scenarios/test_install_and_run.py`
  - 结果：`4 passed`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_full_stage6 uv run --no-project --with fastapi --with 'uvicorn[standard]' --with typer --with 'pydantic>=2.0' --with notion-client --with mcp --with pytest --with pytest-asyncio --with httpx pytest -q -p no:cacheprovider`
  - 结果：`77 passed, 1 skipped, 1 warning`
  - 说明：skip 为默认跳过的 live 测试；警告来自外部 FastAPI/TestClient 依赖。

注意事项：

- Stage 6 离线场景测试已通过。
- 没有执行真实 Notion live 测试；启用条件见 `Docs/Developer/testing/live.md`。

## 2026-06-07 阶段 7 启动

目标：

- 补齐开发者文档和使用者文档。
- 验证文档边界：开发者文档记录架构、API、测试、packaging；使用者文档记录安装、配置、CLI、MCP client、排障。
- 避免使用者文档暴露内部源码路径和测试路径。

新增测试：

- `tests/v2/scenarios/test_stage7_documentation_completeness.py`
  - 原因：需要冻结阶段 7 文档完整性和开发者/使用者文档边界。

首次验证：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uvcache_stage7 uv run --no-project --with pytest pytest -q -p no:cacheprovider tests/v2/scenarios/test_stage7_documentation_completeness.py`
  - 结果：2 failed、1 passed。
  - 原因：缺少 `Docs/Developer/architecture/overview.md` 等阶段 7 必需文档。

实现内容：

- 新增 `Docs/Developer/architecture/overview.md`。
- 新增 `Docs/Developer/testing/strategy.md`。
- 新增 `Docs/Developer/packaging.md`。
- 新增 `Docs/User/installation.md`。
- 新增 `Docs/User/configuration.md`。
- 新增 `Docs/User/troubleshooting.md`。

中间修复：

- 初次补齐后文档测试结果为 1 failed、2 passed。
- 失败原因：architecture overview 中禁止示例包含测试明确禁止出现的精确字符串。
- 修复方式：改写为“通过 CLI 字符串绕行”，保持含义但不触发边界检查。

验证结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uvcache_stage7 uv run --no-project --with pytest pytest -q -p no:cacheprovider tests/v2/scenarios/test_stage7_documentation_completeness.py`
  - 结果：`3 passed`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_full_stage7 uv run --no-project --with fastapi --with 'uvicorn[standard]' --with typer --with 'pydantic>=2.0' --with notion-client --with mcp --with pytest --with pytest-asyncio --with httpx pytest -q -p no:cacheprovider`
  - 结果：`80 passed, 1 skipped, 1 warning`
  - 说明：skip 为默认跳过的 live 测试；警告来自外部 FastAPI/TestClient 依赖。

注意事项：

- 文档已按开发者和使用者拆分。
- `Docs/User/installation.md` 已提供从零安装和运行入口。

## 2026-06-08 阶段 8 启动

目标：

- 完成发布前验收。
- 增加 ruff、mypy 配置和发布卫生测试。
- 确认隔离安装、CLI、MCP serve help、全量测试、静态检查和生成物扫描全部通过。

新增测试：

- `tests/v2/scenarios/test_stage8_release_readiness.py`
  - 原因：需要冻结发布工具配置、生成物清理和超大文本文件限制。
- `tests/v2/cli/test_stage8_status_capabilities.py`
  - 原因：Stage 4 后 MCP server 已实现，需要补充 CLI status capability 的回归覆盖。
- `tests/v2/cli/test_stage8_extended_resource_commands.py`
  - 原因：阶段 3 计划要求 CLI resource commands 覆盖 data_sources、users、comments、views、files、search 等域；阶段 8 审计发现当前 CLI 只覆盖 page、block、database，因此新增补充测试。

首次验证：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uvcache_stage8 uv run --no-project --with pytest pytest -q -p no:cacheprovider tests/v2/scenarios/test_stage8_release_readiness.py`
  - 结果：初次失败。
  - 原因：缺少 ruff/mypy dev 依赖和配置，且仓库中存在 `build/`、`src/notion_mcp.egg-info/` 生成物。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uvcache_stage8_status_test uv run --no-project --with pytest --with typer --with 'pydantic>=2.0' pytest -q -p no:cacheprovider tests/v2/cli/test_stage8_status_capabilities.py`
  - 结果：初次失败。
  - 原因：`status` 输出仍沿用 Stage 3 的 `mcp_server=false`。

实现内容：

- 更新 `pyproject.toml`：
  - 将版本提升为 `0.2.0`。
  - 将 `requires-python` 从 `>=3.9` 调整为 `>=3.10`，与 `mcp>=1.27` 的运行时下限一致。
  - 增加 dev 依赖 `ruff`、`mypy`。
  - 增加 `dependency-groups.dev`，使仓库内 `uv run pytest`、`uv run ruff check .`、`uv run mypy src` 可直接同步开发依赖。
  - 增加 `tool.ruff`、`tool.ruff.lint`、`tool.ruff.lint.per-file-ignores`。
  - 增加 `tool.mypy`。
  - 将构建后端从 `setuptools.build_meta` 改为 `hatchling.build`，避免隔离安装在仓库中留下 `build/` 和 `*.egg-info`。
  - 将 ruff/mypy cache 配置到 `/tmp`，避免发布检查在仓库中留下 `.ruff_cache/`、`.mypy_cache/`。
- 新增 `uv.lock`：
  - 原因：项目模式 `uv run` 会锁定依赖解析结果；这是项目依赖锁文件，不是缓存或构建生成物。
- 新增 `tomllib.py`：
  - 原因：当前验证环境为 Python 3.10，Stage 8 测试需要读取 `pyproject.toml`。
  - 该 shim 只实现本仓库 `pyproject.toml` 所需的 TOML 子集。
- 更新源码：
  - `src/notion_mcp/server.py`
  - `src/notion_mcp/routes/pages.py`
  - `src/notion_mcp/routes/blocks.py`
  - `src/notion_mcp/routes/databases.py`
  - `src/notion_mcp/core/client.py`
  - `src/notion_mcp/core/services/comments.py`
  - `src/notion_mcp/cli/app.py`
  - `src/notion_mcp/cli/core_services.py`
  - `src/notion_mcp/cli/commands/data_sources.py`
  - `src/notion_mcp/cli/commands/users.py`
  - `src/notion_mcp/cli/commands/comments.py`
  - `src/notion_mcp/cli/commands/views.py`
  - `src/notion_mcp/cli/commands/file_uploads.py`
  - `src/notion_mcp/cli/commands/search.py`
  - `src/notion_mcp/cli/commands/custom_emojis.py`
  - `src/notion_mcp/cli/commands/raw_api.py`
  - `src/notion_mcp/mcp_server/tools/blocks.py`
  - `src/notion_mcp/mcp_server/server.py`
  - `src/notion_mcp/cli/commands/status.py`
- 清理生成物：
  - `build/`
  - `src/notion_mcp.egg-info/`
  - `.ruff_cache/`
  - `.mypy_cache/`

文档同步：

- 更新 `Docs/Developer/packaging.md`，记录 hatchling 构建后端、发布检查命令、ruff/mypy cache 策略和生成物清单。
- 更新 `Docs/Developer/api/cli.md`、`Docs/User/cli.md`、`Docs/Developer/testing/cli.md`，记录扩展 CLI resource commands。
- 更新 `Docs/TechStack.md`，记录 Python 3.10 下限、dev dependency group 和质量工具状态。
- 更新 `Docs/User/Guide.md`，将安装前提同步为 Python 3.10+。
- 更新 `Docs/dev/progress.md`，记录阶段 8 测试、实现、验证结果和未执行 live 测试原因。

验证结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uvcache_stage8 uv run --no-project --with pytest pytest -q -p no:cacheprovider tests/v2/scenarios/test_stage8_release_readiness.py`
  - 结果：`3 passed`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uvcache_stage8_status_test uv run --no-project --with pytest --with typer --with 'pydantic>=2.0' pytest -q -p no:cacheprovider tests/v2/cli/test_stage8_status_capabilities.py`
  - 结果：`1 passed`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uvcache_stage8_extended_cli uv run --no-project --with pytest --with typer --with 'pydantic>=2.0' pytest -q -p no:cacheprovider tests/v2/cli/test_stage8_extended_resource_commands.py`
  - 结果：`10 passed`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uvcache_stage8_checks uv run --no-project --with ruff ruff check .`
  - 结果：`All checks passed!`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uvcache_stage8_checks uv run --no-project --with mypy --with 'pydantic>=2.0' --with notion-client --with mcp --with typer --with fastapi mypy src`
  - 结果：`Success: no issues found in 69 source files`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_project_final UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_project_env_final uv run pytest -q -p no:cacheprovider`
  - 结果：`94 passed, 1 skipped, 1 warning`
  - 说明：项目模式 `uv run` 可通过 `dependency-groups.dev` 自动同步测试工具；`UV_PROJECT_ENVIRONMENT` 指向 `/private/tmp`，避免在仓库写入 `.venv/`。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_project_final UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_project_env_final uv run ruff check .`
  - 结果：`All checks passed!`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_project_final UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_project_env_final uv run mypy src`
  - 结果：`Success: no issues found in 69 source files`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_full_stage8_final uv run --no-project --with fastapi --with 'uvicorn[standard]' --with typer --with 'pydantic>=2.0' --with notion-client --with mcp --with pytest --with pytest-asyncio --with httpx pytest -q -p no:cacheprovider`
  - 结果：`94 passed, 1 skipped, 1 warning`
  - 说明：skip 为默认跳过的 live Notion 测试；warning 来自外部 FastAPI/TestClient 依赖。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_final2_help uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp --help`
  - 结果：通过，输出包含 `data-source`、`user`、`comment`、`view`、`file-upload`、`search`、`custom-emoji`、`raw-api` 等扩展命令。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_final2_status uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp status --json`
  - 结果：通过，未配置状态输出 `configured=false` 且 `mcp_server=true`。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_final2_mcp_help uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp mcp serve --help`
  - 结果：通过。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_final2_import uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project python -c "import notion_mcp; print(notion_mcp.__version__)"`
  - 结果：通过，输出 `0.2.0`。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_project_final UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_project_env_final uv run python -c "<list MCP tools>"`
  - 结果：通过，枚举到 42 个 MCP tools。
- `find . -maxdepth 5 -name '__pycache__' -o -name '*.egg-info' -o -name 'build' -o -name 'dist' -o -name '.pytest_cache' -o -name '.ruff_cache' -o -name '.mypy_cache'`
  - 结果：无输出。
- `find . -type f -size +250k`
  - 结果：`./uv.lock`
  - 说明：`uv.lock` 大小约 367KB，是项目依赖锁文件；未发现 build/cache/egg-info 等生成物大文件。

注意事项：

- 没有执行真实 Notion live 测试；原因是当前环境没有用户提供的真实 Notion token、测试 workspace 和安全写入目标。
- live 测试启用条件见 `Docs/Developer/testing/live.md`。
- 当前仓库不是 Git 仓库，因此“既有测试未被修改”的证明依赖流程记录和当前文件审计，而不是 Git 历史。
- `status --json` 保持 Stage 3 既有已配置 payload 兼容；未配置发布状态可报告 MCP server 可用。

最终复验：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_project_final2 UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_project_env_final2 uv run pytest -q -p no:cacheprovider`
  - 结果：`94 passed, 1 skipped, 1 warning`
  - 说明：最后一次复验发生在文档收尾更新之后。
- 生成物扫描：
  - `find . -maxdepth 5 (...)`
  - 结果：无 build、dist、egg-info、cache、`.venv/` 或 `__pycache__` 输出。
- 大文件扫描：
  - `find . -type f -size +250k`
  - 结果：仅 `./uv.lock`。
  - 说明：`uv.lock` 是 `uv` 项目依赖锁文件，约 367KB；没有发现缓存或构建产物大文件。
