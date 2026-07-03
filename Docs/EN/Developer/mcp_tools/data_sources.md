# Data Source Tools

## Semantic Boundary

Data source tools own table-level capabilities:

- Retrieve a data source.
- Query a data source.
- Create or update a data source.
- List templates.
- Manage schema/properties.
- Create or update entries/pages through the Page/DataSource split.

`data_source` is not a synonym for `database`. A database is the container; a data source is the concrete table under that container. The current CLI/Core/MCP stack includes `templates` and `property rename`.

- `data_source_retrieve`
  - Description: reads a Notion data source.
  - Required parameters: `data_source_id`.
- `data_source_query`
  - Description: queries a Notion data source.
  - Required parameters: `data_source_id`.
  - Optional parameters: `payload`.
- `data_source_create`
  - Description: creates a data source.
  - Required parameters: `payload`.
  - Optional parameters: `database_id`, `dry_run`.
  - Notes: when `database_id` is provided, calls `DataSourcesService.create_for_database()` and creates the data source under that database container; otherwise it uses raw payload create.
- `data_source_update`
  - Description: updates a data source.
  - Required parameters: `data_source_id`, `payload`.
  - Optional parameters: `dry_run`.
- `data_source_templates`
  - Description: lists page templates available to a data source.
  - Required parameters: `data_source_id`.
- `data_source_property_rename`
  - Description: renames a data source property by property ID or current property name.
  - Required parameters: `data_source_id`, `property_id_or_name`, `new_name`.
  - Optional parameters: `dry_run`.

MCP data source tools call `DataSourcesService`. They do not call CLI and do not import the Notion SDK directly. Table-level query/schema/templates/property operations must not be placed under database container tools.
