# Block CLI

Block commands operate on Notion content blocks. Use `insert-after` for precise sibling insertion. `insert-before` is not a stable public command.

## Commands

| Command | Purpose |
| --- | --- |
| `nilo block children <block_id>` | List child blocks for a block or page. |
| `nilo block append <block_id>` | Append child blocks under a block or page. |
| `nilo block insert-after <block_id>` | Insert sibling blocks after the target block. |
| `nilo block update <block_id>` | Update a block. |
| `nilo block trash <block_id>` | Move a block to trash. |

## Examples

```bash
nilo block append <block_id> --payload '{"children": []}' --dry-run --json
nilo block insert-after <block_id> --payload '{"children": []}'
nilo block update <block_id> --payload '{"paragraph": {}}'
nilo block trash <block_id>
```
