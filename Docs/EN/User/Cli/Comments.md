# Comments CLI

Comment commands list, create, and reply to Notion comments.

## Commands

| Command | Purpose |
| --- | --- |
| `nilo comment list <block_id_or_page_id>` | List comments on a page or block. |
| `nilo comment create <page_id>` | Create a comment on a page. |
| `nilo comment reply <comment_id>` | Reply to an existing comment. |

## Examples

```bash
nilo comment list <page_id> --json
nilo comment create <page_id> --payload '{"rich_text": []}'
nilo comment reply <comment_id> --payload '{"rich_text": []}'
```
