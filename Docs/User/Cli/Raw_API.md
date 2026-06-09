# Raw API CLI

Raw API 只作为高级兜底入口，不作为普通 page/database 编辑路径。

## 命令

| 命令 | 作用 |
| --- | --- |
| `notion-mcp raw-api operations` | 列出当前可用的 raw API operation 名称。 |
| `notion-mcp raw-api invoke <operation>` | 调用指定 raw API operation。 |

## 示例

```bash
notion-mcp raw-api operations
notion-mcp raw-api invoke search --arguments '{"query": "Tasks"}' --json
```
