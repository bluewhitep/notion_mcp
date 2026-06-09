# Auth And User CLI

本文说明 auth 和 user 查询命令。

## 命令

| 命令 | 作用 |
| --- | --- |
| `notion-mcp auth validate` | 验证当前 token 是否可用。 |
| `notion-mcp auth whoami` | 查询当前 token 对应的 Notion 身份；普通用户用它查看 user id，不需要手动配置 user id。 |
| `notion-mcp user me` | 读取当前用户或 bot 信息。 |
| `notion-mcp user list` | 列出 workspace users。 |
| `notion-mcp user retrieve <user_id>` | 读取指定 user。 |

## 示例

```bash
notion-mcp auth validate
notion-mcp auth whoami --json
notion-mcp user me --json
notion-mcp user list --json
notion-mcp user retrieve <user_id> --json
```
