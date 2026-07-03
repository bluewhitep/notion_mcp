# MCP Tools 開発者ドキュメント

これは MCP tool documentation の入口です。Repository は `src/nilo/mcp_server/` を実装し、MCP Python SDK `FastMCP` 経由で local tools を expose します。

## Server

- Server factory: `src/nilo/mcp_server/server.py`
- Package entry: `nilo.mcp_server:create_mcp_server`
- CLI stdio entry: `nilo server stdio`
- CLI background HTTP entry: `nilo server run --host 127.0.0.1 --port 8000`
- Supported transports: `stdio`, `streamable-http`

## Tool domain documents

- `config.md`
- `auth.md`
- `pages.md`
- `blocks.md`
- `databases.md`
- `data_sources.md`
- `users.md`
- `comments.md`
- `views.md`
- `file_uploads.md`
- `search.md`
- `custom_emojis.md`
- `raw_api.md`

## Tool inventory

Current server は 46 tools を expose します。

- `auth_validate`
- `auth_whoami`
- `block_append`
- `block_children_list`
- `block_trash`
- `block_update`
- `comment_create`
- `comment_list`
- `comment_reply`
- `config_get`
- `config_status`
- `custom_emoji_list`
- `custom_emoji_retrieve`
- `data_source_create`
- `data_source_property_rename`
- `data_source_query`
- `data_source_retrieve`
- `data_source_templates`
- `data_source_update`
- `database_create`
- `database_query`
- `database_rename`
- `database_retrieve`
- `database_sources`
- `database_update`
- `file_upload_complete`
- `file_upload_create`
- `file_upload_list`
- `file_upload_retrieve`
- `file_upload_send`
- `page_create`
- `page_property_retrieve`
- `page_retrieve`
- `page_trash`
- `page_update`
- `raw_api_invoke`
- `raw_api_registered_operations`
- `search`
- `user_list`
- `user_me`
- `user_retrieve`
- `view_create`
- `view_list`
- `view_query`
- `view_retrieve`
- `view_update`

## Common rules

- MCP tools は Core だけを呼びます。CLI を呼んではいけません。
- Tool errors は structured `{"ok": false, "error": ...}` payload を返します。
- Tokens は default で redacted です。
- Delete、archive、trash 系 tools は `destructiveHint` を持ち、`confirm=true` を要求します。
- Real Notion permissions、paid plans、real workspace が必要な capability は tests と progress documentation に明記します。
