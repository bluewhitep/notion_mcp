# Comments CLI

Comment commands は Notion comments の list、create、reply を扱います。

## コマンド

| Command | Purpose |
| --- | --- |
| `nilo comment list <block_id_or_page_id>` | page または block の comments を一覧します。 |
| `nilo comment create <page_id>` | page に comment を作成します。 |
| `nilo comment reply <comment_id>` | 既存 comment に reply します。 |

## 例

```bash
nilo comment list <page_id> --json
nilo comment create <page_id> --payload '{"rich_text": []}'
nilo comment reply <comment_id> --payload '{"rich_text": []}'
```
