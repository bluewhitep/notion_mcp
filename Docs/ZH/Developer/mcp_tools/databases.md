# Database Tools

## 语义边界

Database tools 必须严格区分 `database` 和 `data_source`：

- `database` 是 Notion database 容器。
- `data_source` 是 database 下的具体表。
- database tools 负责容器级操作，例如 retrieve、create、update、sources。
- 表级 schema、query、templates 和 entries/pages 操作应归入 data source tools。

当前 CLI/Core/MCP 已实现 database 容器级 `retrieve/create/update/sources/rename`。`database_query` 仍保留为 legacy 兼容入口，但通过 Core Raw API 兼容路径调用 `databases.query`；新的表级查询应优先使用 `data_source_query`。

- `database_retrieve`
  - 说明：读取 Notion database 容器。
  - 必选参数：`database_id`。
- `database_sources`
  - 说明：列出 database 容器下的 data sources。
  - 必选参数：`database_id`。
- `database_query`
  - 说明：legacy database query 兼容入口。新表级查询优先使用 `data_source_query`。
  - 必选参数：`database_id`。
  - 可选参数：`payload`。
- `database_create`
  - 说明：创建 Notion database 容器。
  - 必选参数：`payload`。
  - 可选参数：`dry_run`。
- `database_update`
  - 说明：更新 Notion database 容器。
  - 必选参数：`database_id`、`payload`。
  - 可选参数：`dry_run`。
- `database_rename`
  - 说明：重命名 Notion database 容器。
  - 必选参数：`database_id`、`new_name`。
  - 可选参数：`dry_run`。

MCP database tools 调用 `DatabasesService`，不调用 CLI，也不直接导入 Notion SDK。`database_sources` 返回结构为：

```json
{
  "database_id": "database-id",
  "data_sources": []
}
```
