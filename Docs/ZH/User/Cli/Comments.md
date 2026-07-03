# Comments CLI

本文说明 comment 相关命令。

## 命令

| 命令 | 作用 |
| --- | --- |
| `nilo comment list <block_id_or_page_id>` | 列出指定 page/block 的 comments。 |
| `nilo comment create <page_id>` | 在 page 上创建 comment。 |
| `nilo comment reply <comment_id>` | 回复已有 comment。 |

## 示例

```bash
nilo comment list <page_id> --json
nilo comment create <page_id> --payload '{"rich_text": []}'
nilo comment reply <comment_id> --payload '{"rich_text": []}'
```
