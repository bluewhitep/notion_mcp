# Data Source Tools

## 语义边界

Data source tools 承担表级能力：

- retrieve data source。
- query data source。
- create/update data source。
- list templates。
- 管理 schema/properties。
- 在 data source 中创建或更新 entry/page 的相关能力通过 Page/DataSource 分层实现。

`data_source` 不是 `database` 的同义词。`database` 是容器，`data_source` 是该容器下的具体表。当前 CLI/Core/MCP 已实现 `templates` 和 `property rename`。

- `data_source_retrieve`
  - 说明：读取 Notion data source。
  - 必选参数：`data_source_id`。
- `data_source_query`
  - 说明：查询 Notion data source。
  - 必选参数：`data_source_id`。
  - 可选参数：`payload`。
- `data_source_create`
  - 说明：创建 data source。
  - 必选参数：`payload`。
  - 可选参数：`database_id`、`dry_run`。
  - 备注：传入 `database_id` 时调用 `DataSourcesService.create_for_database()`，在指定 database 容器下创建 data source；未传时调用 raw payload create。
- `data_source_update`
  - 说明：更新 data source。
  - 必选参数：`data_source_id`、`payload`。
  - 可选参数：`dry_run`。
- `data_source_templates`
  - 说明：列出 data source 可用 page templates。
  - 必选参数：`data_source_id`。
- `data_source_property_rename`
  - 说明：按 property id 或当前 property 名称重命名 data source property。
  - 必选参数：`data_source_id`、`property_id_or_name`、`new_name`。
  - 可选参数：`dry_run`。

MCP data source tools 调用 `DataSourcesService`，不调用 CLI，也不直接导入 Notion SDK。表级 query/schema/templates/property 操作不得放入 database container tool。
