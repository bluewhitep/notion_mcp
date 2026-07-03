# Block CLI

Block commands は Notion content block を操作します。正確な sibling insertion には `insert-after` を使います。`insert-before` は安定した公開コマンドではありません。

## コマンド

| Command | Purpose |
| --- | --- |
| `nilo block children <block_id>` | block または page の child blocks を一覧します。 |
| `nilo block append <block_id>` | block または page の下に child blocks を追加します。 |
| `nilo block insert-after <block_id>` | 対象 block の後ろに sibling blocks を挿入します。 |
| `nilo block update <block_id>` | block を更新します。 |
| `nilo block trash <block_id>` | block を trash に移動します。 |

## 例

```bash
nilo block append <block_id> --payload '{"children": []}' --dry-run --json
nilo block insert-after <block_id> --payload '{"children": []}'
nilo block update <block_id> --payload '{"paragraph": {}}'
nilo block trash <block_id>
```
