# User Tools

- `user_list`
  - 说明：列出 integration 可访问的 Notion users。
  - 可选参数：`page_size`、`start_cursor`。
- `user_retrieve`
  - 说明：读取指定 user。
  - 必选参数：`user_id`。
- `user_me`
  - 说明：读取当前 token 对应的 bot/user。
  - 必选参数：无。
  - live 限制：需要真实 Notion token。
