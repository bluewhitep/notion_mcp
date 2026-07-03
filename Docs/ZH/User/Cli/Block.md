# Block CLI

本文说明 block 内容块命令。

Block 命令是内容块的底层入口。需要精确插入时，优先使用 `insert-after`；`insert-before` 暂不作为稳定公开命令。

## 命令

| 命令 | 作用 |
| --- | --- |
| `nilo block children <block_id>` | 列出指定 block 的 child blocks。 |
| `nilo block append <block_id>` | 在指定 block/page 下追加 child blocks。 |
| `nilo block insert-after <block_id>` | 在目标 block 后插入新的 sibling blocks。 |
| `nilo block update <block_id>` | 更新指定 block。 |
| `nilo block trash <block_id>` | 将指定 block 移入 trash。 |

## 示例

```bash
nilo block append <block_id> --payload '{"children": []}' --dry-run --json
nilo block insert-after <block_id> --payload '{"children": []}'
nilo block update <block_id> --payload '{"paragraph": {}}'
nilo block trash <block_id>
```
