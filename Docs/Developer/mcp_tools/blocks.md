# Block Tools

- `block_children_list`
  - 说明：列出区块子元素。
  - 必选参数：`block_id`。
- `block_append`
  - 说明：追加子区块，使用 Notion 2026 `position` 合约。
  - 必选参数：`block_id`、`children`。
  - 可选参数：`position`、`dry_run`。
- `block_update`
  - 说明：更新区块。
  - 必选参数：`block_id`、`payload`。
  - 可选参数：`dry_run`。
- `block_trash`
  - 说明：删除或 trash 区块。
  - 必选参数：`block_id`、`confirm`。
  - 可选参数：`dry_run`。
  - 危险性：`destructiveHint=true`，缺少 `confirm=true` 会返回 `confirmation_required`。
