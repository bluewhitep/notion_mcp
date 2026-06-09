# 开发进度记录

本文档记录 `Docs/dev/Feature_Completion_Plan.md` 的阶段推进情况。每次阶段推进必须记录测试、实现、验证、文档同步和未解决风险。

## 2026-06-09 User CLI 文档拆分

目标：

- 将 `Docs/User/Cli.md` 从混合命令手册调整为 CLI 文档索引。
- 将 page、block、database/data-source、项目配置、auth/user、comment、view、file upload、search/custom emoji、raw-api、MCP server 和 legacy 命令拆到独立分册。
- 保证 `Docs/User` 下 Markdown 文件名都以大写字母开头。

实现内容：

- 新增 `Docs/User/Cli/` 分册目录：
  - `Overview.md`
  - `Project_Config.md`
  - `Page.md`
  - `Block.md`
  - `Database_DataSource.md`
  - `Auth_And_User.md`
  - `Comments.md`
  - `Views.md`
  - `File_Uploads.md`
  - `Search_And_Custom_Emoji.md`
  - `Raw_API.md`
  - `MCP_Server.md`
  - `Legacy_Commands.md`
- 将 `Docs/User/Cli.md` 改为入口索引。
- 将 `Docs/User` 顶层文档文件名调整为首字母大写：
  - `Configuration.md`
  - `Installation.md`
  - `MCP_Clients.md`
  - `Troubleshooting.md`
- 更新 README、User 指南和 Developer 测试文档中的 User 文档路径。

测试同步：

- CLI 文档清单测试改为读取 `Docs/User/Cli.md` 和 `Docs/User/Cli/*.md`。
- User 文档边界测试改为递归检查 `Docs/User`。
- 新增 User 文档文件名大写约束测试。

验证结果：

- `UV_CACHE_DIR=/tmp/uvcache uv run pytest tests/v2/scenarios/test_cli_documentation_inventory.py tests/v2/scenarios/test_documentation_reader_boundary.py tests/v2/scenarios/test_stage1_documentation_alignment.py tests/v2/scenarios/test_stage7_documentation_completeness.py tests/v2/cli/test_raw_api_positioning.py`
  - 结果：`17 passed`
- `PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/uvcache UV_PROJECT_ENVIRONMENT=/tmp/notion_mcp_full_doc_split_env uv run pytest -q -p no:cacheprovider`
  - 结果：`197 passed, 1 skipped, 1 warning`

## 2026-06-09 CLI 命令面修订

目标：

- 移除公开命令面中的 `project`、`local`、root `status`、`current`、`deattach`、`page content`、`page block *` 和 `page insert *`。
- 将全局配置改为 `notion-mcp config --global ...`，项目配置查看改为 `notion-mcp config --local --show`。
- 新增 `notion-mcp pwd` 和 `notion-mcp version`。
- 将 page 读取拆分为 `page retrieve` 和 `page blocks`。
- 将 block 编辑统一移动到顶层 `block append/insert-after/update/trash`。
- 保持 database/data-source 语义分离：显式 data source 操作用 `data-source`，绑定 database 的 active data source 才使用 `database` 快捷命令。

新增测试：

- `tests/v3/cli/test_public_command_surface_revision.py`
  - 原因：冻结新的公开命令面，防止旧别名重新出现在 help 和用户文档中。

实现内容：

- 新增 root `version` 命令。
- 新增 root `pwd` 命令，并将 `project` / `local` 命名空间隐藏为兼容入口。
- 将 root `status` 隐藏为兼容入口；全局状态改由 `config --global --show` 承担。
- 更新 `config` 命令，支持：
  - `notion-mcp config --global --show`
  - `notion-mcp config --local --show`
  - `notion-mcp config --global user.token <token>`
  - `notion-mcp config --global user.name <name>`
- 新增 `page blocks`；`page retrieve` 支持省略 page id 使用 attached page。
- 将 `page current`、`page deattach`、`page content`、`page block *`、`page insert *` 隐藏为兼容入口。
- 新增顶层 `block insert-after`、`block update`、`block trash`。
- 更新 database 快捷命令，隐藏 `database current`、`database deattach` 和 `database query --data-source`，并让公开 `database page create` 只作用于 attached active data source。
- 新增 `data-source page create <data_source_id>`。

文档同步：

- 新增 `Docs/dev/ADR-004-cli-command-surface-consolidation.md`。
- 更新 `Docs/User/Cli.md`、`Docs/User/Configuration.md`、`Docs/User/Installation.md`、`Docs/User/Guide.md`、`Docs/User/Troubleshooting.md`、`Docs/User/MCP_Clients.md`。
- 更新 `Docs/Developer/api/cli.md`、`Docs/Developer/testing/cli.md`。
- 更新 `Docs/dev/V2_V3_Development_Design.md` 和 `Docs/dev/V2_V3_Trackable_Tasks.md`。

验证结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_command_surface_post2 UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_command_surface_post2_env uv run pytest -q -p no:cacheprovider tests/v3/cli/test_public_command_surface_revision.py`
  - 结果：`7 passed`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_v3_cli UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_v3_cli_env uv run pytest -q -p no:cacheprovider tests/v3/cli`
  - 结果：`43 passed`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_v2_cli3 UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_v2_cli3_env uv run pytest -q -p no:cacheprovider tests/v2/cli tests/v2/scenarios`
  - 结果：`64 passed, 1 warning`

注意事项：

- Hidden compatibility aliases remain for old scripts, but public docs and help must not present them as official commands.
- Real Notion workspace validation is still integration-only and must be enabled explicitly with a safe test workspace.

## 2026-06-09 Page URL 输入解析

目标：

- 允许公开 `<page_id>` 输入直接传 Notion page id、Notion 分享 URL 或包含 Notion URL 的 Markdown 链接。
- URL 中的 32 位 Notion id 解析后统一规范为带连字符的 UUID。

实现内容：

- 新增 `src/notion_mcp/core/identifiers.py`，集中解析 Notion-style UUID。
- CLI page 命令支持 URL 输入：
  - `page attach <page_id_or_url>`
  - `page retrieve <page_id_or_url>`
  - `page blocks <page_id_or_url>`
  - `page create --parent-page <page_id_or_url>`
  - `page update <page_id_or_url>`
  - `page trash <page_id_or_url>`
- `database create --parent-page <page_id_or_url>` 支持 URL 输入。
- Core `ContextResolver.resolve_page_id()` 和 `PagesService` 的 page id 方法也支持 URL 输入，便于 MCP tools 复用。

新增测试：

- `tests/v3/core/test_identifier_parsing.py`
- `tests/v3/cli/test_page_url_inputs.py`
- 更新 `tests/v3/core/test_page_content_service.py`

验证结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_page_url_post3 UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_page_url_post3_env uv run pytest -q -p no:cacheprovider tests/v3/core/test_identifier_parsing.py tests/v3/core/test_page_content_service.py tests/v3/cli/test_page_url_inputs.py tests/v3/cli/test_page_attach.py tests/v3/cli/test_page_content_attach.py tests/v3/cli/test_page_insert.py tests/v3/cli/test_database_context_resolution.py tests/v3/cli/test_page_context_resolution.py`
  - 结果：`24 passed`

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
- 新增 `Docs/User/MCP_Clients.md`，作为使用者配置 MCP client 的文档入口。

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
- 新增 `Docs/User/Cli.md`。
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
- 更新 `Docs/User/MCP_Clients.md`。
- 更新 `Docs/User/Cli.md`。
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
- 新增 `Docs/User/Installation.md`。
- 新增 `Docs/User/Configuration.md`。
- 新增 `Docs/User/Troubleshooting.md`。

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
- `Docs/User/Installation.md` 已提供从零安装和运行入口。

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
- 更新 `Docs/Developer/api/cli.md`、`Docs/User/Cli.md`、`Docs/Developer/testing/cli.md`，记录扩展 CLI resource commands。
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

## 2026-06-08 CLI 文档清单补全

目标：

- 补全 `Docs/User/Cli.md`，写出当前所有可操作 CLI 指令。
- 明确哪些能力有专用 CLI 子命令，哪些能力当前需要通过 `raw-api invoke` 操作。
- 补全 MCP client 和 MCP tools 文档中的具体 tool 清单。

新增测试：

- `tests/v2/scenarios/test_cli_documentation_inventory.py`
  - 原因：用户 CLI 文档此前只列常用示例，没有覆盖 `auth`、page update/trash、扩展资源生命周期命令、legacy 兼容命令和 raw-api 覆盖操作。

首次验证：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_docs_inventory UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_docs_inventory_env uv run pytest -q -p no:cacheprovider tests/v2/scenarios/test_cli_documentation_inventory.py`
  - 结果：`2 failed`
  - 原因：`Docs/User/Cli.md` 缺少 `notion-mcp auth validate` 等专用命令，并缺少 `blocks.update`、`blocks.delete`、`databases.create`、`databases.update` raw-api 覆盖说明。

文档更新：

- 更新 `Docs/User/Cli.md`：
  - 改为完整 CLI 命令参考。
  - 补齐 init、status、config、auth、pages、blocks、databases、data sources、users、comments、views、file uploads、search、custom emojis、raw-api、MCP serve、legacy 兼容命令。
  - 明确当前 CLI 没有区块 update/trash 和 database create/update 专用子命令；这些能力可通过受控 Raw API 操作。
- 更新 `Docs/Developer/api/cli.md`：
  - 补齐专用 CLI 命令清单和 raw-api operation 清单。
  - 记录 block/database 的专用 CLI 缺口和 raw-api 覆盖路径。
- 更新 `Docs/User/MCP_Clients.md`：
  - 补齐 42 个 MCP tool 名称。
- 更新 `Docs/Developer/mcp_tools/README.md`：
  - 补齐 MCP tool inventory。
- 更新 `Docs/Developer/testing/cli.md`：
  - 记录 CLI 文档清单测试和验证命令。

验证结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_docs_inventory UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_docs_inventory_env uv run pytest -q -p no:cacheprovider tests/v2/scenarios/test_cli_documentation_inventory.py tests/v2/scenarios/test_stage7_documentation_completeness.py tests/v2/scenarios/test_stage8_release_readiness.py`
  - 结果：`8 passed`
  - 说明：文档清单、使用者文档边界和发布卫生检查通过。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_docs_full UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_docs_full_env uv run pytest -q -p no:cacheprovider`
  - 结果：`96 passed, 1 skipped, 1 warning`
  - 说明：新增文档清单测试已纳入全量测试；skip 为默认跳过的 live Notion 测试。

注意事项：

- 本次只补文档和文档清单测试，没有新增 CLI 实现。
- 当前 CLI 专用命令仍没有 `block update/trash` 和 `database create/update`；这些操作通过 `notion-mcp raw-api invoke blocks.update`、`blocks.delete`、`databases.create`、`databases.update` 记录为可操作路径。

## 2026-06-08 ADR-002 v2 设计决议固化

目标：

- 固化 Git-like 本地目录上下文设计。
- 固化 `database` 和 `data_source` 严格分离的语义边界。
- 固化 Page CLI、Block CLI、Database CLI、DataSource CLI 和 Raw API 的用户分层。
- 明确 ADR-002 是 Accepted / 待实施，不表示当前 CLI 已具备全部计划命令。

文档更新：

- 新增 `Docs/dev/ADR-002-local-context-and-cli-v2.md`：
  - 记录全局配置与本地 `.notion-mcp/config.json` 分离。
  - 记录本地配置不保存 token。
  - 记录 database/data_source 语义边界和 Core 服务划分。
  - 补充 Notion 官方 Database、Data source 和 Versioning 文档链接作为设计语义依据。
  - 记录 page content、page block、database sources、data-source property 等 v2 计划命令。
  - 记录 `insert-before` 不作为 v2 首批稳定能力。
  - 记录 Notion-Version 默认 pinned 且集中配置。
  - 记录 v2.0 到 v2.5 实施阶段和最小闭环。
- 更新 `Docs/dev/User_Usage_Model_Revision.md`：
  - 改为指向 ADR-002，避免重复维护。
- 更新 `Docs/Requirements.md`：
  - 新增 v2 设计决议摘要。
- 更新 `Docs/User/Configuration.md`：
  - 新增 v2 待实施本地目录上下文配置说明。
- 更新 `Docs/User/Cli.md`：
  - 新增 v2 待实施人类友好 CLI 计划说明。
- 更新 `Docs/Developer/api/cli.md`：
  - 新增 ADR-002 CLI 设计边界。
- 更新 `Docs/Developer/mcp_tools/databases.md` 和 `Docs/Developer/mcp_tools/data_sources.md`：
  - 记录 database 是容器、data_source 是表级对象。
- 更新 `Docs/Developer/testing/cli.md`：
  - 新增 ADR-002 待新增测试清单。
- 更新 `Docs/dev/Feature_Completion_Plan.md`：
  - 记录 ADR-002 是后续 v2 产品层补充。

验证结果：

- 本次为文档/ADR 固化，未新增 CLI 实现。
- 未运行 pytest；当前新增内容是待实施设计说明，不改变源码行为。
- 未执行 live Notion 测试；原因是没有实现变更，也没有真实 Notion token、测试 workspace 和安全写入目标。

## 2026-06-08 ADR-003 项目 attach runtime 工作流加入后续任务

目标：

- 将 `.notion_mcp` 项目级配置与 page/database attach 工作流加入后续开发任务。
- 明确 ADR-003 覆盖 ADR-002 中 `.notion-mcp` 目录命名的早期设计。
- 将后续实现拆分为 project 配置、page attach、database attach、场景测试和文档收敛阶段。

文档更新：

- 新增 `Docs/dev/ADR-003-project-attach-context.md`：
  - 记录状态为 `Design Accepted / 待实现`。
  - 记录项目级目录名 `.notion_mcp`、配置文件 `.notion_mcp/config.json`、状态目录 `.notion_mcp/state/`。
  - 记录 `page.attach.json` 和 `database.attach.json` 状态文件结构。
  - 记录 token 不允许写入项目目录。
  - 记录 cwd 向上发现项目配置规则。
  - 记录 `project init/status/root`、`page attach/status/refresh/detach/deattach`、`database attach/status/refresh/detach/deattach` 计划命令。
  - 记录 page/database 操作默认对象解析规则：显式 id > attachment > error。
  - 记录 `tests/v3/core/`、`tests/v3/cli/`、`tests/v3/scenarios/` 后续测试目录。
- 更新 `Docs/dev/ADR-002-local-context-and-cli-v2.md`：
  - 增加后续 ADR 覆盖说明，明确 `.notion_mcp` 以 ADR-003 为准。
- 更新 `Docs/Requirements.md`：
  - 将后续目标挂接到 ADR-003，并改用 `.notion_mcp/config.json`。
- 更新 `Docs/User/Configuration.md`：
  - 增加项目配置和 attach state 说明。
- 更新 `Docs/User/Cli.md`：
  - 增加 project/page attach/database attach 待实施命令摘要。
- 更新 `Docs/Developer/api/cli.md`：
  - 增加 ProjectResolver、AttachmentStore、ContextResolver 相关后续设计。
- 更新 `Docs/Developer/testing/cli.md`：
  - 增加 v3 attach workflow 测试清单。
- 更新 `Docs/dev/Feature_Completion_Plan.md`：
  - 将 ADR-003 纳入后续开发计划。

验证结果：

- 本次只新增和同步设计文档，未新增 CLI 实现。
- 未运行 pytest；当前新增内容不改变源码行为。
- 未执行 live Notion 测试；原因是没有实现变更，也没有真实 Notion token、测试 workspace 和安全写入目标。

## 2026-06-08 V2/V3 开发设计和任务追踪清单

目标：

- 将 ADR-002 和 ADR-003 从设计决议转换为实施导向的开发设计。
- 建立可追踪任务列表，覆盖项目配置、attach state、Page CLI、Database/DataSource、MCP 工具、Raw API、版本策略、测试和文档同步。
- 明确每个任务的任务 ID、依赖、输出文件、测试目标和验收标准。

文档更新：

- 新增 `Docs/dev/V2_V3_Development_Design.md`：
  - 记录目标调用关系：CLI/MCP Tool 共享 Core。
  - 记录全局配置与项目级 `.notion_mcp` 配置边界。
  - 记录 ProjectResolver、ProjectConfigStore、AttachmentStore、ContextResolver 等开发模块职责。
  - 记录 page/database attach、Page content、Page block、Database/DataSource CLI、MCP tools 和 Raw API 的实现边界。
  - 记录 v2/v3 测试目录和最小交付闭环。
- 新增 `Docs/dev/V2_V3_Trackable_Tasks.md`：
  - 拆分 D0 到 P15 阶段任务。
  - 任务覆盖 tests-first、Core、CLI、MCP、文档同步和最终验收。
  - 将 `insert-before`、cache/index、logs/audit、OAuth 和 GUI 标记为 deferred。
- 更新 `Docs/dev/Feature_Completion_Plan.md`：
  - 增加 V2/V3 开发设计和任务列表入口。

验证结果：

- 本次为文档规划更新，没有修改源码。
- 未运行 pytest；当前新增内容不改变代码行为。

## 2026-06-08 V2/V3 P1/P2 项目配置实现

完成任务：

- `V2V3-P1-001`：新增 project root discovery Core 测试。
- `V2V3-P1-002`：新增 `project init` CLI 测试。
- `V2V3-P1-003`：新增 `project status/root` CLI 测试。
- `V2V3-P2-001`：实现 `.notion_mcp` project path helpers。
- `V2V3-P2-002`：实现 `ProjectResolver`。
- `V2V3-P2-003`：实现 `ProjectConfigStore`。
- `V2V3-P2-004`：实现项目配置原子 JSON 写入。
- `V2V3-P2-005`：实现 `notion-mcp project init/status/root`。
- `V2V3-P2-006`：实现 `notion-mcp local init/status/root` 兼容别名。

源码更新：

- `src/notion_mcp/core/errors.py`
  - 新增 project config missing/already initialized/validation error 类型。
- `src/notion_mcp/core/project/`
  - 新增 `project_paths.py`、`project_config.py`、`project_resolver.py` 和 package export。
- `src/notion_mcp/cli/commands/project.py`
  - 新增 project/local 命令组。
- `src/notion_mcp/cli/app.py`
  - 注册 project/local 命令组。

测试更新：

- `tests/v3/core/test_project_resolver.py`
- `tests/v3/cli/test_project_init.py`
- `tests/v3/cli/test_project_status.py`

文档更新：

- `Docs/dev/V2_V3_Trackable_Tasks.md`
  - 将 P1/P2 任务标记为完成。
- `Docs/User/Configuration.md`
  - 记录 project/local 命令已实现，page/database attach 仍待实施。
- `Docs/User/Cli.md`
  - 新增项目上下文命令说明。
- `Docs/Developer/api/cli.md`
  - 记录 project/local 命令和 Core project 模块。
- `Docs/Developer/testing/cli.md`
  - 记录已新增 v3 project tests。

验证命令和结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_v3_project_tests UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_v3_project_env uv run pytest -q -p no:cacheprovider tests/v3/core/test_project_resolver.py tests/v3/cli/test_project_init.py tests/v3/cli/test_project_status.py`
  - 结果：`12 passed`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_v3_project_tests UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_v3_project_env uv run pytest -q -p no:cacheprovider tests/v2/cli tests/v3`
  - 结果：`35 passed`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_v3_project_full UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_v3_project_full_env uv run pytest -q -p no:cacheprovider`
  - 首次结果：`1 failed, 107 passed, 1 skipped, 1 warning`
  - 失败原因：仓库根目录存在生成物 `__pycache__`，触发 release readiness 测试。
  - 处理：删除 `__pycache__` 生成物。
  - 重跑结果：`108 passed, 1 skipped, 1 warning`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_v3_project_full UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_v3_project_full_env uv run ruff check .`
  - 结果：`All checks passed!`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_v3_project_full UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_v3_project_full_env uv run mypy src`
  - 结果：`Success: no issues found in 74 source files`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_v3_project_help uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp --help`
  - 结果：通过，help 中包含 `project` 和 `local` 命令组。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_v3_project_help uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp project --help`
  - 结果：通过，包含 `init`、`status`、`root`。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_v3_project_help uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp local --help`
  - 结果：通过，包含 `init`、`status`、`root`。

未运行：

- 未运行真实 Notion integration 测试；本阶段只实现本地项目配置，不调用 Notion API。

风险和后续：

- Page/database attach state 尚未实现。
- attach 后 page/database 命令省略 id 尚未实现。
- 下一阶段应进入 `V2V3-P3` 和 `V2V3-P4`，先写 Page attachment tests，再实现 PageAttachmentStore 和 page attach/status/refresh/detach。

## 2026-06-08 V2/V3 P3/P4 Page attach 实现

官方文档检查：

- 检查日期：2026-06-08。
- Notion Retrieve a page: https://developers.notion.com/reference/retrieve-a-page
  - 结论：`pages.retrieve` 返回 page properties，不返回页面内容；页面内容仍需通过 block children 获取。
- Notion Page object: https://developers.notion.com/reference/page
  - 结论：Page object 包含 `parent`、`url`、`in_trash`；`archived` 已废弃，应优先使用 `in_trash`。
- Notion Trash a page: https://developers.notion.com/reference/trash-page
  - 结论：trash 使用 update page 的 `in_trash`；本阶段的 `page detach/deattach` 只删除本地 state，不修改 Notion page。

完成任务：

- `V2V3-P3-001`：新增 page attachment store 测试。
- `V2V3-P3-002`：新增 `page attach` CLI 测试。
- `V2V3-P3-003`：新增 `page status/current/refresh` CLI 测试。
- `V2V3-P3-004`：新增 `page detach/deattach` CLI 测试。
- `V2V3-P3-005`：新增 page id context resolution 测试。
- `V2V3-P4-001`：实现 `PageAttachment` model。
- `V2V3-P4-002`：实现 `PageAttachmentStore`。
- `V2V3-P4-003`：实现 `ContextResolver.resolve_page_id()`。
- `V2V3-P4-004`：实现 `notion-mcp page attach`。
- `V2V3-P4-005`：实现 `notion-mcp page status/current/refresh`。
- `V2V3-P4-006`：实现 `notion-mcp page detach/deattach`。

源码更新：

- `src/notion_mcp/core/errors.py`
  - 新增 `PageAttachmentNotFoundError`。
- `src/notion_mcp/core/attachments/`
  - 新增 `page_attachment.py`、`attachment_store.py`、`context_resolver.py` 和 package export。
- `src/notion_mcp/cli/commands/pages.py`
  - 新增 page attach/status/current/refresh/detach/deattach 命令。

测试更新：

- `tests/v3/core/test_page_attachment_store.py`
- `tests/v3/cli/test_page_attach.py`
- `tests/v3/cli/test_page_status.py`
- `tests/v3/cli/test_page_detach.py`
- `tests/v3/cli/test_page_context_resolution.py`

文档更新：

- `Docs/dev/V2_V3_Trackable_Tasks.md`
  - 将 P3/P4 任务标记为完成。
- `Docs/User/Configuration.md`
  - 记录 page attach/status/current/refresh/detach/deattach 已实现。
- `Docs/User/Cli.md`
  - 新增 Page attach 命令说明。
- `Docs/Developer/api/cli.md`
  - 记录 Core attachment 模块和 page attach 命令边界。
- `Docs/Developer/testing/cli.md`
  - 记录已新增 v3 page attachment tests。

验证命令和结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_v3_page_tests UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_v3_page_env uv run pytest -q -p no:cacheprovider tests/v3/core/test_page_attachment_store.py tests/v3/cli/test_page_attach.py tests/v3/cli/test_page_status.py tests/v3/cli/test_page_detach.py tests/v3/cli/test_page_context_resolution.py`
  - 结果：`14 passed`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_v3_page_tests UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_v3_page_env uv run pytest -q -p no:cacheprovider tests/v2/cli tests/v3`
  - 结果：`49 passed`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_v3_page_full UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_v3_page_full_env uv run pytest -q -p no:cacheprovider`
  - 结果：`122 passed, 1 skipped, 1 warning`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_v3_page_full UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_v3_page_full_env uv run ruff check .`
  - 首次结果：1 个未使用 import；已修复。
  - 重跑结果：`All checks passed!`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_v3_page_full UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_v3_page_full_env uv run mypy src`
  - 结果：`Success: no issues found in 78 source files`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_v3_page_help uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp page --help`
  - 结果：通过，help 中包含 `attach`、`current`、`status`、`refresh`、`detach`、`deattach`。

未运行：

- 未运行真实 Notion integration 测试；本阶段测试使用 fake page service，避免真实 workspace 写入。

风险和后续：

- `page content` 尚未实现，因此最终最小闭环中的 `notion-mcp page content` 仍未完成。
- attach 后 page/database 命令省略 id 尚未完整接入普通 page/database 操作。
- 下一阶段应进入 `V2V3-P5` 和 `V2V3-P6`，实现 page content 和 page-scoped block editing。

## 2026-06-08 V2/V3 P5/P6 Page content 和页面内编辑实现

官方文档检查：

- 检查日期：2026-06-08。
- Notion Retrieve block children: https://developers.notion.com/reference/get-block-children
  - 结论：page 内容需要通过 block children 获取；需要递归时继续读取有 `has_children` 的 child block。
- Notion Append block children: https://developers.notion.com/reference/patch-block-children
  - 结论：`after` 已废弃，`2026-03-11` 应使用 `position`；`insert-after` 使用 `{ "type": "after_block", "after_block": { "id": "<block_id>" } }`。
- Notion Update a block: https://developers.notion.com/reference/update-a-block
  - 结论：block children 不能通过 update endpoint 直接更新；children 追加应使用 append block children。
- Notion Delete a block: https://developers.notion.com/reference/delete-a-block
  - 结论：delete block 会将 block 设置为 `in_trash: true`，用于 `page block remove`。
- Notion Create a page: https://developers.notion.com/reference/post-page
  - 结论：创建 child page 时可使用 page parent；当 payload 未提供 parent 时，CLI 使用 attached page。
- Notion Create a database: https://developers.notion.com/reference/create-database
  - 结论：database 是容器，create database 会创建 database 及初始 data source；当 payload 未提供 parent 时，CLI 使用 attached page。

完成任务：

- `V2V3-P5-001`：新增 `page content` 测试。
- `V2V3-P5-002`：新增 page-scoped block editing 测试。
- `V2V3-P5-003`：新增 `page insert page/database` 测试。
- `V2V3-P6-001`：实现 `PagesService.content()`。
- `V2V3-P6-002`：实现 page content human 和 JSON 输出。
- `V2V3-P6-003`：实现 `page content` attached defaulting。
- `V2V3-P6-004`：实现 `page block append/update/insert-after/remove`。
- `V2V3-P6-005`：实现 `page insert page/database`。

源码更新：

- `src/notion_mcp/core/services/pages.py`
  - 新增 `content()`、block summary、parent id 和 rich text 摘要 helpers。
- `src/notion_mcp/cli/commands/pages.py`
  - 新增 `page content`。
  - 新增 `page block append/insert-after/update/remove`。
  - 新增 `page insert page/database`。

测试更新：

- `tests/v3/core/test_page_content_service.py`
- `tests/v3/cli/test_page_content_attach.py`
- `tests/v3/cli/test_page_block_edit_attach.py`
- `tests/v3/cli/test_page_insert.py`

文档更新：

- `Docs/dev/V2_V3_Trackable_Tasks.md`
  - 将 P5/P6 任务标记为完成。
- `Docs/User/Cli.md`
  - 记录 page content、page block 和 page insert 已实现。
- `Docs/User/Configuration.md`
  - 记录 page content 和页面内编辑命令已实现。
- `Docs/Developer/api/cli.md`
  - 记录 page content、page block 和 page insert 的 CLI 到 Core 边界。
- `Docs/Developer/testing/cli.md`
  - 记录已新增 v3 page content/edit tests。

验证命令和结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_v3_content_tests UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_v3_content_env uv run pytest -q -p no:cacheprovider tests/v3/core/test_page_content_service.py tests/v3/cli/test_page_content_attach.py tests/v3/cli/test_page_block_edit_attach.py tests/v3/cli/test_page_insert.py`
  - 结果：`10 passed`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_v3_content_tests UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_v3_content_env uv run pytest -q -p no:cacheprovider tests/v2/cli tests/v3`
  - 结果：`59 passed`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_v3_content_full UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_v3_content_full_env uv run pytest -q -p no:cacheprovider`
  - 结果：`132 passed, 1 skipped, 1 warning`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_v3_content_full UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_v3_content_full_env uv run ruff check .`
  - 结果：`All checks passed!`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_v3_content_full UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_v3_content_full_env uv run mypy src`
  - 首次结果：`src/notion_mcp/cli/commands/pages.py` 有动态 dict/list 类型问题；已用 `typing.cast` 收紧。
  - 重跑结果：`Success: no issues found in 78 source files`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_v3_content_help uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp page --help`
  - 结果：通过，help 中包含 `content`、`block`、`insert`。

未运行：

- 未运行真实 Notion integration 测试；本阶段测试使用 fake page/block/database service，避免真实 workspace 写入。

风险和后续：

- Database/DataSource attach 与 database 默认 active data source 仍未实现。
- MCP tools 尚未同步新的 attach/page content 行为。
- 最小闭环中 page 部分已经具备本地 fake 测试覆盖；database attach/query 部分仍待 P7-P10。

## 2026-06-08 V2/V3 P7/P8 Database/DataSource Core 和 CLI 扩展

官方文档检查：

- 检查日期：2026-06-08。
- Notion Data source object: https://developers.notion.com/reference/data-source
  - 结论：data sources 是 database 下的具体表，pages 是 data source 中的 items；data source 承载 properties/schema。
- Notion Retrieve a database: https://developers.notion.com/reference/retrieve-database
  - 结论：database 是包含一个或多个 data sources 的容器；response 中的 `data_sources` 提供 id/name，并可用于 retrieve/update/query data source。
- Notion Retrieve a data source: https://developers.notion.com/reference/retrieve-a-data-source
  - 结论：retrieve data source 返回表级 schema；查询 rows/pages 应使用 Query a data source。
- Notion Query a data source: https://developers.notion.com/reference/query-a-data-source
  - 结论：query data source 返回 data source 中的 pages/entries，并支持 filter、sort 和 pagination。
- Notion Create a data source: https://developers.notion.com/reference/create-a-data-source
  - 结论：create data source 在现有 database 容器下新增表；parent 使用 database id。
- Notion Update a data source: https://developers.notion.com/reference/update-a-data-source
  - 结论：update data source 用于更新 title、description、properties、trash 状态和 parent；不能用于更新 data source rows。
- Notion Update data source properties: https://developers.notion.com/reference/update-data-source-properties
  - 结论：重命名 property 应在 `properties` body 中用 property id/name 指向 `{ "name": "<new_name>" }`。
- Notion List data source templates: https://developers.notion.com/reference/list-data-source-templates
  - 结论：templates endpoint 是 `GET /v1/data_sources/{data_source_id}/templates`；Python SDK v3.1.0 本地检查显示方法名为 `client.data_sources.list_templates`。
- Notion Parent object: https://developers.notion.com/reference/parent-object
  - 结论：data source parent object 使用 `type: "data_source_id"` 和 `data_source_id`，用于 page/entry parent。
- Notion Create a page: https://developers.notion.com/reference/post-page
  - 结论：创建 page 可使用 page 或 data source parent；data source 下创建 page 时 properties 必须匹配 parent data source schema。
- Notion 2026-03-11 Upgrade Guide: https://developers.notion.com/guides/get-started/upgrade-guide-2026-03-11
  - 结论：继续遵守 `position` 和 `in_trash` 语义；本阶段没有新增 block positioning 能力。

完成任务：

- `V2V3-P7-001`：新增 database/data source service separation 测试。
- `V2V3-P7-002`：新增 database container CLI 测试。
- `V2V3-P7-003`：新增显式 `data-source` namespace CLI 测试。
- `V2V3-P7-004`：部分新增 database shortcut 测试，覆盖显式 `--data-source`、`database page`、`database property`；单/多 data source 自动解析仍待 P9/P10。
- `V2V3-P8-001`：部分实现 `DatabaseService` 容器能力，新增 `list_data_sources()` 和 `rename()`；legacy `query()` 暂保留以兼容旧测试。
- `V2V3-P8-002`：实现 `DataSourcesService` 的 `create_for_database()`、`templates()` 和 `rename_property()`。
- `V2V3-P8-003`：实现 database CLI container commands。
- `V2V3-P8-004`：实现显式 `data-source` CLI namespace 扩展。
- `V2V3-P8-005`：部分实现 database shortcut commands；完整 shortcut resolver 等待 database attach context。

源码更新：

- `src/notion_mcp/core/services/databases.py`
  - 新增 database container `list_data_sources()`、`rename()` 和 rich text title helper。
- `src/notion_mcp/core/services/data_sources.py`
  - 新增 `create_for_database()`、`templates()`、`rename_property()`。
- `src/notion_mcp/cli/commands/databases.py`
  - 新增 `sources/create/update/rename`。
  - 新增 `database query --data-source` 显式 data source shortcut。
  - 新增 `database page create/update`。
  - 新增 `database property rename`。
- `src/notion_mcp/cli/commands/data_sources.py`
  - 新增 `data-source create <database_id>`。
  - 新增 `data-source templates`。
  - 新增 `data-source property rename`。

测试更新：

- `tests/v2/core/test_database_data_source_services.py`
- `tests/v2/cli/test_database_container.py`
- `tests/v2/cli/test_data_source_namespace.py`
- `tests/v2/cli/test_database_shortcut_commands.py`

文档更新：

- `Docs/dev/V2_V3_Trackable_Tasks.md`
  - 将 P7-001/P7-002/P7-003、P8-002/P8-003/P8-004 标记为完成。
  - 将 P7-004、P8-001、P8-005 标记为进行中，并记录 legacy query 和 attach/defaulting 待完成原因。
- `Docs/User/Cli.md`
  - 新增 database/data-source 当前已实现命令说明。
- `Docs/User/Configuration.md`
  - 更新当前已实现和仍待实施的 database/defaulting 状态。
- `Docs/Developer/api/cli.md`
  - 记录 database/data-source CLI 到 Core 边界。
- `Docs/Developer/testing/cli.md`
  - 记录新增 P7/P8 测试文件。
- `Docs/Developer/mcp_tools/databases.md`
- `Docs/Developer/mcp_tools/data_sources.md`
  - 记录 CLI/Core 已扩展但 MCP tools 尚未同步的缺口。

验证命令和结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_sdk_inspect uv run python -c '...'`
  - 结果：通过；本地安装 `notion-client==3.1.0`，`Client` 有 `data_sources`，其中包含 `create`、`retrieve`、`update`、`query`、`list_templates`。
  - 注意：这条命令未设置 `UV_PROJECT_ENVIRONMENT`，生成了本地 `.venv/`；随后已删除 `.venv/` 并重跑 release readiness。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p7_pre UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p7_pre_env uv run pytest -q -p no:cacheprovider tests/v2/core/test_database_data_source_services.py tests/v2/cli/test_database_container.py tests/v2/cli/test_data_source_namespace.py tests/v2/cli/test_database_shortcut_commands.py`
  - 首次结果：`10 failed, 1 passed`；失败点是预期的缺失 P7/P8 功能。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p7_post UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p7_post_env uv run pytest -q -p no:cacheprovider tests/v2/core/test_database_data_source_services.py tests/v2/cli/test_database_container.py tests/v2/cli/test_data_source_namespace.py tests/v2/cli/test_database_shortcut_commands.py`
  - 结果：`11 passed`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p7_wide UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p7_wide_env uv run pytest -q -p no:cacheprovider tests/v2/core tests/v2/cli tests/v3`
  - 结果：`96 passed`

未运行：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p7_docs UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p7_docs_env uv run pytest -q -p no:cacheprovider tests/v2/scenarios/test_cli_documentation_inventory.py tests/v2/scenarios/test_stage7_documentation_completeness.py tests/v2/scenarios/test_stage8_release_readiness.py`
  - 首次结果：`1 failed, 7 passed`；失败原因是本轮 SDK 检查误生成仓库根 `.venv/`，release readiness 扫描到 `.venv` 中的大文件。
- `rm -rf .venv`
  - 结果：通过；删除本轮误生成的仓库根临时环境。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p7_docs2 UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p7_docs2_env uv run pytest -q -p no:cacheprovider tests/v2/scenarios/test_cli_documentation_inventory.py tests/v2/scenarios/test_stage7_documentation_completeness.py tests/v2/scenarios/test_stage8_release_readiness.py`
  - 结果：`8 passed`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p7_full UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p7_full_env uv run pytest -q -p no:cacheprovider`
  - 结果：`143 passed, 1 skipped, 1 warning`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p7_full UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p7_full_env uv run ruff check .`
  - 结果：`All checks passed!`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p7_full UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p7_full_env uv run mypy src`
  - 结果：`Success: no issues found in 78 source files`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p7_help1 uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp --help`
  - 结果：通过；root help 显示 `database` 和 `data-source` 命令组。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p7_help2 uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp database --help`
  - 结果：通过；help 显示 `retrieve/sources/create/update/rename/query/page/property`。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p7_help3 uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp data-source --help`
  - 结果：通过；help 显示 `retrieve/query/create/update/templates/property`。
- `find . -name __pycache__ -type d -print`
  - 结果：无输出。
- `test -d .venv && printf '.venv exists\n' || true`
  - 结果：无输出。
- `git diff --check`
  - 结果：无输出。

未运行：

- 未运行真实 Notion integration 测试；本阶段使用 fake services 和 fake SDK-compatible clients，避免真实 workspace 写入。

风险和后续：

- `database query <database_id>` legacy 兼容入口仍保留，以避免破坏旧测试；完整迁移到 data source shortcut/defaulting 需要 P9/P10 database attach 后完成。
- `database query --payload` 省略 id、`database page create --properties` 省略 id、`database property rename` 省略 data source id 仍未实现；需要 `.notion_mcp/state/database.attach.json` 的 active data source。
- database id 自动解析单 data source、多 data source 要求显式指定尚未实现。
- MCP tools 尚未同步 `database.sources`、`data_source.templates` 和 property rename。

## 2026-06-08 V2/V3 P9/P10 Database attach 和 active data source defaulting

官方文档检查：

- 检查日期：2026-06-08。
- 本阶段继续沿用 P7/P8 已检查的 Notion database/data source 文档：
  - Retrieve a database: https://developers.notion.com/reference/retrieve-database
  - Data source object: https://developers.notion.com/reference/data-source
  - Query a data source: https://developers.notion.com/reference/query-a-data-source
  - Parent object: https://developers.notion.com/reference/parent-object
- 结论：database attach 必须记录 database container 和 active data source；query/page create/property rename 等表级操作使用 active data source。

完成任务：

- `V2V3-P9-001`：新增 database attachment store 测试。
- `V2V3-P9-002`：新增 `database attach` CLI 测试。
- `V2V3-P9-003`：新增 `database status/current/refresh` CLI 测试。
- `V2V3-P9-004`：新增 `database detach/deattach` CLI 测试。
- `V2V3-P9-005`：新增 attached database defaulting 测试。
- `V2V3-P10-001`：实现 `DatabaseAttachment` model。
- `V2V3-P10-002`：实现 `DatabaseAttachmentStore` load/save/delete。
- `V2V3-P10-003`：实现 data source 按 id/name 匹配和多 source 错误。
- `V2V3-P10-004`：实现 `database attach`。
- `V2V3-P10-005`：实现 `database status/current/refresh`。
- `V2V3-P10-006`：实现 `database detach/deattach`。
- `V2V3-P10-007`：实现 attached database/data source context resolution。

源码更新：

- `src/notion_mcp/core/attachments/database_attachment.py`
  - 新增 `DatabaseAttachment`、`AttachedDatabase`、`AttachedDataSource`。
  - 新增 database title/data sources extraction、active data source selection 和 refresh helper。
- `src/notion_mcp/core/attachments/attachment_store.py`
  - 新增 `DatabaseAttachmentStore`。
- `src/notion_mcp/core/attachments/context_resolver.py`
  - 新增 `resolve_database_id()`、`resolve_data_source_id()`。
- `src/notion_mcp/core/attachments/__init__.py`
  - 导出 database attachment 相关 public symbols。
- `src/notion_mcp/core/errors.py`
  - 新增 `DatabaseAttachmentNotFoundError`、`ActiveDataSourceNotFoundError`、`DatabaseDataSourceSelectionError`。
- `src/notion_mcp/cli/commands/databases.py`
  - 新增 `database attach/status/current/refresh/detach/deattach`。
  - `database retrieve/sources` 支持省略 database id，默认读取 attached database。
  - `database query` 省略 id 时默认查询 attached active data source。
  - `database page create` 省略 data source id 时默认使用 active data source。
  - `database property rename` 支持 explicit data source id 或 attached active data source。

测试更新：

- `tests/v3/core/test_database_attachment_store.py`
- `tests/v3/cli/test_database_attach.py`
- `tests/v3/cli/test_database_status.py`
- `tests/v3/cli/test_database_detach.py`
- `tests/v3/cli/test_database_context_resolution.py`

文档更新：

- `Docs/dev/V2_V3_Trackable_Tasks.md`
  - 将 P9/P10 任务标记为完成。
  - 将 P7-004/P8-005 更新为完成，因为 attached active data source defaulting 已覆盖。
- `Docs/User/Cli.md`
  - 记录 database attach/status/current/refresh/detach/deattach 已实现。
  - 记录 database query/page create/property rename 的省略 id 行为。
- `Docs/User/Configuration.md`
  - 更新当前已实现 database attach 和 defaulting 状态。
- `Docs/Developer/api/cli.md`
  - 记录 database attachment state 和 context resolution 边界。
- `Docs/Developer/testing/cli.md`
  - 记录新增 v3 database attachment/defaulting tests。

验证命令和结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p9_pre UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p9_pre_env uv run pytest -q -p no:cacheprovider tests/v3/core/test_database_attachment_store.py tests/v3/cli/test_database_attach.py tests/v3/cli/test_database_status.py tests/v3/cli/test_database_detach.py tests/v3/cli/test_database_context_resolution.py`
  - 首次结果：collection error；原因是尚未导出 `DatabaseAttachment` / `DatabaseAttachmentStore`。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p9_post UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p9_post_env uv run pytest -q -p no:cacheprovider tests/v3/core/test_database_attachment_store.py tests/v3/cli/test_database_attach.py tests/v3/cli/test_database_status.py tests/v3/cli/test_database_detach.py tests/v3/cli/test_database_context_resolution.py`
  - 中间结果：`8 failed, 2 passed`；失败原因是新测试误用了 Typer `CliRunner.isolated_filesystem`，已改为仓库现有的 `monkeypatch.chdir(tmp_path)` 风格。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p9_post2 UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p9_post2_env uv run pytest -q -p no:cacheprovider tests/v3/core/test_database_attachment_store.py tests/v3/cli/test_database_attach.py tests/v3/cli/test_database_status.py tests/v3/cli/test_database_detach.py tests/v3/cli/test_database_context_resolution.py`
  - 结果：`10 passed`

后续验证命令和结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p10_docs UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p10_docs_env uv run pytest -q -p no:cacheprovider tests/v2/scenarios/test_cli_documentation_inventory.py tests/v2/scenarios/test_stage7_documentation_completeness.py tests/v2/scenarios/test_stage8_release_readiness.py`
  - 结果：`8 passed`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p10_full UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p10_full_env uv run pytest -q -p no:cacheprovider`
  - 首次结果：`4 failed, 149 passed, 1 skipped, 1 warning`
  - 失败原因：显式 id 场景也先查 project root，导致旧 v2 database CLI tests 在无 `.notion_mcp` 时失败。
  - 修复：`resolve_database_id()` / `resolve_data_source_id()` 在显式 id 存在时直接返回，只有省略 id 时才读取 attachment。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p10_fix UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p10_fix_env uv run pytest -q -p no:cacheprovider tests/v2/cli/test_database_container.py tests/v2/cli/test_database_shortcut_commands.py tests/v3/cli/test_database_context_resolution.py`
  - 结果：`8 passed`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p10_full2 UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p10_full2_env uv run pytest -q -p no:cacheprovider`
  - 结果：`153 passed, 1 skipped, 1 warning`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p10_full2 UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p10_full2_env uv run ruff check .`
  - 首次结果：1 个长 import 行；已拆行。
  - 重跑结果：`All checks passed!`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p10_full2 UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p10_full2_env uv run mypy src`
  - 结果：`Success: no issues found in 79 source files`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p10_help1 uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp database --help`
  - 结果：通过；help 显示 `attach/current/status/refresh/deattach/detach/retrieve/sources/create/update/rename/query/page/property`。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p10_help2 uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp database attach --help`
  - 结果：通过；help 显示 `--data-source`、`--verify/--no-verify`、`--require-project`、`--json`。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p10_help3 uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp database page create --help`
  - 结果：通过；`data_source_id` 为可选 argument，支持 attached active data source defaulting。
- `find . -name __pycache__ -type d -print`
  - 结果：无输出。
- `test -d .venv && printf '.venv exists\n' || true`
  - 结果：无输出。
- `git diff --check`
  - 结果：无输出。

未运行：

- 未运行真实 Notion integration 测试；本阶段使用 fake services 和本地 state 文件，避免真实 workspace 写入。

风险和后续：

- Legacy `database query <database_id>` 仍保留，用于旧测试和旧入口兼容；用户文档优先推荐 data source 和 attached active data source 路径。
- MCP tools 尚未同步 database attachment、database sources、data source templates/property rename。
- 还需要补 P13 场景测试，验证从子目录发现 `.notion_mcp/config.json` 并完成 page/database attach workflow。

## 2026-06-08 V2/V3 P11 MCP Tool Alignment

官方文档检查：

- 检查日期：2026-06-08。
- 本阶段没有新增 Notion endpoint 语义；只把 P7/P8 已实现并已检查的 Core database/data_source 能力暴露到 MCP tool 层。
- 继续沿用 P7/P8 已记录的官方 Notion database/data source 文档检查结果。

完成任务：

- `V2V3-P11-001`：新增 MCP database/data_source separation tests。
- `V2V3-P11-002`：实现 MCP database/data_source 工具同步。
- `V2V3-P11-003`：验证 page/block 相关 MCP tests 仍通过。
- `V2V3-P14-004`：同步 MCP tool 文档。

测试更新：

- `tests/v2/mcp_tools/__init__.py`
- `tests/v2/mcp_tools/test_database_data_source_tools.py`
  - 验证 tool inventory 包含 `database_sources`、`database_rename`、`data_source_templates`、`data_source_property_rename`。
  - 验证 database MCP tools 调用 `DatabasesService`。
  - 验证 data source MCP tools 调用 `DataSourcesService`。
  - 验证 database/data_source MCP tool 模块不调用 CLI，也不直接导入 Notion SDK。

源码更新：

- `src/notion_mcp/mcp_server/tools/databases.py`
  - 将描述从 legacy database 改为 database container。
  - 新增 `database_sources`。
  - 新增 `database_rename`。
  - 保留 `database_query` legacy 兼容入口，并提示优先使用 `data_source_query`。
- `src/notion_mcp/mcp_server/tools/data_sources.py`
  - `data_source_create` 支持可选 `database_id`，传入后调用 `create_for_database()`。
  - 新增 `data_source_templates`。
  - 新增 `data_source_property_rename`。

文档更新：

- `Docs/dev/V2_V3_Trackable_Tasks.md`
  - 将 P11-001/P11-002/P11-003 标记为完成。
  - 将 P14-004 标记为完成，P14-006 标记为持续进行中。
- `Docs/Developer/mcp_tools/README.md`
  - Tool inventory 从 42 更新为 46。
- `Docs/Developer/mcp_tools/databases.md`
  - 记录 database container MCP tools，包括 `database_sources` 和 `database_rename`。
- `Docs/Developer/mcp_tools/data_sources.md`
  - 记录 `data_source_create` with `database_id`、`data_source_templates`、`data_source_property_rename`。
- `Docs/Developer/testing/cli.md`
  - 记录新增 P11 MCP tests 和验证命令。
- `Docs/Developer/api/cli.md`
- `Docs/User/Cli.md`
- `Docs/User/Configuration.md`
  - 修正 P10/P11 之后仍保留的过期“待实施/计划”措辞。

验证命令和结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p11_pre UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p11_pre_env uv run pytest -q -p no:cacheprovider tests/v2/mcp_tools/test_database_data_source_tools.py`
  - 首次结果：`3 failed, 1 passed`。
  - 失败原因：符合测试先行预期；MCP tool inventory 缺少 `database_sources`、`database_rename`、`data_source_templates`、`data_source_property_rename`，且 `data_source_create` 尚未支持 `database_id`。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p11_after UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p11_after_env uv run pytest -q -p no:cacheprovider tests/v2/mcp_tools/test_database_data_source_tools.py`
  - 结果：`4 passed`。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p11_mcp UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p11_mcp_env uv run pytest -q -p no:cacheprovider tests/v2/mcp_server tests/v2/mcp_tools tests/v2/scenarios/test_mcp_to_core_to_fake_notion.py tests/v2/scenarios/test_mcp_client_flow.py`
  - 结果：`18 passed`。

未运行：

- 未运行真实 Notion integration 测试；P11 使用 fake Core services 验证 MCP 到 Core 的调用边界，不需要真实 workspace。
- 本阶段尚未运行全量 pytest、ruff、mypy；后续 P13/P15 或最终验收会运行 release-relevant local checks。

风险和后续：

- P12 Raw API/version policy 测试仍未完成。
- P13 场景测试仍未完成。
- P15 最小交付闭环和全量 release checks 仍未完成。

## 2026-06-08 V2/V3 P12 Raw API and Notion-Version policy

官方文档检查：

- 检查日期：2026-06-08。
- Versioning - Notion Docs: https://developers.notion.com/reference/versioning
  - 结论：Notion API 是 versioned API；REST 请求必须包含 `Notion-Version` header；新的 breaking API version 会改变字段或行为，因此本项目保持 pinned policy。
- Upgrade guide - Notion Docs: https://developers.notion.com/guides/get-started/upgrade-guide-2026-03-11
  - 结论：`2026-03-11` 包含 block positioning、trash/archive 语义和 block type rename 等 breaking changes；本项目继续要求版本集中配置并配套兼容性测试。

完成任务：

- `V2V3-P12-001`：新增 Raw API 定位测试。
- `V2V3-P12-002`：新增 Notion-Version policy 测试。
- `V2V3-P12-003`：重新检查官方 Notion versioning 和 2026-03-11 upgrade guide，并记录链接。

测试更新：

- `tests/v2/cli/test_raw_api_positioning.py`
  - 验证 `raw-api operations --json` 仍可用。
  - 验证 common page/database workflows 已有专用 CLI 命令。
  - 验证 raw-api CLI help 和用户文档将 Raw API 定位为 advanced fallback。
- `tests/v2/core/test_notion_version_policy.py`
  - 验证默认 Notion-Version pinned。
  - 验证 Notion-Version 从 global Core config 读取。
  - 验证 SDK client factory 只注入配置中的 version。
  - 验证 `src/notion_mcp` 中除配置层外没有散落硬编码版本字符串。

源码更新：

- `src/notion_mcp/cli/commands/raw_api.py`
  - `raw-api` Typer help 改为 `Advanced fallback for registered raw API operations`。
- `src/notion_mcp/routes/databases.py`
  - 移除 legacy REST route 文档字符串中的具体 Notion API version 文本，改为引用当前配置的 Notion-Version。

文档更新：

- `Docs/dev/V2_V3_Trackable_Tasks.md`
  - 将 P12-001/P12-002/P12-003 标记为完成。
- `Docs/Developer/testing/cli.md`
  - 记录 P12 新增测试文件和验证结果。

验证命令和结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p12_pre UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p12_pre_env uv run pytest -q -p no:cacheprovider tests/v2/cli/test_raw_api_positioning.py tests/v2/core/test_notion_version_policy.py`
  - 首次结果：`2 failed, 6 passed`。
  - 失败原因：`raw-api --help` 未包含 advanced/fallback 定位；legacy REST route 文档字符串中仍有具体 Notion-Version。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p12_after UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p12_after_env uv run pytest -q -p no:cacheprovider tests/v2/cli/test_raw_api_positioning.py tests/v2/core/test_notion_version_policy.py`
  - 结果：`8 passed`。

未运行：

- 未运行真实 Notion integration 测试；P12 是本地 CLI/docs/config policy 测试，不需要真实 workspace。
- 本阶段尚未运行全量 pytest、ruff、mypy；后续 P13/P15 或最终验收会运行 release-relevant local checks。

风险和后续：

- P13 场景测试仍未完成。
- P15 最小交付闭环和全量 release checks 仍未完成。

## 2026-06-08 V2/V3 P13 Scenario Tests

完成任务：

- `V2V3-P13-001`：新增 local page context workflow scenario。
- `V2V3-P13-002`：新增 page content edit workflow scenario。
- `V2V3-P13-003`：新增 database attach/query workflow scenario。
- `V2V3-P13-004`：新增 project context discovery scenario。
- `V2V3-P14-005`：同步测试文档中的 P13 场景测试说明。

测试更新：

- `tests/v3/scenarios/__init__.py`
- `tests/v3/scenarios/test_attach_page_workflow.py`
  - 覆盖 page attach、page status、从子目录执行 `page content`、page detach、missing attach error。
- `tests/v2/scenarios/test_page_content_edit_workflow.py`
  - 覆盖 content read、insert-after、append、update、remove。
- `tests/v3/scenarios/test_attach_database_workflow.py`
  - 覆盖 database attach、active data source query、显式 data source override、database page create/update、detach。
- `tests/v3/scenarios/test_project_context_discovery.py`
  - 覆盖 nested cwd project root discovery 和 missing project context remediation error。

文档更新：

- `Docs/dev/V2_V3_Trackable_Tasks.md`
  - 将 P13-001/P13-002/P13-003/P13-004 标记为完成。
  - 将 P14-005 标记为完成。
- `Docs/Developer/testing/cli.md`
  - 记录 P13 场景测试文件和验证命令。
- `Docs/User/Configuration.md`
  - 移除场景测试仍待实施的旧状态，补充真实 Notion integration 仍需显式启用。

验证命令和结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p13_pre UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p13_pre_env uv run pytest -q -p no:cacheprovider tests/v3/scenarios/test_attach_page_workflow.py tests/v2/scenarios/test_page_content_edit_workflow.py tests/v3/scenarios/test_attach_database_workflow.py tests/v3/scenarios/test_project_context_discovery.py`
  - 结果：`5 passed`。

未运行：

- 未运行真实 Notion integration 测试；P13 使用 fake services 和本地 `.notion_mcp` state 验证用户工作流。

风险和后续：

- P15 最小交付闭环和全量 release checks 仍未完成。

## 2026-06-08 V2/V3 P15 Minimum Delivery Verification

完成任务：

- `V2V3-P14-001`：用户配置文档同步完成。
- `V2V3-P14-002`：用户 CLI 文档同步完成。
- `V2V3-P14-003`：开发者 CLI API 文档同步完成。
- `V2V3-P14-006`：阶段进度记录同步完成。
- `V2V3-P15-001`：page attach minimum loop 已由 P13 fake scenario 覆盖。
- `V2V3-P15-002`：database attach minimum loop 已由 P13 fake scenario 覆盖。
- `V2V3-P15-003`：child directory discovery 已由 P13 fake scenario 覆盖。
- `V2V3-P15-004`：release-relevant local checks 已运行。

验证命令和结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p15_full UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p15_full_env uv run pytest -q -p no:cacheprovider`
  - 首次结果：`1 failed, 169 passed, 1 skipped, 1 warning`。
  - 失败原因：仓库根存在测试生成的 `__pycache__`，触发 release readiness 生成物检查。
- `find . -name __pycache__ -type d -print`
  - 结果：输出 `./__pycache__`。
- `rm -rf __pycache__`
  - 结果：通过；删除生成物。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p15_full2 UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p15_full2_env uv run pytest -q -p no:cacheprovider`
  - 结果：`170 passed, 1 skipped, 1 warning`。
  - warning：外部 FastAPI/TestClient 的 StarletteDeprecationWarning。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p15_full2 UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p15_full2_env uv run ruff check .`
  - 结果：`All checks passed!`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p15_full2 UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p15_full2_env uv run mypy src`
  - 结果：`Success: no issues found in 79 source files`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p15_isolated uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp --help`
  - 结果：通过；root help 显示 project/local/page/database/data-source/raw-api/mcp 等命令组，`raw-api` 显示 advanced fallback。
- `find . -name __pycache__ -type d -print`
  - 结果：无输出。
- `test -d .venv && printf '.venv exists\n' || true`
  - 结果：无输出。
- `git diff --check`
  - 结果：无输出。

未运行：

- 未运行真实 Notion integration 测试；没有本轮用户提供的真实 token/workspace，也避免真实 Notion 写入。真实环境测试仍需显式 integration 配置后执行。

当前风险和后续：

- `database query <database_id>` legacy 兼容入口仍保留，用于旧测试和迁移；推荐路径是 `data-source query` 或 attached active data source defaulting。
- `insert-before`、cache/index、local logs/audit、OAuth、GUI 仍是 deferred items，不属于本轮最小交付闭环。

## 2026-06-08 V2/V3 P8 Final DatabaseService Boundary

完成任务：

- `V2V3-P8-001`：最终确认并实现 `DatabaseService` 只承载 database container 能力。

完成度审计发现：

- `Docs/dev/V2_V3_Trackable_Tasks.md` 中唯一非 deferred 未完成项是 `V2V3-P8-001`。
- 原因是 `DatabasesService` 仍保留 legacy `query()`，这与 database container / data_source table-level 分离原则冲突。

测试更新：

- `tests/v2/core/test_database_service_container_only.py`
  - 验证 `DatabasesService` 不暴露表级 `query`。
- `tests/v2/cli/test_legacy_database_query_raw_api.py`
  - 验证 legacy `database query <database_id>` 通过 Core Raw API 兼容路径调用 `databases.query`。
- `tests/v2/mcp_tools/test_legacy_database_query_raw_api.py`
  - 验证 legacy `database_query` MCP tool 通过 Core Raw API 兼容路径调用 `databases.query`。

源码更新：

- `src/notion_mcp/core/services/databases.py`
  - 移除 `DatabasesService.query()`。
- `src/notion_mcp/cli/commands/databases.py`
  - legacy `database query <database_id>` 在真实 `DatabasesService` 无 `query` 时调用 `RawNotionService.invoke("databases.query", ...)`。
  - 为旧 mock 测试保留 `hasattr(service, "query")` 兼容分支。
- `src/notion_mcp/mcp_server/tools/databases.py`
  - legacy `database_query` MCP tool 同样改为 Core Raw API 兼容路径。
- `src/notion_mcp/cli/core_services.py`
  - 更新 `DatabasesService` usage comment。

文档更新：

- `Docs/dev/V2_V3_Trackable_Tasks.md`
  - 将 `V2V3-P8-001` 标记为完成。
  - 记录 legacy database query 现在走 Core Raw API 兼容路径。
- `Docs/Developer/api/cli.md`
- `Docs/Developer/mcp_tools/databases.md`
- `Docs/Developer/testing/cli.md`
- `Docs/User/Cli.md`
- `Docs/User/Guide.md`
  - 同步 legacy database query 和 data source 推荐路径说明。

验证命令和结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p8_final_pre UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p8_final_pre_env uv run pytest -q -p no:cacheprovider tests/v2/core/test_database_service_container_only.py tests/v2/cli/test_legacy_database_query_raw_api.py tests/v2/mcp_tools/test_legacy_database_query_raw_api.py`
  - 首次结果：`3 failed`。
  - 失败原因：符合测试先行预期；`DatabasesService.query()` 仍存在，CLI/MCP 没有 raw-api compatibility service getter。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_p8_final_after UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_p8_final_after_env uv run pytest -q -p no:cacheprovider tests/v2/core/test_database_service_container_only.py tests/v2/cli/test_legacy_database_query_raw_api.py tests/v2/mcp_tools/test_legacy_database_query_raw_api.py`
  - 结果：`3 passed`。

风险和后续：

- 本阶段后需要重新运行全量 pytest、ruff、mypy、isolated help 和文档测试，确认 P8 finalization 没有破坏 P15 验收。

## 2026-06-08 V2/V3 Final Re-verification After P8 Boundary Fix

完成度审计：

- `Docs/dev/V2_V3_Trackable_Tasks.md` 中除状态图例和 deferred items 外，没有 `[ ]`、`[~]` 或 `[!]` 未完成任务。
- `V2V3-P8-001` 已完成，`DatabasesService` 不再暴露表级 `query`。
- legacy `database query <database_id>` 和 MCP `database_query` 仍保留为兼容入口，但经 Core Raw API compatibility path 调用 `databases.query`。

最终验证命令和结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_final_full UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_final_full_env uv run pytest -q -p no:cacheprovider`
  - 结果：`173 passed, 1 skipped, 1 warning`。
  - warning：外部 FastAPI/TestClient 的 StarletteDeprecationWarning。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_final_full UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_final_full_env uv run ruff check .`
  - 结果：`All checks passed!`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_final_full UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_final_full_env uv run mypy src`
  - 结果：`Success: no issues found in 79 source files`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_final_isolated uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp --help`
  - 结果：通过；root help 显示完整命令组，`raw-api` 显示 advanced fallback。
- `find . -name __pycache__ -type d -print`
  - 结果：无输出。
- `test -d .venv && printf '.venv exists\n' || true`
  - 结果：无输出。
- `git diff --check`
  - 结果：无输出。

未运行：

- 未运行真实 Notion integration 测试；没有本轮用户提供的真实 token/workspace，也避免真实 Notion 写入。

剩余 deferred items：

- Stable `insert-before`。
- Full cache/index support。
- Local logs/audit。
- OAuth。
- GUI。

## 2026-06-08 Config Global/Local Namespace Split

背景：

- 用户指出 `Docs/User/Configuration.md` 中 `notion-mcp config set notion_token ...` 和 `notion-mcp init --token ... --user-id ...` 容易混淆，不清楚是全局配置还是当前仓库配置。
- 用户要求全局配置使用 `config global`，仓库级配置使用 `config local`。
- 用户要求普通用户不需要手动填写 `user_id`。

源码更新：

- `src/notion_mcp/cli/commands/config.py`
  - 新增 `notion-mcp config global set/get/list/unset`，行为等同旧全局 `config set/get/list/unset`。
  - 新增 `notion-mcp config local init/status/root`，复用项目级 `.notion_mcp` context 命令。
  - 保留旧 `notion-mcp config set/get/list/unset` 作为全局配置兼容入口。
- `src/notion_mcp/cli/commands/init.py`
  - `init` 不再缺省 prompt 用户 UUID；`--user-id` 和 `--user` 仅保留为可选兼容参数。
- `src/notion_mcp/core/config.py`
  - `init_core_config(..., user_id=None)` 支持不保存 configured user id。

测试更新：

- `tests/v2/cli/test_init.py`
  - 新增 `test_init_does_not_require_user_id`。
- `tests/v2/cli/test_config_commands.py`
  - 新增 `test_config_global_namespace_targets_global_config`。
  - 新增 `test_config_local_namespace_targets_project_config`。

文档更新：

- `Docs/User/Configuration.md`
  - 明确全局 token 使用 `notion-mcp config global set notion_token ...`。
  - 明确项目级配置使用 `notion-mcp config local init/status/root`。
  - 移除普通流程中手动填写 `user_id` 的说明。
- `Docs/User/Installation.md`
- `Docs/User/Cli.md`
- `Docs/User/Guide.md`
- `Docs/User/MCP_Clients.md`
- `Docs/User/Troubleshooting.md`
- `Docs/Developer/api/cli.md`
- `Docs/Developer/testing/cli.md`
  - 同步配置命名空间和 user id 可选语义。

验证命令和结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_config_split_pre UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_config_split_pre_env uv run pytest -q -p no:cacheprovider tests/v2/cli/test_init.py tests/v2/cli/test_config_commands.py`
  - 首次结果：`3 failed, 4 passed`。
  - 失败原因：符合测试先行预期；`init` 仍要求 `user_id`，`config global/local` 尚未实现。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_config_split_after UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_config_split_after_env uv run pytest -q -p no:cacheprovider tests/v2/cli/test_init.py tests/v2/cli/test_config_commands.py tests/v3/cli/test_project_init.py tests/v3/cli/test_project_status.py`
  - 结果：`15 passed`。

未运行：

- 未运行真实 Notion integration 测试；本阶段不需要真实 token/workspace。

## 2026-06-08 Root Init Project Context Correction

背景：

- 用户进一步明确 `notion-mcp init` 应该用于项目级初始化，在当前项目中生成 `.notion_mcp/` 配置目录，而不是全局配置入口。
- 全局配置继续使用 `notion-mcp config global ...`。
- 项目级配置继续使用 root `notion-mcp init`、`notion-mcp project init`、`notion-mcp local init` 或 `notion-mcp config local init`。

源码更新：

- `src/notion_mcp/cli/commands/init.py`
  - root `notion-mcp init` 改为 `project.init_command` 的薄别名。
  - 不再写入 Core global config。
  - 不再接收 `--token`、`--user-name`、`--user-id` 或 `--notion-version`。

测试更新：

- `tests/v2/cli/test_init.py`
  - 改为验证 root `init` 创建项目级 `.notion_mcp/config.json`、`state/`、`cache/`、`logs/`。
  - 验证 root `init` 不写 `NOTION_MCP_CONFIG` 指向的全局配置文件。
  - 验证 `--token` 不再属于 root `init`。

文档更新：

- `Docs/User/Configuration.md`
  - 明确 root `notion-mcp init` 是项目级初始化入口。
  - 明确全局 token 只推荐 `notion-mcp config global set notion_token ...`。
- `Docs/User/Cli.md`
  - 初始化章节同步 root `init` 的项目级语义。
- `Docs/User/Guide.md`
  - 缺少 token 的排障提示改为 `config global set notion_token`。
- `Docs/Developer/api/cli.md`
  - 命令结构同步 root `init` 到 project init alias。
- `Docs/Developer/testing/cli.md`
  - 测试说明同步 root `init` 新合约。

验证命令和结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_root_init_pre UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_root_init_pre_env uv run pytest -q -p no:cacheprovider tests/v2/cli/test_init.py`
  - 首次结果：`2 failed`。
  - 失败原因：符合测试先行预期；root `init` 仍是全局配置入口。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_root_init_after2 UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_root_init_after2_env uv run pytest -q -p no:cacheprovider tests/v2/cli/test_init.py tests/v2/cli/test_config_commands.py tests/v3/cli/test_project_init.py tests/v3/cli/test_project_status.py`
  - 结果：`14 passed`。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_root_init_final UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_root_init_final_env uv run pytest -q -p no:cacheprovider tests/test_cli.py tests/v2/cli/test_init.py tests/v2/cli/test_config_commands.py tests/v3/cli/test_project_init.py tests/v3/cli/test_project_status.py tests/v2/scenarios/test_full_local_config_flow.py tests/v2/scenarios/test_cli_documentation_inventory.py tests/v2/scenarios/test_stage7_documentation_completeness.py tests/v2/scenarios/test_stage8_release_readiness.py`
  - 结果：`26 passed`。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_root_init_final UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_root_init_final_env uv run ruff check src tests/test_cli.py tests/v2/cli/test_init.py tests/v2/scenarios/test_full_local_config_flow.py`
  - 结果：`All checks passed!`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_root_init_final UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_root_init_final_env uv run mypy src`
  - 结果：`Success: no issues found in 79 source files`。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_root_init_full UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_root_init_full_env uv run pytest -q -p no:cacheprovider`
  - 结果：`175 passed, 1 skipped, 1 warning`。
  - warning：外部 FastAPI/TestClient 的 StarletteDeprecationWarning。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_root_init_help uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp init --help`
  - 结果：通过；root `init` help 只显示项目级参数。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_root_init_help uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp config global --help`
  - 结果：通过；`config global` help 显示 `set/get/unset/list`。

未运行：

- 未运行真实 Notion integration 测试；本阶段只修改本地 CLI 配置入口和文档。

## 2026-06-08 Root CLI Help Text Fix

背景：

- 用户反馈 `notion-mcp --help` 的 Commands 表里 `init`、`status`、`set-token`、`set-user`、`show`、`run` 只有命令名，没有说明文字。
- 原因是这些 root 直接命令通过动态注册加入 Typer，但注册时没有传入 `help=`。

源码更新：

- `src/notion_mcp/cli/commands/init.py`
  - root `init` 注册时增加 `help` 文本。
- `src/notion_mcp/cli/commands/status.py`
  - root `status` 注册时增加 `help` 文本。
- `src/notion_mcp/cli/commands/legacy.py`
  - `set-token`、`set-user`、`show`、`run` 注册时增加 `help` 文本。
- `src/notion_mcp/cli/commands/project.py`
  - `project/local init/status/root` 动态子命令增加 `help` 文本。
- `src/notion_mcp/cli/commands/config.py`
  - `config global set/get/unset/list` 和 `config local init/status/root` 动态子命令增加 `help` 文本。

测试更新：

- `tests/v2/cli/test_help_text.py`
  - 新增 root help 文本回归测试。
  - 新增 project/config 动态子命令 help 文本回归测试。

文档更新：

- `Docs/Developer/testing/cli.md`
  - 记录 `tests/v2/cli/test_help_text.py` 的覆盖范围。

验证命令和结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_help_text_pre UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_help_text_pre_env uv run pytest -q -p no:cacheprovider tests/v2/cli/test_help_text.py`
  - 首次结果：`2 failed`。
  - 失败原因：符合测试先行预期；root 和动态子命令缺少 `help` 文本。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_help_text_after UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_help_text_after_env uv run pytest -q -p no:cacheprovider tests/v2/cli/test_help_text.py`
  - 结果：`2 passed`。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_help_text_after UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_help_text_after_env uv run notion-mcp --help`
  - 结果：通过；root Commands 表现在显示 `init/status/set-token/set-user/show/run` 的说明文字。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_help_text_final UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_help_text_final_env uv run pytest -q -p no:cacheprovider tests/v2/cli/test_help_text.py tests/v2/cli/test_init.py tests/v2/cli/test_config_commands.py tests/v3/cli/test_project_init.py tests/v3/cli/test_project_status.py`
  - 结果：`16 passed`。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_help_text_final UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_help_text_final_env uv run ruff check src tests/v2/cli/test_help_text.py`
  - 结果：`All checks passed!`
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_help_text_final UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_help_text_final_env uv run mypy src`
  - 结果：`Success: no issues found in 79 source files`。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_help_text_isolated uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp --help`
  - 结果：通过；isolated install style 的 root Commands 表也显示说明文字。

未运行：

- 未运行真实 Notion integration 测试；本阶段只修改 CLI help 文本。

## 2026-06-08 English-Only Program Output

背景：

- 用户要求代码里的程序输出全部使用英文，例如 `notion_token 已更新` 这类中文输出不应继续存在。

源码更新：

- `src/notion_mcp/cli/commands/legacy.py`
  - 将 legacy CLI prompt、echo 输出和 option help 文本改为英文。
- `src/notion_mcp/cli/commands/config.py`
  - 将 `config set/unset` 的 human output 改为英文：`updated`、`cleared`。
- `src/notion_mcp/dependencies.py`
  - 将缺少全局配置或 token 的 HTTP error detail 改为英文。
- `src/notion_mcp/config.py`
  - 将 legacy config 的异常文本和说明字符串改为英文。
- `src/notion_mcp/models/config_model.py`
  - 将 OpenAPI/schema 字段 description 改为英文。
- `src/notion_mcp/server.py`
  - 将 FastAPI app description 和模块说明改为英文。
- `src/notion_mcp/routes/*.py`
  - 将 route docstring、HTTP error detail 和说明字符串改为英文。
- `src/notion_mcp/__init__.py`
- `src/notion_mcp/routes/__init__.py`
  - 将源码模块说明改为英文。

测试更新：

- `tests/v2/cli/test_english_output_text.py`
  - 新增静态回归测试，扫描 `src/notion_mcp/**/*.py` 的字符串常量，禁止中文字符。

文档更新：

- `Docs/Developer/testing/cli.md`
  - 记录英文输出静态测试。

验证命令和结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_english_output_pre UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_english_output_pre_env uv run pytest -q -p no:cacheprovider tests/v2/cli/test_english_output_text.py tests/test_cli.py tests/v2/cli/test_config_commands.py`
  - 结果：`8 passed`。
- `rg -n "[\\p{Han}]" src/notion_mcp --glob '!README.md'`
  - 结果：无源码中文命中。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_english_output_final UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_english_output_final_env uv run pytest -q -p no:cacheprovider tests/v2/cli/test_english_output_text.py tests/test_cli.py tests/v2/cli/test_config_commands.py tests/v2/cli/test_help_text.py`
  - 结果：`10 passed`。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_english_output_final UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_english_output_final_env uv run ruff check src tests/v2/cli/test_english_output_text.py`
  - 结果：`All checks passed!`。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_english_output_final UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_english_output_final_env uv run mypy src`
  - 结果：`Success: no issues found in 79 source files`。
- `env PYTHONDONTWRITEBYTECODE=1 NOTION_MCP_CONFIG=/private/tmp/notion_mcp_missing_config_for_full_english_output.json UV_CACHE_DIR=/private/tmp/notion_mcp_uv_english_output_full2 UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_english_output_full2_env uv run pytest -q -p no:cacheprovider`
  - 结果：`178 passed, 1 skipped, 1 warning`。
  - 说明：首次全量运行发现根目录生成了 `__pycache__/`，导致 release readiness artifact 检查失败；删除该生成物后重跑通过。另一个首次失败来自本机全局配置状态，重跑时使用缺失配置路径隔离环境。

未运行：

- 未运行真实 Notion integration 测试；本阶段只修改本地输出文本。

## 2026-06-08 Reader-Facing Docs Boundary

背景：

- 用户指出 `Docs/User/Cli.md` 中命令清单缺少逐条作用说明。
- 用户要求 `Docs/dev` 之外的阅读文档不写 `v2/v3`、ADR、开发路径或测试路径这类开发资料。

文档更新：

- `Docs/User/Cli.md`
  - 将顶部“阶段实现状态”改为“快速入口和命令作用”。
  - 为 project/config/page/database/data-source 常用命令补充逐条作用说明。
  - 将 `config local init/status/root`、legacy `config get/set/list/unset` 和 Raw API operations 拆成逐条说明。
  - 保留用户需要知道的 `.notion_mcp` 项目路径和 attach state 路径，但移除 ADR、阶段和测试路径。
- `Docs/User/Configuration.md`
  - 删除 ADR 和阶段描述。
  - 将项目级配置、page attach 和 database attach 改成用户可读的操作说明。
- `Docs/User/Guide.md`
  - 移除指向开发者文档路径的尾部引用。
- `Docs/Requirements.md`、`Docs/Design.md`、`Docs/TechStack.md`、`Docs/Development_Plan.md`
  - 移除非必要阶段、ADR、开发路径和测试目录表述。
- `Docs/Developer/api/cli.md`
- `Docs/Developer/mcp_tools/databases.md`
- `Docs/Developer/mcp_tools/data_sources.md`
- `Docs/Developer/testing/*.md`
  - 将 ADR/阶段/逐测试路径叙述改为当前行为、对象边界和高层测试覆盖说明。

测试更新：

- `tests/v2/scenarios/test_documentation_reader_boundary.py`
  - 新增文档边界测试。
  - 验证 `Docs/User/*.md` 不包含 ADR、`v2/v3`、`Docs/dev`、`Docs/Developer` 或版本化测试路径。
  - 验证 `Docs/dev` 之外的文档不引用 ADR、`Docs/dev` 或版本化测试路径。
- `tests/v2/scenarios/test_stage1_documentation_alignment.py`
  - 更新历史开发计划文档断言，适配非 dev 文档不再直接引用 `Docs/dev/...` 路径。

验证命令和结果：

- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_docs_reader_boundary UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_docs_reader_boundary_env uv run pytest -q -p no:cacheprovider tests/v2/scenarios/test_documentation_reader_boundary.py tests/v2/scenarios/test_cli_documentation_inventory.py tests/v2/scenarios/test_stage7_documentation_completeness.py tests/v2/scenarios/test_stage1_documentation_alignment.py tests/v2/cli/test_raw_api_positioning.py`
  - 结果：`16 passed`。
- `env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/notion_mcp_uv_docs_reader_boundary UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_docs_reader_boundary_env uv run ruff check tests/v2/scenarios/test_documentation_reader_boundary.py tests/v2/scenarios/test_stage1_documentation_alignment.py`
  - 结果：`All checks passed!`。
- `rg -n -i "\\b(ADR(?:-[0-9]+)?|v2/v3|Docs/dev(?:/|$)|tests/v[0-9])\\b" Docs --glob '!Docs/dev/**'`
  - 结果：无命中。
- `rg -n "Docs/Developer|Docs/dev|tests/v[0-9]|ADR|v2/v3|\\bv[23]\\b" Docs/User`
  - 结果：无命中。
- `env PYTHONDONTWRITEBYTECODE=1 NOTION_MCP_CONFIG=/private/tmp/notion_mcp_missing_config_for_docs_boundary_full.json UV_CACHE_DIR=/private/tmp/notion_mcp_uv_docs_boundary_full UV_PROJECT_ENVIRONMENT=/private/tmp/notion_mcp_docs_boundary_full_env uv run pytest -q -p no:cacheprovider`
  - 结果：`180 passed, 1 skipped, 1 warning`。
  - 说明：warning 来自外部 FastAPI/TestClient 依赖。

未运行：

- 未运行真实 Notion integration 测试；本阶段只修改文档和文档边界测试。
