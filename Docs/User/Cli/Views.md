# Views CLI

本文说明 view 相关命令。

## 命令

| 命令 | 作用 |
| --- | --- |
| `nilo view retrieve <view_id>` | 读取 view 信息。 |
| `nilo view list <database_id>` | 列出 database 下的 views。 |
| `nilo view query <view_id>` | 查询 view。 |
| `nilo view create` | 创建 view。 |
| `nilo view update <view_id>` | 更新 view。 |

## 示例

```bash
nilo view retrieve <view_id> --json
nilo view list <database_id> --json
nilo view query <view_id> --payload '{"page_size": 10}'
nilo view create --payload '{}'
nilo view update <view_id> --payload '{}'
```
