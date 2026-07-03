# Block Tools

- `block_children_list`
  - Description: lists child blocks.
  - Required parameters: `block_id`.
- `block_append`
  - Description: appends child blocks using the Notion 2026 `position` contract.
  - Required parameters: `block_id`, `children`.
  - Optional parameters: `position`, `dry_run`.
- `block_update`
  - Description: updates a block.
  - Required parameters: `block_id`, `payload`.
  - Optional parameters: `dry_run`.
- `block_trash`
  - Description: deletes or trashes a block.
  - Required parameters: `block_id`, `confirm`.
  - Optional parameters: `dry_run`.
  - Risk: `destructiveHint=true`; missing `confirm=true` returns `confirmation_required`.
