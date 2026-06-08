# Troubleshooting

本文面向使用者，记录常见问题。

## 未配置 token

运行：

```bash
notion-mcp init --token ntn_xxx --user-name "Ada" --user-id 01234567-89ab-cdef-0123-456789abcdef
```

然后检查：

```bash
notion-mcp status
```

## token 无权限

确认 Notion integration 已被授权访问目标页面、数据库或 workspace 内容。

## 用户 UUID 不匹配

如果 `auth validate` 报告用户不匹配，请确认 `--user-id` 是当前 token 对应的 Notion 用户 UUID。

## MCP client 无法启动

先在终端确认：

```bash
notion-mcp mcp serve --help
```

client 配置应使用：

```json
{
  "command": "notion-mcp",
  "args": ["mcp", "serve", "--transport", "stdio"]
}
```

## Notion API version 问题

当前默认使用 `2026-03-11`。如果调用参数与 Notion 返回错误不匹配，请检查 Notion API 文档对应版本的字段名。

## Rate limit

如果遇到 rate limit，请降低调用频率，或让 Agent 分批执行操作。
