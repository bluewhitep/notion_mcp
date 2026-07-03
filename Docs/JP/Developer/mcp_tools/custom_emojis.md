# Custom Emoji Tools

- `custom_emoji_list`
  - 説明: integration が access できる custom emoji を一覧します。
  - Optional parameters: `page_size`, `start_cursor`.
- `custom_emoji_retrieve`
  - 説明: custom emoji を 1 つ読み取ります。
  - Required parameters: `custom_emoji_id`.
  - Live requirement: workspace の custom emoji availability と API permissions に依存します。
