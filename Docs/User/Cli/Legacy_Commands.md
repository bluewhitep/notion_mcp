# Legacy Commands

以下命令保留给旧脚本和迁移使用，不建议作为新用法。

## 命令

| 命令 | 作用 |
| --- | --- |
| `notion-mcp set-token` | 设置旧配置中的 Notion token。新用法是 `notion-mcp config --global user.token <token>`。 |
| `notion-mcp set-user` | 设置旧配置中的 user id。普通用户不需要手动设置 user id。 |
| `notion-mcp show` | 显示旧配置文件内容；注意旧配置可能明文显示 token。 |
| `notion-mcp run` | 启动 legacy FastAPI REST 兼容入口；MCP client 应使用 `notion-mcp mcp serve`。 |
