# User Tools

- `user_list`
  - Description: lists Notion users accessible to the integration.
  - Optional parameters: `page_size`, `start_cursor`.
- `user_retrieve`
  - Description: reads one user.
  - Required parameters: `user_id`.
- `user_me`
  - Description: reads the bot/user behind the current token.
  - Required parameters: none.
  - Live requirement: a real Notion token.
