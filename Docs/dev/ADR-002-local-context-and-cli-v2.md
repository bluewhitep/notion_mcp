# ADR-002: Notion 本地 MCP v2 设计决议

## 状态

Accepted / 待实施。

本文是 v2 设计决议和实施边界记录。本文记录未来要实现的设计决策，不表示当前 CLI 已经具备全部命令。当前已实现命令仍以 `Docs/User/Cli.md`、`Docs/Developer/api/cli.md` 和源码为准。

## 后续 ADR 覆盖说明

`Docs/dev/ADR-003-project-attach-context.md` 已接受项目级 `.notion_mcp` 配置与 page/database attach 工作流设计。ADR-003 覆盖本文中项目级目录命名和本地上下文工作流的早期设计：

- 本文早期命名：`.notion-mcp/config.json`
- ADR-003 最终命名：`.notion_mcp/config.json`

后续实现 project context、page attach 和 database attach 时，以 ADR-003 为准。本文关于 Database/DataSource 分离、Page CLI 主入口、Block CLI 高级入口和 Raw API 兜底定位的决策仍然有效。

## 背景

本项目目标是制作一个本地运行的 Notion MCP 服务器，使用 Notion 集成授权访问 Notion API。该服务需要类似 Git 一样支持全局配置和本地目录上下文配置：

- 全局配置保存认证、用户、Notion API version、timeout、retry 等运行参数。
- 本地目录配置保存当前目录绑定的 Notion 主 page。
- CLI 从当前工作目录向上查找本地配置，使普通用户不需要每次输入 page id。
- Core 覆盖 Notion SDK/API 的公开能力。
- MCP Tool 面向 Agent/LLM 暴露结构化能力。
- CLI 面向人类提供常用、可解释、可组合的操作。
- Raw API 保留为兜底和高级入口。

此前存在一个需要修正的设计点：不能把 `data_source` 简化理解为 `database`。在新的 Notion API 语义里，`database` 和 `data_source` 是不同对象：

- `database` 是容器对象。
- `data_source` 是 `database` 下的具体表。
- `data_source` 承载 schema、properties、query、templates、entries/pages 等表级能力。
- `database` 负责容器级信息，例如包含哪些 data sources、database 的父级、创建/更新 database 容器等。

因此，v2 设计必须同时建模 `database` 和 `data_source`，不能让任一方吞并另一方。

## 官方文档核对

本 ADR 已按 Notion 官方文档做设计语义核对：

- [Notion Database object](https://developers.notion.com/reference/database)：database 是包含一个或多个 data sources 的容器；在 `2025-09-03` 之后，database object 包含 child `data_sources`，不再把 data source properties 放在 database 层。
- [Notion Data source object](https://developers.notion.com/reference/data-source)：data sources 是 database 下的独立数据表；pages 是 data source 中的 items/children；data source API 覆盖 create、update、retrieve、query。
- [Notion Versioning](https://developers.notion.com/reference/versioning)：Notion API 通过 `Notion-Version` header 固定行为；breaking changes 通过新的 API version 发布；SDK 版本和 API version 是独立概念。

## 决议 1：全局配置与本地目录配置分离

采用双层配置模型：

| 配置类型 | 路径 | 保存内容 | 是否保存 token | 作用 |
| --- | --- | --- | --- | --- |
| 全局配置 | `~/.notion_mcp/config.json` | `token`、`user_id`、`notion_version`、`timeout`、`retry` | 是 | 认证和运行配置 |
| 本地配置 | `.notion-mcp/config.json` | `main_page_id`、`main_page_title`、`workspace_hint` | 否 | 当前目录的 Notion 上下文 |

本地配置文件名采用 `.notion-mcp/config.json`，不采用 `.notion-mcp.json`。原因是 `.notion-mcp/config.json` 更接近 Git 的目录配置模型，并为未来扩展留出空间：

```text
.notion-mcp/
  config.json
  cache/
  index/
  audit/
  logs/
```

本地目录配置不得保存 token，避免把个人或集成凭据写进项目目录。

本地配置字段：

```json
{
  "main_page_id": "notion-page-id",
  "main_page_title": "Project Home",
  "workspace_hint": "optional-human-readable-name"
}
```

本地配置命令：

```bash
notion-mcp local init --main-page <page_id>
notion-mcp local status
notion-mcp local set main_page_id <page_id>
notion-mcp local unset main_page_id
```

上下文解析规则：

1. CLI 从当前工作目录开始向上查找 `.notion-mcp/config.json`。
2. 找到后，将 `main_page_id` 作为默认 page 上下文。
3. 用户显式传入 `<page_id>` 时，显式参数覆盖本地默认上下文。
4. 没有本地配置且命令需要 page 上下文时，CLI 必须提示用户显式传入 page id，或先执行 `notion-mcp local init --main-page <page_id>`。

## 决议 2：Database 和 DataSource 必须严格区分

Core/API 层必须同时建模：

- `Database`
- `DataSource`
- `Page`
- `Block`
- `User`
- `Search`
- `RawApi`

不得把 `data_source` 当作 `database` 的别名，也不得把所有 database-like 操作都塞进 `DatabaseService`。

语义边界：

| 对象 | 语义 | 负责能力 |
| --- | --- | --- |
| `database` | Notion database 容器 | 创建 database、更新 database 容器、读取 database、列出 child data sources |
| `data_source` | database 下的具体表 | schema/properties、query、templates、在表中创建 page、更新表结构 |
| `page` | 普通页面或 data source entry | 页面属性、页面内容、页面移动、页面 trash |
| `block` | 页面内容节点 | children、append、update、trash |

推荐 Core 服务划分：

```text
DatabaseService
  retrieve_database(database_id)
  create_database(parent, title, initial_data_source)
  update_database(database_id, ...)
  list_data_sources(database_id)

DataSourceService
  retrieve_data_source(data_source_id)
  query_data_source(data_source_id, filter, sorts, ...)
  create_data_source(database_id, title, properties, ...)
  update_data_source(data_source_id, properties, ...)
  list_data_source_templates(data_source_id)

PageService
  retrieve_page(page_id)
  create_page(parent: page_id | data_source_id, properties, children, position)
  update_page(page_id, properties)
  trash_page(page_id)
  move_page(page_id, target_parent)

BlockService
  retrieve_block(block_id)
  list_children(block_id, recursive=False)
  append_children(block_id, children, position_or_after)
  update_block(block_id, payload)
  trash_block(block_id)

RawApiService
  invoke(method, path, query, body)
```

禁止的错误建模：

```text
DatabaseService = database + data_source + database page + schema + query 全部混在一起
database_id == data_source_id
data_source 就是 database
```

正确写法：

- `data_source` 是 Notion database 下的具体表。
- `database` 是容器。
- 一个 `database` 可以包含一个或多个 `data_source`。
- 多数旧 database query/schema 操作在新 API 中应迁移到 `data_source`。

## 决议 3：用户 CLI 可以保留 database 心智，但必须暴露 data-source 命名空间

CLI 同时提供：

```bash
notion-mcp database ...
notion-mcp data-source ...
```

其中：

- `database` 命令处理容器级操作。
- `data-source` 命令处理表级操作。
- `database page ...` 可以作为人类友好的快捷命令，但内部必须解析到 data source。
- 当 database 包含多个 data sources 时，CLI 不得静默选择其中一个，必须要求用户显式指定。

Database CLI 容器级命令：

```bash
notion-mcp database retrieve <database_id>
notion-mcp database sources <database_id>
notion-mcp database create --payload '<json>'
notion-mcp database update <database_id> --payload '<json>'
notion-mcp database rename <database_id> <new_name>
```

DataSource CLI 表级命令：

```bash
notion-mcp data-source retrieve <data_source_id>
notion-mcp data-source query <data_source_id> --payload '<json>'
notion-mcp data-source create <database_id> --payload '<json>'
notion-mcp data-source update <data_source_id> --payload '<json>'
notion-mcp data-source templates <data_source_id>
notion-mcp data-source property rename <data_source_id> <property_id_or_name> <new_name>
```

Database 快捷命令人类友好入口：

```bash
notion-mcp database page create <database_id_or_data_source_id> --properties '<json>'
notion-mcp database page update <page_id> --properties '<json>'
notion-mcp database query <database_id_or_data_source_id> --payload '<json>'
```

快捷命令解析规则：

- 当传入的是 `data_source_id`，直接调用 `DataSourceService`。
- 当传入的是 `database_id`，先 retrieve database，读取 data sources。
- 如果 database 只有一个 data source，自动选择该 data_source。
- 如果 database 有多个 data sources，报错并提示用户使用 `--data-source <data_source_id_or_name>`。

多 data source 报错示例：

```text
This database has multiple data sources:
1. Tasks
2. Bugs
3. Archive
Please pass --data-source <data_source_id_or_name>.
```

## 决议 4：Page CLI 是普通用户编辑页面内容的主入口

Page CLI 作为普通用户在当前页面内探索、读取和编辑内容的主入口。用户不应该为了编辑当前页面内容而直接理解 block API。Block CLI 仍然存在，但它是更底层、更高级的入口。

Page CLI 支持：

- 获取当前页面内容。
- 返回页面属性。
- 返回页面下的 block 列表或树。
- 返回每个 block 的 id、type、text 摘要和父子关系。
- 支持 `--json` 给脚本或 Agent 使用。
- 在当前 page 内编辑 block。
- 在当前 page 下插入 page。
- 在当前 page 下插入 database。

Page CLI 命令：

```bash
notion-mcp page content
notion-mcp page content <page_id>
notion-mcp page content --json
notion-mcp page content --tree
notion-mcp page block remove <block_id>
notion-mcp page block update <block_id> --payload '<json>'
notion-mcp page block insert-after <block_id> --payload '<json>'
notion-mcp page block append <block_id> --payload '<json>'
notion-mcp page insert page --payload '<json>'
notion-mcp page insert database --payload '<json>'
```

`notion-mcp page content` 默认读取当前目录本地配置中的 `main_page_id`。`notion-mcp page content <page_id>` 使用显式 page id 覆盖本地配置。

普通输出应适合人类阅读：

```text
Page: Project Home
ID: xxx
Properties:
- Status: Active
- Owner: Blue White
Blocks:
1. [paragraph] block_id=... "intro text..."
2. [heading_2] block_id=... "Tasks"
3. [bulleted_list_item] block_id=... "item..."
```

JSON 输出应适合脚本和 Agent：

```json
{
  "page": {
    "id": "page-id",
    "properties": {}
  },
  "blocks": [
    {
      "id": "block-id",
      "type": "paragraph",
      "text": "summary",
      "parent_id": "page-id",
      "has_children": false,
      "children": []
    }
  ]
}
```

## 决议 5：Block CLI 保留为高级/底层入口

Block CLI 不作为普通用户编辑当前页面内容的主入口。它保留给以下场景：

- 用户已知 block id，要直接操作任意 block。
- 操作不依赖当前 page。
- 调试 Notion block API 的底层行为。
- 跨 page 检查或操作 block。
- MCP/Agent 调试。

Block CLI 命令：

```bash
notion-mcp block retrieve <block_id>
notion-mcp block children <block_id>
notion-mcp block children <block_id> --recursive
notion-mcp block append <block_id> --payload '<json>'
notion-mcp block update <block_id> --payload '<json>'
notion-mcp block trash <block_id>
```

用户文档中，普通页面编辑优先展示：

```bash
notion-mcp page content
notion-mcp page block update <block_id> --payload '<json>'
notion-mcp page block append <block_id> --payload '<json>'
```

Block CLI 放在高级用法章节。

## 决议 6：insert-before 不作为 v2 首批稳定能力

v2 首批稳定支持：

```bash
notion-mcp page block insert-after <block_id> --payload '<json>'
```

暂不把以下命令作为稳定能力：

```bash
notion-mcp page block insert-before <block_id> --payload '<json>'
```

原因：

- Notion block append/position 能力存在版本差异和 API 限制。
- 旧 API 主要使用 `after` 参数插入到某个 block 后。
- 新 API/SDK 中 `position` 能力更细。
- 现有 block 不能通过 append endpoint 被移动。
- `insert-before` 对“目标 block 是第一个 sibling”的情况无法简单实现。

v2.1 可选 best-effort 规则：

1. 找到目标 block 的父级。
2. 列出父级 children。
3. 找到目标 block 的前一个 sibling。
4. 如果存在 previous sibling，则用 `after`/`position` 插到 previous sibling 后。
5. 如果目标 block 是第一个 sibling，则根据 Notion-Version 判断是否支持 `position.start` 或 `page_start`；若不支持，返回 `unsupported` 错误，不做静默替代。

用户文档必须明确写出：

```text
insert-before is limited by Notion API positioning support and Notion-Version.
When exact insertion is not supported, the command fails explicitly instead of silently appending elsewhere.
```

## 决议 7：Notion-Version 集中配置，不在各模块硬编码

全局配置增加：

```json
{
  "notion_version": "2025-09-03",
  "version_policy": "pinned"
}
```

或在确认项目选择更新版本后：

```json
{
  "notion_version": "2026-03-11",
  "version_policy": "pinned"
}
```

规则：

1. `notion_version` 只能由配置管理层读取。
2. SDK Client 初始化时统一注入 Notion-Version。
3. Core、Route、CLI 不得散落硬编码版本。
4. 每次升级 Notion SDK 或 Notion-Version，必须新增兼容性测试。
5. Docs 记录项目当前测试过的 Notion-Version。
6. 实施前必须重新检查官方 Notion API 文档和 SDK 文档，确认 endpoint、字段和 breaking changes。

版本策略：

- 默认 `pinned`。
- 不默认追随 latest。

原因：

- Notion API 有 breaking changes。
- MCP 工具和 CLI 命令需要稳定行为。
- 自动追随 latest 会导致用户命令行为不稳定。

允许高级用户设置：

```bash
notion-mcp config set notion_version 2026-03-11
```

但必须提示：

```text
Changing Notion-Version can change field names, endpoint behavior, and block positioning semantics.
Run the compatibility tests before using this in production.
```

## 决议 8：Raw API 是兜底，不是常用路径

保留 Raw API：

```bash
notion-mcp raw-api invoke --method GET --path /v1/...
notion-mcp raw-api invoke --method POST --path /v1/... --payload '<json>'
```

Raw API 用于：

- Notion SDK 已支持但 CLI 未封装的低频操作。
- 新 API 临时试验。
- Debug。
- 开发者/高级用户入口。

Raw API 不用于普通用户常用 page/database 编辑路径。

用户文档不得继续把高频 page/database 编辑缺口描述为“使用 raw-api 完成”。新增 v2 常用命令后，应把 raw-api 移到高级章节。

## 决议 9：MCP Tools 与 CLI 分离，但共享 Core

MCP Tools 和 CLI 都不得直接调用 Notion SDK。二者都必须调用 Core。

```text
CLI      -> Core -> Notion SDK/API
MCP Tool -> Core -> Notion SDK/API
```

原因：

- 避免业务逻辑散落。
- 保证 CLI、MCP Tool、测试共享同一行为。
- 便于做权限、错误处理、重试、审计、日志。
- 便于将来添加 HTTP API 或其他入口。

MCP Tool 面向 Agent/LLM，优先结构化、可组合：

```text
page.retrieve
page.create
page.update
page.trash
page.property.retrieve
block.children
block.append
block.update
block.trash
database.retrieve
database.create
database.update
database.sources
data_source.retrieve
data_source.query
data_source.create
data_source.update
data_source.templates
raw.invoke
```

## 决议 10：测试策略

遵循既有规则：

- 不能为了过测试而修改已创建的测试代码。
- 发现测试覆盖不足，只能新增测试，如 `v2`、`v3`。

v2 新增测试目录：

```text
tests/v2/cli/
tests/v2/scenarios/
tests/v2/core/
tests/v2/mcp_tools/
```

必须新增的测试：

- `tests/v2/cli/test_local_config.py`
  - `local init` 创建 `.notion-mcp/config.json`。
  - `local status` 显示当前配置。
  - `local set main_page_id`。
  - `local unset main_page_id`。
  - 从 cwd 向上查找本地配置。
  - 显式 page id 覆盖本地配置。
- `tests/v2/cli/test_page_content.py`
  - `page content` 使用 local `main_page_id`。
  - `page content <page_id>` 覆盖 local `main_page_id`。
  - `--json` 输出结构稳定。
  - `--tree` 递归读取 children。
  - block 摘要、type、id、parent-child 关系输出。
- `tests/v2/cli/test_page_block_edit.py`
  - append。
  - insert-after。
  - update。
  - remove/trash。
  - insert-before unsupported 或 best-effort 行为。
- `tests/v2/cli/test_database_data_source.py`
  - database retrieve。
  - database sources。
  - data-source retrieve。
  - data-source query。
  - data-source update。
  - data-source property rename。
  - database page create 自动解析单 data source。
  - database page create 遇到多 data source 时要求显式 `--data-source`。
- `tests/v2/scenarios/test_local_page_context_workflow.py`
- `tests/v2/scenarios/test_page_content_edit_workflow.py`
- `tests/v2/scenarios/test_database_data_source_workflow.py`

场景测试覆盖：

1. 在目录中执行 `local init`。
2. 执行 `page content` 读取主 page。
3. 在某个 block 后插入新 block。
4. 查询某个 data source。
5. 在 data source 中创建 page。
6. 更新 page properties。

真实 Notion 环境测试可以标记为 integration，并默认跳过：

```python
@pytest.mark.integration
@pytest.mark.skipif(not REAL_NOTION_TOKEN, reason="requires real Notion workspace")
```

## 决议 11：文档同步范围

实施后必须同步以下文档。

用户文档：

- `Docs/User/Configuration.md`
  - 全局配置和本地目录配置的区别。
  - `.notion-mcp/config.json` 的查找规则。
  - 本地配置不保存 token。
  - 绑定当前目录主 page 的示例。
- `Docs/User/Cli.md`
  - `local`。
  - `page content`。
  - `page block`。
  - `page insert`。
  - `database`。
  - `data-source`。
  - database 快捷命令与 data source 的关系。
  - raw-api 从常用路径降级为高级兜底路径。

开发者文档：

- `Docs/Developer/api/cli.md`
  - CLI 到 Core 的调用边界。
  - database/data_source 的命令映射。
  - 本地上下文解析规则。
- `Docs/Developer/mcp_tools/databases.md`
- `Docs/Developer/mcp_tools/data_sources.md`
  - database 容器工具。
  - data_source 表级工具。
  - 不再把 data_source 当作 database 的同义词。
- `Docs/Developer/testing/cli.md`
  - v2 CLI 测试结构。
  - 本地配置测试。
  - page 内容测试。
  - page 内 block 编辑测试。
  - database/data_source 测试。

开发计划与进度：

- `Docs/dev/Feature_Completion_Plan.md`
- `Docs/dev/progress.md`
- `Docs/Requirements.md`
  - Core 覆盖 Notion SDK/API 的原则。
  - database/data_source 分离原则。
  - v2 阶段目标和完成状态。
  - 已推后真实环境测试的项目。

## 决议 12：实施阶段

### v2.0：文档和 ADR 固化

先更新：

- `Docs/dev/ADR-002-local-context-and-cli-v2.md`
- `Docs/Requirements.md`
- `Docs/Developer/api/cli.md`
- `Docs/User/Configuration.md`
- `Docs/User/Cli.md`
- `Docs/dev/progress.md`

目标：

- 固化 database/data_source 语义。
- 固化本地目录配置模型。
- 固化 CLI 分层。
- 明确哪些命令是计划能力，哪些是当前已实现能力。

### v2.1：本地目录配置与上下文解析

实现：

```bash
notion-mcp local init --main-page <page_id>
notion-mcp local status
notion-mcp local set main_page_id <page_id>
notion-mcp local unset main_page_id
```

Core 增加：

```text
LocalConfigStore
ContextResolver
find_local_config_from_cwd()
resolve_main_page_id(explicit_page_id=None)
```

### v2.2：Page 内容读取

实现：

```bash
notion-mcp page content
notion-mcp page content <page_id>
notion-mcp page content --json
notion-mcp page content --tree
```

### v2.3：Page 内 block 编辑

实现稳定能力：

```bash
notion-mcp page block append <block_id> --payload '<json>'
notion-mcp page block insert-after <block_id> --payload '<json>'
notion-mcp page block update <block_id> --payload '<json>'
notion-mcp page block remove <block_id>
```

`insert-before` 不进入 v2.3 稳定范围。

### v2.4：Database/DataSource CLI

实现：

```bash
notion-mcp database retrieve <database_id>
notion-mcp database sources <database_id>
notion-mcp database rename <database_id> <new_name>
notion-mcp data-source retrieve <data_source_id>
notion-mcp data-source query <data_source_id> --payload '<json>'
notion-mcp data-source update <data_source_id> --payload '<json>'
notion-mcp data-source property rename <data_source_id> <property_id_or_name> <new_name>
notion-mcp database page create <database_id_or_data_source_id> --properties '<json>'
notion-mcp database page update <page_id> --properties '<json>'
```

### v2.5：MCP Tool 同步

新增或修正：

```text
database.retrieve
database.create
database.update
database.sources
data_source.retrieve
data_source.query
data_source.create
data_source.update
data_source.templates
```

## 最终决策表

| 议题 | 决策 |
| --- | --- |
| 本地配置文件名 | `.notion-mcp/config.json` |
| token 放哪里 | 只放全局配置，不放本地配置 |
| 当前目录默认上下文 | 从 cwd 向上查找 `.notion-mcp/config.json` |
| 普通用户编辑入口 | page CLI |
| 高级 block 操作入口 | block CLI |
| `data_source` 是否等于 `database` | 不等于 |
| Core 是否只以 data_source 为主 | 否，Core 必须同时建模 database 和 data_source |
| database 是什么 | 容器对象，包含一个或多个 data sources |
| data_source 是什么 | database 下的具体表，承载 schema/properties/query/pages/templates |
| 查询 rows/pages 用哪个 | data_source |
| 修改属性 schema 用哪个 | data_source |
| 创建/管理 database 容器用哪个 | database |
| 用户 CLI 是否仍可叫 database | 可以，但必须提供 data-source 命名空间，并正确解析多 data source 场景 |
| raw-api 定位 | 兜底和高级入口，不作为常用路径 |
| insert-before | 不作为 v2 首批稳定能力 |
| Notion-Version | 全局集中配置，默认 pinned，不在模块中硬编码 |
| 测试策略 | 不改旧测试；新增 `tests/v2/...` |
| 文档策略 | 先 ADR，再同步 User/Developer/Testing/Progress |

## 最小可落地目标

v2 的最小闭环是：

```bash
notion-mcp local init --main-page <page_id>
notion-mcp page content
notion-mcp page block append <block_id> --payload '<json>'
notion-mcp data-source query <data_source_id> --payload '<json>'
notion-mcp database sources <database_id>
```

完成这条链路后，再扩展：

```bash
notion-mcp page block insert-after <block_id> --payload '<json>'
notion-mcp data-source property rename <data_source_id> <property_id_or_name> <new_name>
notion-mcp database page create <database_id_or_data_source_id> --properties '<json>'
notion-mcp page insert database --payload '<json>'
```

## 结论

v2 的主题不是“补几个 CLI 命令”，而是新增一个产品层：

```text
Git-like local Notion context + human-friendly CLI + strict Database/DataSource separation
```

最终设计必须做到：

1. 本地目录绑定 Notion 主 page。
2. 普通用户围绕 page 读取和编辑内容。
3. Block CLI 保留为高级底层入口。
4. Database 和 DataSource 在 Core/API/MCP 层严格分离。
5. 用户 CLI 保留 database 心智，但必须暴露 data-source 命名空间。
6. Raw API 只做兜底。
7. 所有新功能先写测试，再实现，文档随功能同步更新。
