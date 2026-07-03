# MCP Tools Developer Documentation

This is the entrypoint for MCP tool documentation. The repository implements `src/nilo/mcp_server/` and exposes local tools through the MCP Python SDK `FastMCP`.

## Server

- Server factory: `src/nilo/mcp_server/server.py`
- Package entry: `nilo.mcp_server:create_mcp_server`
- CLI stdio entry: `nilo server stdio`
- CLI background HTTP entry: `nilo server run --host 127.0.0.1 --port 8000`
- Supported transports: `stdio`, `streamable-http`

## Tool Domain Documents

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

## Tool Inventory

The current server exposes 46 tools:

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

## Common Rules

- MCP tools may call Core only; they must not call CLI.
- Tool errors should return structured `{"ok": false, "error": ...}` payloads.
- Tokens must be redacted by default.
- Delete, archive, and trash tools must carry `destructiveHint` and require `confirm=true`.
- Capabilities that require real Notion permissions, paid plans, or a real workspace must be marked in tests and progress documentation.
