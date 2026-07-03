# Auth Tools

- `auth_validate`
  - 说明：通过 Core auth service 调用 `users.me()` 校验当前 token。
  - 必选参数：无。
  - 返回：`valid`、`user_id`、`name`、`raw`。
  - live 限制：需要真实 Notion token。
- `auth_whoami`
  - 说明：返回当前 token 对应的 Notion 用户信息。
  - 必选参数：无。
  - live 限制：需要真实 Notion token。
