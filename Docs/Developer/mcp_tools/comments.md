# Comment Tools

- `comment_list`
  - 说明：按 raw Notion comment query 参数列出 comments。
  - 必选参数：`params`。
- `comment_create`
  - 说明：创建 comment。
  - 必选参数：`payload`。
  - 可选参数：`dry_run`。
- `comment_reply`
  - 说明：回复 discussion。
  - 必选参数：`discussion_id`、`rich_text`。
  - 可选参数：`dry_run`。
