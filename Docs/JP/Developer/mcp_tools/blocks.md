# Block Tools

- `block_children_list`
  - 説明: child blocks を一覧します。
  - Required parameters: `block_id`.
- `block_append`
  - 説明: Notion 2026 `position` contract に従って child blocks を追加します。
  - Required parameters: `block_id`, `children`.
  - Optional parameters: `position`, `dry_run`.
- `block_update`
  - 説明: block を更新します。
  - Required parameters: `block_id`, `payload`.
  - Optional parameters: `dry_run`.
- `block_trash`
  - 説明: block を delete/trash します。
  - Required parameters: `block_id`, `confirm`.
  - Optional parameters: `dry_run`.
  - Risk: `destructiveHint=true`; `confirm=true` がない場合は `confirmation_required` を返します。
