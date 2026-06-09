# ADR-003: .notion_mcp 项目级配置与 Page/Database Attach 工作流

## 状态

Design Accepted / 待实现。

本文描述新的 CLI runtime 工作流设计。本文是待实现设计文档，不表示当前 CLI 已经具备这些命令。当前已实现命令仍以源码、`Docs/User/Cli.md` 和 `Docs/Developer/api/cli.md` 为准。

## 目标

本设计要解决当前 Notion MCP CLI 使用时的主要问题：

1. 每次 page 操作都需要输入 page id，使用成本高。
2. 每次 database 操作都需要输入 database id 或 data source id，使用成本高。
3. CLI 缺少类似 Git 的“当前项目上下文”。
4. 用户需要一个清晰的本地状态文件，能查看当前 attach 的 page/database 信息。
5. 本地项目配置和全局认证配置需要隔离，避免 token 写入项目目录。

因此，本设计引入项目级 `.notion_mcp` 目录，并新增 page/database attach 工作流。

## 与 ADR-002 的关系

ADR-003 继承 ADR-002 的以下决策：

- 全局配置和项目级配置分离。
- token 只保存在全局配置，不写入项目目录。
- CLI 从当前目录向上查找项目配置。
- Page CLI 是普通用户读取和编辑页面内容的主入口。
- Database 和 DataSource 必须严格区分。
- Raw API 是兜底和高级入口，不作为常用 attach 工作流路径。

ADR-003 覆盖 ADR-002 的项目级目录命名：

- ADR-002 早期命名：`.notion-mcp/config.json`
- ADR-003 最终命名：`.notion_mcp/config.json`

后续实现 project context 和 attach workflow 时，以 ADR-003 为准。

## 核心决策摘要

| 议题 | 决策 |
| --- | --- |
| 项目级目录名 | `.notion_mcp` |
| 项目级配置文件 | `.notion_mcp/config.json` |
| 项目级状态目录 | `.notion_mcp/state/` |
| Page attach 状态文件 | `.notion_mcp/state/page.attach.json` |
| Database attach 状态文件 | `.notion_mcp/state/database.attach.json` |
| token 是否写入项目目录 | 不允许 |
| CLI 是否自动查找项目配置 | 是，从当前目录向上查找 |
| page 操作默认对象 | 显式 page id > attach page > 报错 |
| database 操作默认对象 | 显式 id > attach database/data_source > 报错 |
| detach 命令名 | 标准命令用 `detach`，兼容别名 `deattach` |
| database attach 是否只保存 database_id | 否，同时保存 database 信息和 active data_source 信息 |
| raw-api 定位 | 兜底，不作为常用 attach 工作流路径 |

## 术语

### Global Config

全局配置位于用户主目录：

```text
~/.notion_mcp/config.json
```

用于保存认证和运行参数：

```json
{
  "notion_token": "secret_xxx_or_ntn_xxx",
  "user_id": "notion-user-uuid",
  "notion_version": "2025-09-03",
  "timeout_ms": 60000,
  "retry": {
    "max_retries": 2,
    "initial_retry_delay_ms": 1000,
    "max_retry_delay_ms": 60000
  }
}
```

全局配置可以通过环境变量覆盖路径：

```bash
NOTION_MCP_CONFIG=/custom/path/config.json
```

### Project Config

项目级配置位于项目目录：

```text
<project-root>/.notion_mcp/config.json
```

项目配置不保存 token，只保存项目上下文和 runtime 行为设置。

示例：

```json
{
  "schema_version": 1,
  "project_name": "optional-project-name",
  "workspace_hint": "optional-human-readable-workspace-name",
  "created_at": "2026-06-08T00:00:00Z",
  "updated_at": "2026-06-08T00:00:00Z",
  "settings": {
    "prefer_attached_page": true,
    "prefer_attached_database": true,
    "json_output_default": false
  }
}
```

### Attach State

Attach state 是当前项目中“当前默认 Notion 对象”的状态文件。

Page attach 后创建：

```text
.notion_mcp/state/page.attach.json
```

Database attach 后创建：

```text
.notion_mcp/state/database.attach.json
```

Detach 后删除对应状态文件，或将其标记为 detached。默认策略：删除状态文件。

## 目录结构设计

项目根目录中新增：

```text
.notion_mcp/
  config.json
  state/
    page.attach.json
    database.attach.json
  cache/
  logs/
  .gitignore
```

- `.notion_mcp/config.json`：项目级配置文件，不保存 token。
- `.notion_mcp/state/page.attach.json`：保存当前 attach 的 page 信息。
- `.notion_mcp/state/database.attach.json`：保存当前 attach 的 database 信息，以及必要时保存 active data_source 信息。
- `.notion_mcp/cache/`：未来用于缓存 page tree、block tree、database schema、data source schema；v1 不强制实现。
- `.notion_mcp/logs/`：未来用于本地 CLI 操作日志或审计日志；v1 不强制实现。

`.notion_mcp/.gitignore` 默认创建：

```gitignore
state/
cache/
logs/
```

原因：

- attach state 是本地 runtime 状态，不一定应该提交到 git。
- 不保存 token，但 page/database id 和 title 也可能暴露项目信息。
- 如果团队希望共享 attach 配置，可以手动调整 `.gitignore` 策略。

## 项目配置发现规则

CLI runtime 行为类似 Git。当用户在任意目录执行命令时，CLI 按以下顺序查找项目配置：

1. 从当前工作目录 cwd 开始。
2. 检查当前目录是否存在 `.notion_mcp/config.json`。
3. 如果不存在，继续向父目录查找。
4. 一直查找到文件系统根目录。
5. 找到第一个 `.notion_mcp/config.json` 的目录即为 project root。
6. 如果未找到：
   - 对于 `project init`、`page attach`、`database attach`，可以创建 `.notion_mcp`。
   - 对于需要默认上下文的命令，返回明确错误。

查找示例：

```text
/workspace/my-project/.notion_mcp/config.json
/workspace/my-project/src/module
```

执行：

```bash
cd /workspace/my-project/src/module
notion-mcp page content
```

CLI 应自动找到：

```text
/workspace/my-project/.notion_mcp/config.json
```

并读取：

```text
/workspace/my-project/.notion_mcp/state/page.attach.json
```

未来可支持：

```bash
notion-mcp --project /path/to/project page content
```

优先级：

```text
--project 显式路径 > cwd 向上查找
```

v1 可暂不实现 `--project`，但设计上保留。

## Project Init 工作流

推荐标准命令：

```bash
notion-mcp project init
```

兼容别名：

```bash
notion-mcp local init
```

执行后在当前目录创建：

```text
.notion_mcp/
  config.json
  state/
  cache/
  logs/
  .gitignore
```

如果已存在 `.notion_mcp/config.json`，默认报错：

```text
Project already initialized: /path/.notion_mcp/config.json
```

允许覆盖：

```bash
notion-mcp project init --force
```

初始化配置示例：

```json
{
  "schema_version": 1,
  "project_name": null,
  "workspace_hint": null,
  "created_at": "2026-06-08T00:00:00Z",
  "updated_at": "2026-06-08T00:00:00Z",
  "settings": {
    "prefer_attached_page": true,
    "prefer_attached_database": true,
    "json_output_default": false
  }
}
```

## Page Attach 工作流

用户 attach 一个 Notion page 后，后续 page 操作默认使用该 page，不再要求每次输入 page id。

命令：

```bash
notion-mcp page attach <page_id>
notion-mcp page attach <page_id> --title "Project Home"
notion-mcp page attach <page_id> --verify
notion-mcp page attach <page_id> --no-verify
notion-mcp page attach <page_id> --init
```

默认行为：

- 如果当前目录或上级目录已存在 `.notion_mcp/config.json`，使用已发现的 project root。
- 如果不存在，默认在当前目录创建 `.notion_mcp/config.json`。

原因：attach 的目的就是建立本地项目上下文，不应要求用户额外先执行 `project init`。

可选严格模式：

```bash
notion-mcp page attach <page_id> --require-project
```

如果没有项目配置，则报错。

Attach 时默认访问 Notion API 验证 page，并读取 page 名称。默认等价于：

```bash
notion-mcp page attach <page_id> --verify
```

如果用户离线或想快速写入状态，可使用：

```bash
notion-mcp page attach <page_id> --no-verify --title "Manual Title"
```

Page attach 状态文件路径：

```text
.notion_mcp/state/page.attach.json
```

验证模式示例：

```json
{
  "schema_version": 1,
  "kind": "page_attach",
  "status": "attached",
  "page": {
    "id": "notion-page-id",
    "title": "Project Home",
    "url": "https://www.notion.so/...",
    "parent": {
      "type": "workspace",
      "id": null
    },
    "archived": false,
    "in_trash": false
  },
  "attached_at": "2026-06-08T00:00:00Z",
  "updated_at": "2026-06-08T00:00:00Z",
  "verified_at": "2026-06-08T00:00:00Z",
  "source": {
    "created_by": "cli",
    "command": "notion-mcp page attach"
  }
}
```

`--no-verify` 示例：

```json
{
  "schema_version": 1,
  "kind": "page_attach",
  "status": "attached",
  "page": {
    "id": "notion-page-id",
    "title": "Manual Title",
    "url": null,
    "parent": null,
    "archived": null,
    "in_trash": null
  },
  "attached_at": "2026-06-08T00:00:00Z",
  "updated_at": "2026-06-08T00:00:00Z",
  "verified_at": null,
  "source": {
    "created_by": "cli",
    "command": "notion-mcp page attach --no-verify"
  }
}
```

## Page Status / Refresh / Detach 工作流

命令：

```bash
notion-mcp page status
notion-mcp page current
notion-mcp page attached
notion-mcp page status --json
notion-mcp page status --refresh
notion-mcp page refresh
notion-mcp page detach
notion-mcp page deattach
```

`page status` 读取当前项目的 `.notion_mcp/state/page.attach.json`，输出当前 attach page 信息。

人类输出示例：

```text
Attached page
Project root:
  /workspace/my-project
State file:
  /workspace/my-project/.notion_mcp/state/page.attach.json
Page:
  Title: Project Home
  ID: notion-page-id
  URL: https://www.notion.so/...
  Archived: false
  In trash: false
Attached at:
  2026-06-08T00:00:00Z
Verified at:
  2026-06-08T00:00:00Z
```

JSON 输出示例：

```json
{
  "project_root": "/workspace/my-project",
  "state_file": "/workspace/my-project/.notion_mcp/state/page.attach.json",
  "attachment": {
    "schema_version": 1,
    "kind": "page_attach",
    "status": "attached",
    "page": {
      "id": "notion-page-id",
      "title": "Project Home"
    }
  }
}
```

Refresh 重新从 Notion API 拉取标题、URL、trash 状态，并更新：

- `verified_at`
- `updated_at`
- `page.title`
- `page.url`
- `page.archived`
- `page.in_trash`

Detach 默认删除：

```text
.notion_mcp/state/page.attach.json
```

`deattach` 是兼容别名。Detach 只修改本地状态，不修改 Notion，不删除、trash、修改远端 page，也不取消 integration 权限。

## Page 操作中的默认 page 解析

对于 page 命令：

```text
显式 page_id > attached page > 报错
```

示例：

```bash
notion-mcp page content <page_id>
```

使用显式 `<page_id>`。

```bash
notion-mcp page content
```

使用 attach 状态中的 page id。

如果未 attach：

```text
No page is attached for this project.
Run:
  notion-mcp page attach <page_id>
Or pass page_id explicitly:
  notion-mcp page content <page_id>
```

以下命令支持省略 page id：

```bash
notion-mcp page content
notion-mcp page blocks
notion-mcp page tree
notion-mcp page insert page --payload '<json>'
notion-mcp page insert database --payload '<json>'
```

以下命令仍然需要 block id，因为 block id 是具体编辑位置：

```bash
notion-mcp page block update <block_id> --payload '<json>'
notion-mcp page block append <block_id> --payload '<json>'
notion-mcp page block insert-after <block_id> --payload '<json>'
notion-mcp page block remove <block_id>
```

这些命令使用 attached page 的意义是：

- 用于校验 block 是否属于当前 attached page。
- 用于输出上下文。
- 用于避免误操作其他 page 的 block。

默认校验策略：

- 如果能高效验证 block 属于 attached page，则验证。
- 如果需要大量递归查询，默认不强制验证，可提供 `--strict-page-check`。

## Database Attach 工作流

Notion API 中，database 和 data_source 不是同一个对象：

- database 是容器。
- data_source 是 database 下的具体表。
- 查询 rows/pages、修改 properties schema、创建 database page 等表级操作通常需要 data_source。

因此，database attach 状态必须能表达：

- attached database container
- active data source

如果一个 database 只有一个 data_source，可以自动选择该 data_source。如果一个 database 有多个 data_sources，必须显式指定 active data_source，不能静默选择。

命令：

```bash
notion-mcp database attach <database_id>
notion-mcp database attach <database_id> --data-source <data_source_id_or_name>
notion-mcp database attach <database_id> --verify
notion-mcp database attach <database_id> --no-verify --title "Tasks"
notion-mcp database attach <database_id> --init
```

为了方便用户，也允许直接 attach data source：

```bash
notion-mcp database attach --data-source <data_source_id>
```

未来可考虑独立命令：

```bash
notion-mcp data-source attach <data_source_id>
```

但 v1 推荐先实现：

```bash
notion-mcp database attach <database_id> --data-source <data_source_id_or_name>
```

避免命令面过大。

Attach 时默认访问 Notion API：

1. retrieve database。
2. 读取 database title。
3. 读取 database 下 data_sources 列表。
4. 如果 data_sources 数量为 1，自动设为 active_data_source。
5. 如果数量大于 1 且未传 `--data-source`，报错并列出候选项。
6. 如果传入 `--data-source`，按 id 或 name 匹配。
7. 写入 `.notion_mcp/state/database.attach.json`。

多 data source 错误示例：

```text
This database contains multiple data sources.
Database:
  Project Database
  database-id
Data sources:
  1. Tasks     data-source-id-1
  2. Bugs      data-source-id-2
  3. Archive   data-source-id-3
Please attach again with:
  notion-mcp database attach <database_id> --data-source <data_source_id_or_name>
```

## Database Attach 状态文件

路径：

```text
.notion_mcp/state/database.attach.json
```

示例：

```json
{
  "schema_version": 1,
  "kind": "database_attach",
  "status": "attached",
  "database": {
    "id": "notion-database-id",
    "title": "Project Database",
    "url": "https://www.notion.so/...",
    "is_inline": false,
    "archived": false,
    "in_trash": false
  },
  "active_data_source": {
    "id": "notion-data-source-id",
    "name": "Tasks",
    "parent_database_id": "notion-database-id"
  },
  "available_data_sources": [
    {
      "id": "notion-data-source-id",
      "name": "Tasks"
    }
  ],
  "attached_at": "2026-06-08T00:00:00Z",
  "updated_at": "2026-06-08T00:00:00Z",
  "verified_at": "2026-06-08T00:00:00Z",
  "source": {
    "created_by": "cli",
    "command": "notion-mcp database attach"
  }
}
```

如果 `--no-verify`，只允许保存有限信息：

```json
{
  "schema_version": 1,
  "kind": "database_attach",
  "status": "attached",
  "database": {
    "id": "notion-database-id",
    "title": "Manual Database Title",
    "url": null,
    "is_inline": null,
    "archived": null,
    "in_trash": null
  },
  "active_data_source": null,
  "available_data_sources": [],
  "attached_at": "2026-06-08T00:00:00Z",
  "updated_at": "2026-06-08T00:00:00Z",
  "verified_at": null,
  "source": {
    "created_by": "cli",
    "command": "notion-mcp database attach --no-verify"
  }
}
```

如果没有 active_data_source，以下操作必须报错：

- query
- page create in database
- property rename/update
- templates

错误示例：

```text
Attached database has no active data source.
Run:
  notion-mcp database status --refresh
Or set active data source:
  notion-mcp database attach <database_id> --data-source <data_source_id_or_name>
```

## Database Status / Refresh / Detach 工作流

命令：

```bash
notion-mcp database status
notion-mcp database current
notion-mcp database attached
notion-mcp database status --json
notion-mcp database status --refresh
notion-mcp database refresh
notion-mcp database detach
notion-mcp database deattach
```

Status 输出当前 attach database、active data source、available data sources、project root 和 state file。

Refresh 更新：

- database title
- database URL
- archived/in_trash
- available data_sources
- active_data_source 是否仍存在
- `verified_at`
- `updated_at`

Detach 默认删除：

```text
.notion_mcp/state/database.attach.json
```

只影响本地状态，不影响 Notion 远端。

## Database 操作中的默认对象解析

对于 database 容器级操作：

```text
显式 database_id > attached database.database.id > 报错
```

对于 data source 表级操作：

```text
显式 data_source_id > attached database.active_data_source.id > 报错
```

支持 attach 后省略 id：

```bash
notion-mcp database query --payload '<json>'
notion-mcp database page create --properties '<json>'
notion-mcp database retrieve
```

省略时分别使用：

- `active_data_source.id`
- `active_data_source.id`
- `database.id`

## CLI 命令总表

Project 命令：

```bash
notion-mcp project init
notion-mcp project status
notion-mcp project root
notion-mcp local init
notion-mcp local status
notion-mcp local root
```

Page attach 命令：

```bash
notion-mcp page attach <page_id>
notion-mcp page status
notion-mcp page current
notion-mcp page refresh
notion-mcp page detach
notion-mcp page deattach
```

Page 操作命令：

```bash
notion-mcp page content
notion-mcp page content <page_id>
notion-mcp page content --json
notion-mcp page content --tree
notion-mcp page block update <block_id> --payload '<json>'
notion-mcp page block append <block_id> --payload '<json>'
notion-mcp page block insert-after <block_id> --payload '<json>'
notion-mcp page block remove <block_id>
notion-mcp page insert page --payload '<json>'
notion-mcp page insert database --payload '<json>'
```

Database attach 命令：

```bash
notion-mcp database attach <database_id>
notion-mcp database attach <database_id> --data-source <data_source_id_or_name>
notion-mcp database status
notion-mcp database current
notion-mcp database refresh
notion-mcp database detach
notion-mcp database deattach
```

Database/DataSource 操作命令：

```bash
notion-mcp database retrieve
notion-mcp database retrieve <database_id>
notion-mcp database sources
notion-mcp database sources <database_id>
notion-mcp database query --payload '<json>'
notion-mcp database query <data_source_id> --payload '<json>'
notion-mcp database page create --properties '<json>'
notion-mcp database page create <data_source_id> --properties '<json>'
notion-mcp database page update <page_id> --properties '<json>'
notion-mcp database property rename <property_id_or_name> <new_name>
notion-mcp database property rename <data_source_id> <property_id_or_name> <new_name>
```

显式 DataSource 命名空间：

```bash
notion-mcp data-source retrieve <data_source_id>
notion-mcp data-source query <data_source_id> --payload '<json>'
notion-mcp data-source update <data_source_id> --payload '<json>'
notion-mcp data-source templates <data_source_id>
notion-mcp data-source property rename <data_source_id> <property_id_or_name> <new_name>
```

## 典型用户工作流

初始化项目并 attach page：

```bash
cd my-project
notion-mcp page attach <page_id>
notion-mcp page status
notion-mcp page content
```

执行后目录：

```text
my-project/
  .notion_mcp/
    config.json
    state/
      page.attach.json
```

后续 page 操作不再输入 page id：

```bash
notion-mcp page content
notion-mcp page content --tree
notion-mcp page block append <block_id> --payload '<json>'
```

Detach page：

```bash
notion-mcp page detach
```

Attach database：

```bash
notion-mcp database attach <database_id>
notion-mcp database status
notion-mcp database attach <database_id> --data-source Tasks
```

后续 database 操作不再输入 id：

```bash
notion-mcp database query --payload '<json>'
notion-mcp database page create --properties '<json>'
notion-mcp database sources
```

## 错误处理设计

未找到项目配置：

```text
No .notion_mcp/config.json found from current directory or its parents.
Run:
  notion-mcp project init
Or attach a page, which will initialize project context:
  notion-mcp page attach <page_id>
```

未 attach page：

```text
No page is attached for this project.
Run:
  notion-mcp page attach <page_id>
Or pass page_id explicitly:
  notion-mcp page content <page_id>
```

未 attach database：

```text
No database is attached for this project.
Run:
  notion-mcp database attach <database_id>
Or pass id explicitly:
  notion-mcp database retrieve <database_id>
```

Attached database 缺少 active data source：

```text
Attached database has no active data source.
This command requires a data source.
Run:
  notion-mcp database status --refresh
Or:
  notion-mcp database attach <database_id> --data-source <data_source_id_or_name>
```

远端对象无法访问：

```text
Attached page cannot be retrieved.
Possible reasons:
  - The page was deleted or moved to trash.
  - The Notion integration has no access to this page.
  - The configured Notion token is invalid.
  - The stored page id is incorrect.
Run:
  notion-mcp page detach
Or attach a different page:
  notion-mcp page attach <page_id>
```

## Core 设计

建议新增：

```text
src/notion_mcp/core/project/
  project_config.py
  project_resolver.py
  project_paths.py
src/notion_mcp/core/attachments/
  page_attachment.py
  database_attachment.py
  attachment_store.py
  context_resolver.py
src/notion_mcp/core/notion/
  pages.py
  blocks.py
  databases.py
  data_sources.py
```

ProjectResolver 职责：

- `find_project_root(cwd)`
- `find_project_config(cwd)`
- `ensure_project(cwd)`
- `init_project(cwd)`

AttachmentStore 职责：

- `load_page_attachment(project_root)`
- `save_page_attachment(project_root, attachment)`
- `delete_page_attachment(project_root)`
- `load_database_attachment(project_root)`
- `save_database_attachment(project_root, attachment)`
- `delete_database_attachment(project_root)`

ContextResolver 职责：

- `resolve_page_id(explicit_page_id=None)`
- `resolve_database_id(explicit_database_id=None)`
- `resolve_data_source_id(explicit_data_source_id=None)`

解析规则：

```text
explicit > attachment > error
```

## 写文件规则

所有 `.notion_mcp` 状态文件写入必须使用原子写入：

1. 写入临时文件，例如 `page.attach.json.tmp`。
2. fsync。
3. rename 到正式文件，例如 `page.attach.json`。

避免命令中断导致 JSON 损坏。

JSON 格式：

- UTF-8
- 2 spaces indent
- 末尾换行
- 字段顺序稳定，方便 diff

权限：

- 全局配置：`0600`
- 项目配置和状态：`0644`

因为项目配置不保存 token。但如果用户希望更严格，可提供：

```bash
notion-mcp project init --private
```

将项目 `.notion_mcp` 文件设置为 `0600`。

## 安全设计

项目目录 `.notion_mcp` 中不得保存：

- Notion token
- OAuth refresh token
- 用户私钥
- 任何长期认证凭据

项目目录 `.notion_mcp` 可以保存：

- page id
- page title
- page url
- database id
- database title
- data source id
- data source name
- attach 时间
- verified 时间

`project init` 后应提示：

```text
Created .notion_mcp/.
This directory stores project-local Notion context.
It does not store Notion tokens.
By default, runtime state/cache/logs are ignored by .notion_mcp/.gitignore.
```

## 测试设计

遵循项目既有规则：

- 先写测试，再写实现。
- 不能为了过测试而修改已创建的测试代码。
- 发现覆盖不足，只能新增测试，例如 v2、v3。

新增测试目录：

```text
tests/v3/cli/
tests/v3/core/
tests/v3/scenarios/
```

这里使用 v3 是为了区别此前 v2 的 database/data_source 决议和 CLI 扩展测试。

Project 配置测试：

- `tests/v3/core/test_project_resolver.py`
- `tests/v3/cli/test_project_init.py`

覆盖：

- 当前目录创建 `.notion_mcp/config.json`。
- 从子目录向上查找 project root。
- 未找到配置时返回明确错误。
- 重复 init 默认报错。
- `--force` 覆盖。
- `.notion_mcp/.gitignore` 创建。

Page Attach 测试：

- `tests/v3/cli/test_page_attach.py`
- `tests/v3/core/test_page_attachment_store.py`

覆盖：

- `page attach <page_id>` 创建 state 文件。
- `page attach --no-verify --title`。
- `page status`。
- `page status --json`。
- `page refresh`。
- `page detach`。
- `page deattach` alias。
- attach 后 `page content` 可省略 page id。
- 显式 page id 覆盖 attach。

Database Attach 测试：

- `tests/v3/cli/test_database_attach.py`
- `tests/v3/core/test_database_attachment_store.py`

覆盖：

- `database attach <database_id>` 创建 state 文件。
- 单 data source 自动选择 active_data_source。
- 多 data source 未指定时报错。
- 多 data source 指定 `--data-source` 成功。
- `database status`。
- `database status --json`。
- `database refresh`。
- `database detach`。
- `database deattach` alias。
- attach 后 `database query` 可省略 data_source_id。
- 显式 data_source_id 覆盖 attach。

场景测试：

- `tests/v3/scenarios/test_attach_page_workflow.py`
- `tests/v3/scenarios/test_attach_database_workflow.py`
- `tests/v3/scenarios/test_project_context_discovery.py`

真实 Notion 环境测试单独标记：

```python
@pytest.mark.integration
```

默认跳过，只有设置环境变量时执行：

```bash
NOTION_MCP_RUN_INTEGRATION=1
NOTION_TOKEN=...
```

## 文档同步要求

实现后必须同步以下文档。

用户文档：

- `Docs/User/Configuration.md`
  - 全局配置 `~/.notion_mcp/config.json`。
  - 项目配置 `.notion_mcp/config.json`。
  - attach state 文件。
  - token 不写入项目目录。
  - cwd 向上查找规则。
- `Docs/User/Cli.md`
  - project init/status/root。
  - page attach/status/current/refresh/detach/deattach。
  - attach 后 page 命令如何省略 page id。
  - database attach/status/current/refresh/detach/deattach。
  - attach 后 database 命令如何省略 id。
  - database 与 data_source 的用户解释。

开发者文档：

- `Docs/Developer/api/cli.md`
  - CLI context resolution。
  - ProjectResolver。
  - AttachmentStore。
  - ContextResolver。
  - `explicit id > attachment > error` 的解析规则。
- `Docs/Developer/testing/cli.md`
  - v3 attach workflow 测试说明。
  - mock Notion client 测试策略。
  - integration 测试策略。
- `Docs/dev/progress.md`
  - 阶段计划。
  - 已完成命令。
  - 测试结果。
  - 推迟的真实环境测试。

## 实施阶段

### Phase 1：文档和测试骨架

创建或更新：

- `Docs/dev/ADR-003-project-attach-context.md`
- `Docs/User/Configuration.md`
- `Docs/User/Cli.md`
- `Docs/Developer/api/cli.md`
- `Docs/Developer/testing/cli.md`
- `Docs/dev/progress.md`

新增测试骨架：

- `tests/v3/core/`
- `tests/v3/cli/`
- `tests/v3/scenarios/`

### Phase 2：Project 配置

实现：

- ProjectResolver
- ProjectConfigStore
- `project init`
- `project status`
- `project root`

### Phase 3：Page Attach

实现：

- PageAttachmentStore
- `page attach`
- `page status`
- `page refresh`
- `page detach`
- `page deattach` alias
- `page content` 使用 attached page

### Phase 4：Database Attach

实现：

- DatabaseAttachmentStore
- `database attach`
- `database status`
- `database refresh`
- `database detach`
- `database deattach` alias
- `database query` 使用 active data source
- `database page create` 使用 active data source

### Phase 5：场景测试和文档收敛

完成：

- `tests/v3/scenarios/`
- `Docs/User/Cli.md`
- `Docs/User/Configuration.md`
- `Docs/dev/progress.md`

## 最小可交付闭环

最小可交付版本必须完成：

```bash
cd my-project
notion-mcp page attach <page_id>
notion-mcp page status
notion-mcp page content
notion-mcp page detach
notion-mcp database attach <database_id> --data-source <data_source_id_or_name>
notion-mcp database status
notion-mcp database query --payload '<json>'
notion-mcp database detach
```

并确保：

```bash
cd my-project/sub/dir
notion-mcp page content
```

仍能自动发现：

```text
my-project/.notion_mcp/config.json
```

## 非目标

本设计不负责：

- 修改 Notion 远端权限。
- 删除或 trash Notion page/database。
- 把 attach 状态同步到远端。
- 解决多用户共享同一个 `.notion_mcp/state` 的冲突。
- 实现完整本地缓存和索引。
- 实现 OAuth。
- 实现 GUI。

这些能力可作为后续设计单独讨论。

## 最终结论

本工作流的核心是：

```text
项目目录 .notion_mcp + page/database attach state + Git-like cwd discovery
```

最终用户体验应变为：

```bash
cd my-project
notion-mcp page attach <page_id>
notion-mcp page content
```

而不是：

```bash
notion-mcp page content <page_id>
```

database 同理：

```bash
cd my-project
notion-mcp database attach <database_id> --data-source Tasks
notion-mcp database query --payload '<json>'
```

而不是每次输入 database/data_source id。

该设计保留 Notion API 的正确对象边界：

```text
database = 容器
data_source = 具体表
page = 页面或表项
block = 页面内容节点
```

同时为人类 CLI 提供更接近 Git 的本地项目上下文体验。
