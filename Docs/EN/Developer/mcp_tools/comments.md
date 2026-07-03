# Comment Tools

- `comment_list`
  - Description: lists comments using raw Notion comment query parameters.
  - Required parameters: `params`.
- `comment_create`
  - Description: creates a comment.
  - Required parameters: `payload`.
  - Optional parameters: `dry_run`.
- `comment_reply`
  - Description: replies to a discussion.
  - Required parameters: `discussion_id`, `rich_text`.
  - Optional parameters: `dry_run`.
