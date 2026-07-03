# Database Tools

## Semantic boundary

Database tools は `database` と `data_source` を明確に分けます。

- `database` は Notion database container です。
- `data_source` は database 配下の concrete table です。
- Database tools は retrieve、create、update、sources、rename など container-level operations を担当します。
- Table-level schema、query、templates、entries/pages は data source tools に属します。

`database_query` は legacy compatibility entrypoint として残ります。新しい table-level query では `data_source_query` を優先します。

- `database_retrieve`
  - 説明: Notion database container を読み取ります。
  - Required parameters: `database_id`.
- `database_sources`
  - 説明: database container 配下の data sources を一覧します。
  - Required parameters: `database_id`.
- `database_query`
  - 説明: legacy database query compatibility entrypoint。
  - Required parameters: `database_id`.
  - Optional parameters: `payload`.
- `database_create`
  - 説明: Notion database container を作成します。
  - Required parameters: `payload`.
  - Optional parameters: `dry_run`.
- `database_update`
  - 説明: Notion database container を更新します。
  - Required parameters: `database_id`, `payload`.
  - Optional parameters: `dry_run`.
- `database_rename`
  - 説明: Notion database container を rename します。
  - Required parameters: `database_id`, `new_name`.
  - Optional parameters: `dry_run`.

MCP database tools は `DatabasesService` を呼びます。CLI は呼ばず、Notion SDK を直接 import しません。
