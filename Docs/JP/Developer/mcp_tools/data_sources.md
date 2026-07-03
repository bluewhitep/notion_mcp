# Data Source Tools

## Semantic boundary

Data source tools は table-level capabilities を担当します。

- data source の retrieve。
- data source の query。
- data source の create/update。
- templates の list。
- schema/properties の管理。
- Page/DataSource split による entry/page creation または update。

`data_source` は `database` の同義語ではありません。database は container、data source はその container 配下の concrete table です。

- `data_source_retrieve`
  - 説明: Notion data source を読み取ります。
  - Required parameters: `data_source_id`.
- `data_source_query`
  - 説明: Notion data source を query します。
  - Required parameters: `data_source_id`.
  - Optional parameters: `payload`.
- `data_source_create`
  - 説明: data source を作成します。
  - Required parameters: `payload`.
  - Optional parameters: `database_id`, `dry_run`.
- `data_source_update`
  - 説明: data source を更新します。
  - Required parameters: `data_source_id`, `payload`.
  - Optional parameters: `dry_run`.
- `data_source_templates`
  - 説明: data source で利用できる page templates を一覧します。
  - Required parameters: `data_source_id`.
- `data_source_property_rename`
  - 説明: property ID または現在の property name で data source property を rename します。
  - Required parameters: `data_source_id`, `property_id_or_name`, `new_name`.
  - Optional parameters: `dry_run`.

MCP data source tools は `DataSourcesService` を呼びます。CLI は呼ばず、Notion SDK を直接 import しません。
