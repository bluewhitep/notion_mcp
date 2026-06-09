# Views CLI

本文说明 view 相关命令。

## 命令

| 命令 | 作用 |
| --- | --- |
| `notion-mcp view retrieve <view_id>` | 读取 view 信息。 |
| `notion-mcp view list <database_id>` | 列出 database 下的 views。 |
| `notion-mcp view query <view_id>` | 查询 view。 |
| `notion-mcp view create` | 创建 view。 |
| `notion-mcp view update <view_id>` | 更新 view。 |

## 示例

```bash
notion-mcp view retrieve <view_id> --json
notion-mcp view list <database_id> --json
notion-mcp view query <view_id> --payload '{"page_size": 10}'
notion-mcp view create --payload '{}'
notion-mcp view update <view_id> --payload '{}'
```
