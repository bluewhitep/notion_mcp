# Comments CLI

本文说明 comment 相关命令。

## 命令

| 命令 | 作用 |
| --- | --- |
| `notion-mcp comment list <block_id_or_page_id>` | 列出指定 page/block 的 comments。 |
| `notion-mcp comment create <page_id>` | 在 page 上创建 comment。 |
| `notion-mcp comment reply <comment_id>` | 回复已有 comment。 |

## 示例

```bash
notion-mcp comment list <page_id> --json
notion-mcp comment create <page_id> --payload '{"rich_text": []}'
notion-mcp comment reply <comment_id> --payload '{"rich_text": []}'
```
