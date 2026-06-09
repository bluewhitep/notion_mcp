# Database DataSource CLI

本文说明 database 和 data source 相关命令。

Database 是 Notion database 容器；DataSource 是 database 下的具体表。

- 容器级操作使用 `database`。
- 显式操作 data source 时使用 `data-source`。
- 使用当前绑定 database 的 active data source 时，才使用 `database` 快捷命令。

## Database 容器命令

| 命令 | 作用 |
| --- | --- |
| `notion-mcp database attach <database_id>` | 把 database 绑定为当前项目默认 database；单 data source 时可自动选择 active data source。 |
| `notion-mcp database attach <database_id> --data-source <id_or_name>` | 绑定 database，并显式选择 active data source。 |
| `notion-mcp database status` | 查看当前项目绑定的 database 和 active data source。 |
| `notion-mcp database refresh` | 重新从 Notion 拉取 database 标题、URL、data sources 和状态，只刷新本地状态，不修改 Notion 远端 database。 |
| `notion-mcp database detach` | 取消本地 database 绑定，不修改 Notion 远端 database。 |
| `notion-mcp database retrieve` | 读取当前绑定 database 容器信息。 |
| `notion-mcp database retrieve <database_id>` | 读取指定 database 容器信息。 |
| `notion-mcp database sources` | 列出当前绑定 database 下的 data sources。 |
| `notion-mcp database sources <database_id>` | 列出指定 database 下的 data sources。 |
| `notion-mcp database create` | 创建 database 容器，并创建 initial data source。 |
| `notion-mcp database create --parent-page <page_id>` | 在指定 parent page 下创建 database 容器和 initial data source。 |
| `notion-mcp database update <database_id>` | 更新 database 容器级信息，例如标题、描述、图标或封面；不修改 data source schema。 |
| `notion-mcp database rename <database_id> <new_name>` | 修改 database 容器标题。 |

示例：

```bash
notion-mcp database attach <database_id> --data-source Tasks
notion-mcp database status
notion-mcp database sources
notion-mcp database create --parent-page <page_id> --payload '{"title": []}'
notion-mcp database update <database_id> --payload '{"title": []}'
```

## Database 快捷命令

这些命令只作用于当前绑定 database 的 active data source。

| 命令 | 作用 |
| --- | --- |
| `notion-mcp database query --payload '<json>'` | 查询当前绑定 database 的 active data source。 |
| `notion-mcp database page create` | 在当前绑定 database 的 active data source 中创建 page/entry。 |
| `notion-mcp database property rename <property> <new_name>` | 重命名当前绑定 active data source 的 property。 |

示例：

```bash
notion-mcp database query --payload '{"page_size": 10}'
notion-mcp database page create --properties '{"Name": {"title": []}}'
notion-mcp database property rename Status State
```

## DataSource 正式命令

| 命令 | 作用 |
| --- | --- |
| `notion-mcp data-source retrieve <data_source_id>` | 读取 data source 表级信息和 schema。 |
| `notion-mcp data-source query <data_source_id>` | 查询指定 data source 中的 entries/pages。 |
| `notion-mcp data-source create` | 在当前绑定 database 下创建新的 data source。 |
| `notion-mcp data-source create <database_id>` | 在指定 database 容器下创建新的 data source。 |
| `notion-mcp data-source update <data_source_id>` | 更新 data source 表级属性或 schema。 |
| `notion-mcp data-source templates <data_source_id>` | 列出 data source 可用 page templates。 |
| `notion-mcp data-source property rename <data_source_id> <property> <new_name>` | 重命名指定 data source property。 |
| `notion-mcp data-source page create <data_source_id>` | 在指定 data source 中创建 page/entry。 |

示例：

```bash
notion-mcp data-source query <data_source_id> --payload '{"page_size": 10}'
notion-mcp data-source create <database_id> --payload '{"name": "Tasks", "properties": {}}'
notion-mcp data-source property rename <data_source_id> Status State
notion-mcp data-source page create <data_source_id> --properties '{"Name": {"title": []}}'
```
