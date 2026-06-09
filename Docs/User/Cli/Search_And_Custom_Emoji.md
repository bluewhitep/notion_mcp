# Search And Custom Emoji CLI

本文说明搜索和 custom emoji 命令。

## 命令

| 命令 | 作用 |
| --- | --- |
| `notion-mcp search query` | 搜索 workspace 内容。 |
| `notion-mcp custom-emoji list` | 列出 custom emojis，可用分页参数限制结果。 |
| `notion-mcp custom-emoji retrieve <custom_emoji_id>` | 读取指定 custom emoji。 |

## 示例

```bash
notion-mcp search query --payload '{"query": "Tasks"}' --json
notion-mcp custom-emoji list --page-size 20 --json
notion-mcp custom-emoji retrieve <custom_emoji_id> --json
```
