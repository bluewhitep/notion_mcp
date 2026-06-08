# MCP Tools 开发者文档

本文档是 MCP tool 文档入口。当前仓库已实现 `src/notion_mcp/mcp_server/`，使用 MCP Python SDK 的 `FastMCP` 暴露本地工具。

## Server

- server factory：`src/notion_mcp/mcp_server/server.py`
- package entry：`notion_mcp.mcp_server:create_mcp_server`
- CLI entry：`notion-mcp mcp serve --transport stdio`
- 支持 transport：`stdio`、`streamable-http`

## 工具域文档

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

## 公共规则

- MCP Tool 只能调用 Core，不能调用 CLI。
- 工具错误应返回结构化 `{"ok": false, "error": ...}`。
- token 默认必须脱敏。
- 删除、归档、trash 类危险工具必须带 `destructiveHint`，并要求 `confirm=true`。
- live Notion 权限、付费计划或真实 workspace 才能验证的能力，必须在测试和进度文档中标记。
