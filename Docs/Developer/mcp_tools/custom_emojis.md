# Custom Emoji Tools

- `custom_emoji_list`
  - 说明：列出 integration 可访问的 custom emojis。
  - 可选参数：`page_size`、`start_cursor`。
- `custom_emoji_retrieve`
  - 说明：读取指定 custom emoji。
  - 必选参数：`custom_emoji_id`。
  - live 限制：取决于 workspace 是否有 custom emojis 和 API 权限。
