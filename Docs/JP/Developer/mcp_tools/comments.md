# Comment Tools

- `comment_list`
  - 説明: raw Notion comment query parameters で comments を一覧します。
  - Required parameters: `params`.
- `comment_create`
  - 説明: comment を作成します。
  - Required parameters: `payload`.
  - Optional parameters: `dry_run`.
- `comment_reply`
  - 説明: discussion に reply します。
  - Required parameters: `discussion_id`, `rich_text`.
  - Optional parameters: `dry_run`.
