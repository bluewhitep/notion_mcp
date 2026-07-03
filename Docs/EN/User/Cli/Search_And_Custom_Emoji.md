# Search And Custom Emoji CLI

This page covers workspace search and custom emoji commands.

## Commands

| Command | Purpose |
| --- | --- |
| `nilo search query` | Search workspace content. |
| `nilo custom-emoji list` | List custom emoji with optional pagination. |
| `nilo custom-emoji retrieve <custom_emoji_id>` | Read one custom emoji. |

## Examples

```bash
nilo search query --payload '{"query": "Tasks"}' --json
nilo custom-emoji list --page-size 20 --json
nilo custom-emoji retrieve <custom_emoji_id> --json
```
