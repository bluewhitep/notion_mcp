# Database Tools

## Semantic Boundary

Database tools must keep `database` and `data_source` distinct:

- `database` is the Notion database container.
- `data_source` is the concrete table under that database.
- Database tools own container-level operations such as retrieve, create, update, sources, and rename.
- Table-level schema, query, templates, entries, and pages belong to data source tools.

The current CLI/Core/MCP stack implements container-level `retrieve/create/update/sources/rename`. `database_query` remains as a legacy compatibility entrypoint through the Core Raw API compatibility path for `databases.query`; new table-level queries should prefer `data_source_query`.

- `database_retrieve`
  - Description: reads a Notion database container.
  - Required parameters: `database_id`.
- `database_sources`
  - Description: lists data sources under a database container.
  - Required parameters: `database_id`.
- `database_query`
  - Description: legacy database query compatibility entrypoint. Prefer `data_source_query` for new table-level queries.
  - Required parameters: `database_id`.
  - Optional parameters: `payload`.
- `database_create`
  - Description: creates a Notion database container.
  - Required parameters: `payload`.
  - Optional parameters: `dry_run`.
- `database_update`
  - Description: updates a Notion database container.
  - Required parameters: `database_id`, `payload`.
  - Optional parameters: `dry_run`.
- `database_rename`
  - Description: renames a Notion database container.
  - Required parameters: `database_id`, `new_name`.
  - Optional parameters: `dry_run`.

MCP database tools call `DatabasesService`. They do not call CLI and do not import the Notion SDK directly. `database_sources` returns:

```json
{
  "database_id": "database-id",
  "data_sources": []
}
```
