# Auth Tools

- `auth_validate`
  - Description: validates the current token through the Core auth service and `users.me()`.
  - Required parameters: none.
  - Returns: `valid`, `user_id`, `name`, and `raw`.
  - Live requirement: a real Notion token.
- `auth_whoami`
  - Description: returns the Notion user or bot identity for the current token.
  - Required parameters: none.
  - Live requirement: a real Notion token.
