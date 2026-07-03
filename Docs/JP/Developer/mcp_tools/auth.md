# Auth Tools

- `auth_validate`
  - 説明: Core auth service と `users.me()` で現在の token を検証します。
  - Required parameters: none.
  - Returns: `valid`, `user_id`, `name`, `raw`.
  - Live requirement: real Notion token.
- `auth_whoami`
  - 説明: 現在の token に対応する Notion user または bot identity を返します。
  - Required parameters: none.
  - Live requirement: real Notion token.
