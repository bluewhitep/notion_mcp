# Testing Strategy

この文書は test layers と実行方針を説明します。

## Layers

- Compatibility tests
  - 公開 CLI と MCP tool behavior を regression-test 可能に保ちます。
  - 新実装を通すために既存 compatibility tests を弱めません。
- Core tests
  - configuration、errors、client factory、auth、services、Raw API、audit を対象にします。
- CLI tests
  - init、config、status、resource commands、dry-run behavior を対象にします。
- MCP tests
  - server lifecycle、tool inventory、tool calls、dangerous tools を対象にします。
- Scenario tests
  - local configuration flows、CLI -> Core -> fake Notion、MCP -> Core -> fake Notion、isolated install を対象にします。
- Live tests
  - default では skip します。
  - environment variables で明示的に有効化した場合だけ real Notion にアクセスします。

## Rules

- 新しい behavior は実装前に tests を書きます。
- 既存 tests を新実装に合わせて弱めません。
- coverage が不足する場合は、より狭く明確な tests を追加します。
- live test の成功を偽装してはいけません。

## Common commands

```bash
uv run pytest -q -p no:cacheprovider
uv run pytest -q tests/live
```

Isolated install checks:

```bash
uv run --no-project --with . nilo --help
uv run --no-project --with . nilo server run --help
```
