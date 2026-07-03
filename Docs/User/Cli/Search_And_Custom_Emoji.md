# Search And Custom Emoji CLI

本文说明搜索和 custom emoji 命令。

## 命令

| 命令 | 作用 |
| --- | --- |
| `nilo search query` | 搜索 workspace 内容。 |
| `nilo custom-emoji list` | 列出 custom emojis，可用分页参数限制结果。 |
| `nilo custom-emoji retrieve <custom_emoji_id>` | 读取指定 custom emoji。 |

## 示例

```bash
nilo search query --payload '{"query": "Tasks"}' --json
nilo custom-emoji list --page-size 20 --json
nilo custom-emoji retrieve <custom_emoji_id> --json
```
