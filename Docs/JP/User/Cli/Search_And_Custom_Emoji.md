# Search And Custom Emoji CLI

このページでは workspace search と custom emoji commands を説明します。

## コマンド

| Command | Purpose |
| --- | --- |
| `nilo search query` | workspace content を検索します。 |
| `nilo custom-emoji list` | custom emoji を pagination 付きで一覧します。 |
| `nilo custom-emoji retrieve <custom_emoji_id>` | 指定 custom emoji を読み取ります。 |

## 例

```bash
nilo search query --payload '{"query": "Tasks"}' --json
nilo custom-emoji list --page-size 20 --json
nilo custom-emoji retrieve <custom_emoji_id> --json
```
