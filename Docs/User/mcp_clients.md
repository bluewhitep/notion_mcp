# MCP Client 使用入口

本文面向使用者，说明如何让支持 MCP 的客户端调用本地 Notion MCP server。

## 启动命令

```bash
notion-mcp mcp serve --transport stdio
```

如果客户端使用命令数组形式，可配置为：

```json
{
  "command": "notion-mcp",
  "args": ["mcp", "serve", "--transport", "stdio"]
}
```

## 使用前配置

先初始化本地 Notion 配置：

```bash
notion-mcp config --global user.token ntn_xxx
notion-mcp config --global user.name "Ada"
```

确认状态：

```bash
notion-mcp config --global --show
```

## 当前工具域

MCP client 可枚举以下工具域：

- config
- auth
- pages
- blocks
- databases
- data_sources
- users
- comments
- views
- file_uploads
- search
- custom_emojis
- raw_api

## 当前 MCP Tool 清单

配置和认证：

- `config_status`
- `config_get`
- `auth_validate`
- `auth_whoami`

页面：

- `page_retrieve`
- `page_property_retrieve`
- `page_create`
- `page_update`
- `page_trash`

区块：

- `block_children_list`
- `block_append`
- `block_update`
- `block_trash`

数据库：

- `database_retrieve`
- `database_query`
- `database_create`
- `database_update`

数据源：

- `data_source_retrieve`
- `data_source_query`
- `data_source_create`
- `data_source_update`

用户：

- `user_me`
- `user_list`
- `user_retrieve`

评论：

- `comment_list`
- `comment_create`
- `comment_reply`

视图：

- `view_retrieve`
- `view_list`
- `view_query`
- `view_create`
- `view_update`

文件上传：

- `file_upload_retrieve`
- `file_upload_list`
- `file_upload_create`
- `file_upload_send`
- `file_upload_complete`

搜索和自定义表情：

- `search`
- `custom_emoji_list`
- `custom_emoji_retrieve`

受控 Raw API：

- `raw_api_registered_operations`
- `raw_api_invoke`

## 安全说明

- token 保存在本地配置文件中，普通状态输出会脱敏。
- `page_trash`、`block_trash` 等危险工具需要 `confirm=true`。
- 真实 Notion 调用需要集成已被授权访问对应页面、数据库或 workspace 内容。
