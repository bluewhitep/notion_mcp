# User Tools

- `user_list`
  - 説明: integration が access できる Notion users を一覧します。
  - Optional parameters: `page_size`, `start_cursor`.
- `user_retrieve`
  - 説明: user を 1 つ読み取ります。
  - Required parameters: `user_id`.
- `user_me`
  - 説明: current token の bot/user を読み取ります。
  - Required parameters: none.
  - Live requirement: real Notion token.
