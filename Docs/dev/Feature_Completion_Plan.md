# Notion MCP 功能补全开发计划

本文档用于把当前原型补全为符合目标需求的本地 Notion MCP 服务器。它是开发者对象文档，放在 `Docs/dev/` 下，只描述开发计划、约束、阶段和验收标准；面向使用者的安装与使用说明仍放在 `Docs/User/` 下。

## v2 ADR 补充

`Docs/dev/ADR-002-local-context-and-cli-v2.md` 是已接受并已按 `Docs/dev/V2_V3_Trackable_Tasks.md` 完成最小闭环实现的 v2 设计决议。它补充本计划之后的产品层目标：

- Git-like 本地目录上下文配置。
- Page CLI 作为普通用户编辑页面内容的主入口。
- Block CLI 作为高级/底层入口。
- Database 和 DataSource 严格分离。
- Raw API 降级为兜底和高级入口。

ADR-002 中列出的命令和边界已经进入 v2/v3 实施闭环；当前精确实现状态仍以源码、`Docs/User/Cli.md`、`Docs/Developer/api/cli.md` 和 `Docs/dev/progress.md` 为准。

`Docs/dev/ADR-003-project-attach-context.md` 是已接受并已按 `Docs/dev/V2_V3_Trackable_Tasks.md` 完成最小闭环实现的 runtime 工作流设计。它将 ADR-002 的本地上下文进一步收敛为项目级 `.notion_mcp` 目录和 page/database attach state 工作流：

- 项目级配置文件：`.notion_mcp/config.json`。
- Page attach 状态：`.notion_mcp/state/page.attach.json`。
- Database attach 状态：`.notion_mcp/state/database.attach.json`。
- 标准命令：`project init/status/root`、`page attach/status/refresh/detach`、`database attach/status/refresh/detach`。
- 兼容别名：`local ...` 和 `deattach`。
- 测试目录：`tests/v3/core/`、`tests/v3/cli/`、`tests/v3/scenarios/`。

当前 project context 和 attach workflow 以 ADR-003 为准；ADR-002 中 Database/DataSource 分离、Page CLI 主入口和 Raw API 兜底原则仍然有效。

开发实施入口：

- `Docs/dev/V2_V3_Development_Design.md`：把 ADR-002 和 ADR-003 转换为实现导向的开发设计，包括 Core/CLI/MCP 边界、项目配置、attach state、Database/DataSource 分离和测试策略。
- `Docs/dev/V2_V3_Trackable_Tasks.md`：把后续实现拆成带任务 ID、依赖、输出文件、测试和验收标准的可追踪任务列表。

## 历史基线结论

以下结论记录 2026-06-07 阶段 0 启动时的历史基线，不代表当前 v2/v3 最终状态。当前实现状态以 `Docs/dev/V2_V3_Trackable_Tasks.md` 和 `Docs/dev/progress.md` 为准。

已确认的现状：

- 源码目录是 `notion_mcp/`，没有标准 `src/` 布局。
- 没有独立 `core/` 业务逻辑层。
- CLI 直接调用配置函数，HTTP 路由直接调用 Notion SDK 客户端。
- 没有 `mcp` 依赖，没有 MCP server、tool schema、stdio、SSE 或 Streamable HTTP transport。
- 只覆盖少量数据库、页面、区块 REST 操作，未覆盖 Notion API/SDK 的 users、comments、views、file uploads、search、custom emojis、data sources 完整操作等能力。
- `user_id` 只被保存到配置，没有参与编辑者身份校验、审计或操作元数据。
- 现有测试是 mock 单元测试，不包含 MCP 协议测试、隔离安装测试、CLI JSON 模式测试或端到端场景测试。
- `pyproject.toml` 的包发现配置会导致隔离安装后的 `notion-mcp` 入口导入失败。
- `Docs/Development_Plan.md` 把当前原型功能标为完成，但该完成状态只覆盖原型目标，不代表本计划的最终目标已完成。

## 目标形态

最终项目必须采用：

```text
Core + CLI + MCP Tool
```

调用关系必须是：

```text
Human -> CLI -> Core
Agent / LLM -> MCP Tool -> Core
```

禁止以下关系：

```text
MCP Tool -> CLI 字符串 -> Core
CLI 一套业务逻辑，MCP 另一套业务逻辑
```

目标能力：

- 本地安装和运行，优先支持 `uv` 隔离环境；可保留 pip 兼容说明。
- 通过 Notion 集成 token、personal access token 或其他 bearer token 访问 Notion API。
- 全局配置采用 git-like 本地工具体验，初始化时保存 token、用户名、Notion 用户 UUID、Notion API version、默认 transport 等配置。
- Core 覆盖 Notion SDK/API 的公开能力，至少按对象域覆盖 pages、blocks、databases、data sources、users、comments、views、file uploads、search、custom emojis。
- MCP Tool 面向 Agent/LLM，暴露结构化工具、参数 schema、返回结构、危险操作标记和错误信息。
- CLI 面向人类，提供清晰命令、普通文本输出、`--json` 输出、`--dry-run` 支持和可调试状态命令。
- 文档分离：开发者文档包含需求、架构、API/MCP tool、测试、阶段计划、验证方式；使用者文档只包含安装、配置、运行和调用方法。

## 设计依据

本计划以当前官方文档为依据，而不是沿用旧文档里的过期假设。

- Notion API 是 versioned API，请求需要 `Notion-Version`，当前文档示例已使用 `2026-03-11`。
- `2026-03-11` 对 block append、trash/archive 字段和 block type 有 breaking changes：`after` 改为 `position`，`archived` 改为 `in_trash`，`transcription` 改为 `meeting_notes`。
- Notion API 参考中包含 blocks、pages、databases、data sources、comments、views、file uploads、search、users、custom emojis 等对象和端点。
- Notion 官方 MCP 是远程托管服务，使用 OAuth；本项目选择本地自托管时，应明确用于 bearer token、自动化或复用已有 Notion connection 的场景。
- MCP Python SDK 通过 tools/resources/prompts 暴露能力；tools 是执行有副作用或计算动作的正式结构化入口。

参考链接：

- Notion API Reference: https://developers.notion.com/reference/intro
- Notion API Versioning: https://developers.notion.com/reference/versioning
- Notion 2026-03-11 Upgrade Guide: https://developers.notion.com/guides/get-started/upgrade-guide-2026-03-11
- Notion MCP Overview: https://developers.notion.com/guides/mcp/overview
- Notion Local MCP Hosting: https://developers.notion.com/guides/mcp/hosting-open-source-mcp
- Notion MCP Supported Tools: https://developers.notion.com/guides/mcp/mcp-supported-tools
- MCP Python SDK: https://github.com/modelcontextprotocol/python-sdk

## 目录重构目标

目标目录结构：

```text
Docs/
  Developer/
    architecture/
    api/
    mcp_tools/
    testing/
  User/
    Installation.md
    Configuration.md
    Cli.md
    Cli/
      Overview.md
      Project_Config.md
      Page.md
      Block.md
      Database_DataSource.md
      Auth_And_User.md
      Comments.md
      Views.md
      File_Uploads.md
      Search_And_Custom_Emoji.md
      Raw_API.md
      MCP_Server.md
      Legacy_Commands.md
    MCP_Clients.md
    Troubleshooting.md
  dev/
    Feature_Completion_Plan.md
    progress.md
    test_policy.md

src/
  notion_mcp/
    core/
      config.py
      auth.py
      client.py
      errors.py
      models.py
      audit.py
      services/
        blocks.py
        pages.py
        databases.py
        data_sources.py
        users.py
        comments.py
        views.py
        file_uploads.py
        search.py
        custom_emojis.py
        raw_api.py
    cli/
      app.py
      commands/
        init.py
        config.py
        status.py
        auth.py
        pages.py
        blocks.py
        databases.py
        data_sources.py
        users.py
        comments.py
        views.py
        files.py
        search.py
        mcp.py
    mcp_server/
      server.py
      tools/
        config.py
        auth.py
        pages.py
        blocks.py
        databases.py
        data_sources.py
        users.py
        comments.py
        views.py
        file_uploads.py
        search.py
        custom_emojis.py
        raw_api.py

tests/
  legacy/
  v2/
    core/
    cli/
    mcp_server/
    scenarios/
```

迁移原则：

- 现有 `tests/test_*.py` 不修改。若需要保留为回归测试，可整体复制或移动前必须先获得明确决策；默认做法是保持原文件不变，并在 `tests/v2/` 下新增新测试。
- 新测试一旦创建，不能为了过测试而修改；只能新增 `v2`、`v3` 或更明确命名的补充测试，并在 `Docs/dev/progress.md` 记录原因。
- 若重构导致旧测试失败，优先保持兼容适配层，不能直接改旧测试。
- 删除 `__pycache__` 等生成物应作为仓库卫生任务处理，不把生成物纳入正式仓库代码。

## 阶段 0：基线修复和事实冻结

目标：让仓库具备可靠的开发入口，并冻结当前事实，避免在错误基线上继续扩展。

先写测试：

- 新增 `tests/v2/scenarios/test_isolated_install.py`，验证 `uv run --with <repo_path> notion-mcp --help` 可以导入并显示 CLI。
- 新增 `tests/v2/core/test_packaging_metadata.py`，验证包发现能安装 `notion_mcp`。
- 新增 `tests/v2/scenarios/test_existing_rest_smoke.py`，验证现有 FastAPI 根路由和 legacy REST 路由在迁移前仍可导入。

再实现：

- 修正 `pyproject.toml` 包发现配置，优先迁移到 `src/` layout。
- 统一依赖管理，优先采用 `uv`；若保留 `requirements.txt`，必须说明它是兼容文件还是废弃文件。
- 移除生成物：`__pycache__`、构建副产物、测试缓存。
- 增加 `.gitignore` 或等效忽略文件，覆盖 Python、uv、构建和缓存输出。
- 明确 Python 版本，建议以 Python 3.12 作为开发默认版本，兼容范围另行验证。

验收：

- 隔离安装命令通过。
- `notion-mcp --help` 在隔离环境中通过。
- legacy 测试继续通过，新增 v2 基线测试通过。
- `Docs/dev/progress.md` 记录阶段完成、命令和结果。

## 阶段 1：更新顶层需求和架构文档

目标：修正当前文档把 REST 原型称为 MCP 完成品的问题。

先写测试或检查脚本：

- 新增文档检查脚本或测试，验证 `Docs/Developer/` 与 `Docs/User/` 均存在。
- 新增文档检查，验证开发者文档包含 MCP tool 文档入口，使用者文档包含 MCP client 配置入口。
- 新增文档检查，验证 `Docs/Requirements.md` 不再把当前 REST 原型描述为最终完成状态。

再实现：

- 更新 `Docs/Requirements.md`：拆分已实现原型能力和待实现目标能力。
- 更新 `Docs/Design.md`：明确 Core、CLI、MCP Tool 的调用关系。
- 更新 `Docs/TechStack.md`：加入 `mcp` Python SDK、uv、Notion API version 策略。
- 保留或重写 `Docs/Development_Plan.md`，将当前完成清单标注为 legacy prototype，不作为最终完成证明。
- 新增 `Docs/dev/test_policy.md`，正式记录“测试先行、既有测试不可修改、只能新增测试版本”的规则。
- 新增 `Docs/dev/progress.md`，作为阶段推进记录。

验收：

- 文档检查通过。
- 开发者和使用者文档边界清晰。
- 所有未实现能力明确标记为待开发，不能标为完成。

## 阶段 2：Core 层落地

目标：建立唯一业务逻辑层，使 CLI 和 MCP 都只调用 Core。

先写测试：

- `tests/v2/core/test_config.py`
  - 配置初始化、读取、更新、路径覆盖、权限校验。
  - token 不在普通状态输出中泄露。
  - user UUID 格式校验。
  - Notion API version 默认值和覆盖。
- `tests/v2/core/test_auth.py`
  - `auth_validate` 调用 Notion self/user endpoint 的 mock。
  - token 缺失、token 无效、权限不足的错误模型。
- `tests/v2/core/test_client.py`
  - Notion client 初始化注入 token、version、timeout、retry。
  - fake client 可替代真实 client。
- `tests/v2/core/test_services_*.py`
  - 每个服务模块只封装 Core 行为，不依赖 CLI 或 MCP。
- `tests/v2/core/test_raw_api.py`
  - 覆盖受控 SDK pass-through 或 raw endpoint 调用。
  - 验证只允许已登记的 Notion SDK/API 操作。

再实现：

- `core/config.py`：全局配置文件、路径、权限、密钥脱敏。
- `core/auth.py`：token 校验、bot/self 查询、用户 UUID 校验。
- `core/client.py`：Notion SDK client 工厂，支持 fake client 注入。
- `core/errors.py`：统一错误模型，供 CLI 和 MCP 复用。
- `core/models.py`：请求/响应模型和公共类型。
- `core/audit.py`：记录本地操作元数据，包含 configured user UUID、operation、target、dry-run、timestamp。
- `core/services/*`：按 Notion API 对象域拆分服务。
- `core/services/raw_api.py`：为“支持 Notion SDK 所有操作”提供受控扩展入口，避免为每个 endpoint 临时复制逻辑。

验收：

- Core 测试全部通过。
- Core 不导入 CLI 或 MCP 模块。
- CLI 和 MCP 后续只能调用 Core，不直接调用 Notion SDK。

## 阶段 3：CLI 补全为 git-like 本地工具

目标：CLI 服务人类使用体验，可读、可调试、可脚本化。

先写测试：

- `tests/v2/cli/test_init.py`
  - `notion-mcp init` 交互和非交互模式。
  - token、用户名、user UUID、API version 写入。
  - 文件权限符合当前用户读写。
- `tests/v2/cli/test_config_commands.py`
  - `notion-mcp config get/set/unset/list`。
  - token 输出默认脱敏。
- `tests/v2/cli/test_status.py`
  - 普通输出给人看。
  - `--json` 输出稳定结构。
- `tests/v2/cli/test_resource_commands.py`
  - pages、blocks、databases、data_sources、users、comments、views、files、search 命令都通过 Core mock。
- `tests/v2/cli/test_dry_run.py`
  - 写操作支持 `--dry-run`，不会调用真实写入。

再实现：

- `cli/app.py`：统一 Typer app。
- `cli/commands/init.py`：初始化配置。
- `cli/commands/config.py`：git-like 配置命令。
- `cli/commands/status.py`：配置状态、auth 状态、默认 API version、MCP 可用性。
- `cli/commands/auth.py`：`auth validate`、`auth whoami`。
- `cli/commands/*`：面向人类的 Notion 操作命令。
- `cli/commands/mcp.py`：`notion-mcp mcp serve`，启动 MCP server，不通过 HTTP REST 路由绕行。

验收：

- `notion-mcp --help`、`notion-mcp status --json`、`notion-mcp mcp serve --help` 都在隔离安装后可用。
- CLI 测试全部通过。
- CLI 不直接调用 Notion SDK。

## 阶段 4：MCP Server 和 MCP Tools 落地

目标：建立 Agent/LLM 的正式结构化调用入口。

先写测试：

- `tests/v2/mcp_server/test_server_lifecycle.py`
  - MCP server 可初始化。
  - stdio transport 可启动到握手阶段。
  - Streamable HTTP transport 可挂载或启动。
- `tests/v2/mcp_server/test_tool_inventory.py`
  - 工具列表包含 config、auth、pages、blocks、databases、data_sources、users、comments、views、file_uploads、search、custom_emojis、raw_api。
  - 每个工具有名称、描述、输入 schema、输出结构。
- `tests/v2/mcp_server/test_tool_calls.py`
  - MCP tool 调用 Core mock，不调用 CLI。
  - 错误按 MCP 结果结构返回。
- `tests/v2/mcp_server/test_dangerous_tools.py`
  - 删除、归档、移动、覆盖类操作必须声明危险性或需要显式确认参数。
- `tests/v2/scenarios/test_mcp_client_flow.py`
  - 使用 MCP client/inspector 风格流程完成 initialize、list_tools、call_tool。

再实现：

- `mcp_server/server.py`：创建 MCP server，注册 tools/resources/prompts，支持 stdio 和 Streamable HTTP。
- `mcp_server/tools/config.py`：`config_status`、`config_get`。
- `mcp_server/tools/auth.py`：`auth_validate`、`auth_whoami`。
- `mcp_server/tools/pages.py`：`page_retrieve`、`page_create`、`page_update`、`page_trash`、`page_move`、`page_duplicate`。
- `mcp_server/tools/blocks.py`：`block_children_list`、`block_append`、`block_update`、`block_delete_or_trash`。
- `mcp_server/tools/databases.py`：database create/retrieve/update/list related operations。
- `mcp_server/tools/data_sources.py`：data source retrieve/query/update/templates。
- `mcp_server/tools/users.py`：users list/retrieve/me/bot self。
- `mcp_server/tools/comments.py`：comments list/create/reply。
- `mcp_server/tools/views.py`：view create/update/query/list。
- `mcp_server/tools/file_uploads.py`：file upload lifecycle。
- `mcp_server/tools/search.py`：search Notion workspace。
- `mcp_server/tools/custom_emojis.py`：custom emoji list/retrieve where supported。
- `mcp_server/tools/raw_api.py`：受控 SDK/API 操作入口，用于覆盖未被专用工具封装的 Notion SDK 操作。

验收：

- MCP lifecycle、tool inventory、tool call 测试通过。
- MCP 工具全部直接调用 Core。
- Agent 不需要拼 CLI 字符串即可完成操作。
- `Docs/Developer/mcp_tools/` 每个工具域有对应文档。

## 阶段 5：Notion SDK/API 覆盖补全

目标：从“少数 REST 路由”扩展为“覆盖 Notion SDK/API 公开能力”。

先写测试：

- 每个对象域新增服务测试和 MCP tool 测试。
- 对所有分页接口新增分页场景测试，覆盖 `start_cursor`、`page_size`、`has_more`、`next_cursor`。
- 对写操作新增 dry-run 测试。
- 对真实环境才能验证的内容新增 `live` 标记测试，并默认跳过。

再实现：

- pages：retrieve、create、update、property item retrieve、trash/in_trash。
- blocks：retrieve、children list、append with `position`、update、delete/trash。
- databases：create、retrieve、update、move/trash where supported。
- data sources：retrieve、query、update、templates、properties。
- users：list、retrieve、me/self。
- comments：list、create、reply。
- views：create、update、list、query。
- file uploads：create/send/complete/list/retrieve where SDK supports。
- search：search endpoint。
- custom emojis：list/retrieve where supported。
- raw API：受控 pass-through，用登记表覆盖 SDK 暂未专门建模的操作。

验收：

- 工具覆盖清单与 Notion API reference 对齐。
- 不能实现或需付费/权限的能力必须在文档中标注原因和测试状态。
- 所有离线 mock 测试通过。
- live 测试可通过环境变量启用，并默认跳过。

## 阶段 6：场景测试和真实环境测试

目标：证明仓库不仅单元测试通过，还能按真实工作流运行。

先写测试：

- `tests/v2/scenarios/test_full_local_config_flow.py`
  - 临时 HOME 或临时 config 路径。
  - `init`、`status --json`、`auth validate` mock。
- `tests/v2/scenarios/test_cli_to_core_to_fake_notion.py`
  - CLI 写操作通过 Core 到 fake Notion。
- `tests/v2/scenarios/test_mcp_to_core_to_fake_notion.py`
  - MCP tool 通过 Core 到 fake Notion。
- `tests/v2/scenarios/test_install_and_run.py`
  - `uv run --with . notion-mcp --help`。
  - `notion-mcp mcp serve --help`。
- `tests/live/test_live_auth_validate.py`
  - 需要 `NOTION_MCP_LIVE=1`、真实 token 和测试页面，默认跳过。

再实现：

- 增加 fake Notion server 或 fake SDK client fixture。
- 增加 live 测试门控。
- 增加场景测试文档：如何运行、需要哪些环境变量、哪些测试默认跳过。

验收：

- 离线场景测试默认通过。
- live 测试默认跳过并显示明确原因。
- 使用真实环境时，live 测试不修改生产数据；如需写入，只允许测试页面或测试 workspace。

## 阶段 7：文档补全和同步

目标：开发者文档和使用者文档各自完整，不混写。

开发者文档：

- `Docs/Developer/architecture/overview.md`
  - Core、CLI、MCP Tool 调用关系。
- `Docs/Developer/api/core.md`
  - Core 服务 API。
- `Docs/Developer/mcp_tools/*.md`
  - 每个 MCP tool 的说明、参数、返回、危险性、错误。
- `Docs/Developer/testing/strategy.md`
  - 单元、场景、live 测试策略。
- `Docs/Developer/testing/live.md`
  - 真实 Notion 环境测试门控和安全要求。
- `Docs/Developer/packaging.md`
  - uv、pip、入口脚本、发布检查。

使用者文档：

- `Docs/User/Installation.md`
  - uv 隔离安装、pip 安装、卸载。
- `Docs/User/Configuration.md`
  - token、user UUID、用户名、API version、配置路径。
- `Docs/User/Cli.md`
  - git-like CLI 使用方法。
- `Docs/User/MCP_Clients.md`
  - Codex、Claude、Cursor、VS Code 等 MCP client 配置。
- `Docs/User/Troubleshooting.md`
  - token、权限、Notion API version、rate limit、MCP handshake 常见问题。

验收：

- 开发者文档不写普通用户教程。
- 使用者文档不暴露内部设计细节。
- 每个已实现功能都有对应开发者文档。
- 用户可按 `Docs/User/Installation.md` 从零安装并启动。

## 阶段 8：发布前验收

目标：证明完整仓库可以交付。

必须通过：

```bash
uv run pytest -q -p no:cacheprovider
uv run ruff check .
uv run mypy src
uv run --with . notion-mcp --help
uv run --with . notion-mcp status --json
uv run --with . notion-mcp mcp serve --help
```

如未配置 `ruff` 或 `mypy`，本阶段先增加对应 dev 依赖和配置，再写检查说明。

交付清单：

- 无超大文本文件。
- 无 `__pycache__`、build、dist、egg-info、pytest cache 等生成物。
- 源码目录按功能拆分。
- 测试目录按 core、cli、mcp_server、scenarios、live 拆分。
- 现有测试未被修改；新增测试按版本或目的落位。
- 隔离安装可用。
- CLI 和 MCP 都调用 Core。
- MCP tools 可被 MCP client 枚举和调用。
- 文档已按开发者和使用者拆分。
- 真实环境测试如未执行，必须明确标记为跳过原因和启用方式。

## 风险和决策点

- Notion 官方远程 MCP 使用 OAuth；本项目坚持本地 bearer token 模式时，需要在文档中明确这是自托管自动化场景，不等同官方托管 MCP。
- “支持 Notion SDK 所有操作”不能只靠少数手写工具完成，需要专用工具加受控 raw/pass-through 入口共同覆盖。
- Notion API version 会继续变化，Core 必须集中管理 `Notion-Version`，不能散落在各工具里。
- file uploads、AI search、query across data sources 等能力可能受计划、权限或 SDK 版本限制；需要区分离线 mock 通过、live 可用、权限不足三种状态。
- 如果后续要把当前目录初始化为 Git 仓库，应先确认用户意图；没有 Git 时，“既有测试不可修改”的约束只能靠流程和文档维护，不能靠版本控制自动证明。

## 近期下一步

下一次开发应从阶段 0 开始，不应直接扩写 REST 路由。

执行顺序：

1. 创建 `Docs/dev/test_policy.md` 和 `Docs/dev/progress.md`。
2. 新增隔离安装失败的 v2 测试，先让测试失败。
3. 修正 packaging 和 `src/` layout。
4. 保持 legacy 测试通过。
5. 更新 `Docs/Development_Plan.md`，标注其为 legacy prototype 计划。
6. 进入 Core 层测试和实现。
