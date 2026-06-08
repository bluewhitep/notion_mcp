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
notion-mcp init \
  --token ntn_xxx \
  --user-name "Ada" \
  --user-id 01234567-89ab-cdef-0123-456789abcdef
```

确认状态：

```bash
notion-mcp status
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

## 安全说明

- token 保存在本地配置文件中，普通状态输出会脱敏。
- `page_trash`、`block_trash` 等危险工具需要 `confirm=true`。
- 真实 Notion 调用需要集成已被授权访问对应页面、数据库或 workspace 内容。
