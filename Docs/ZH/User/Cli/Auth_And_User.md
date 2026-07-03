# Auth And User CLI

本文说明 auth 和 user 查询命令。

## 命令

| 命令 | 作用 |
| --- | --- |
| `nilo auth validate` | 验证当前 token 是否可用。 |
| `nilo auth whoami` | 查询当前 token 对应的 Notion 身份；普通用户用它查看 user id，不需要手动配置 user id。 |
| `nilo user me` | 读取当前用户或 bot 信息。 |
| `nilo user list` | 列出 workspace users。 |
| `nilo user retrieve <user_id>` | 读取指定 user。 |

## 示例

```bash
nilo auth validate
nilo auth whoami --json
nilo user me --json
nilo user list --json
nilo user retrieve <user_id> --json
```
