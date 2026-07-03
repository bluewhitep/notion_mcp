# Raw API CLI

Raw API は高度な fallback 入口です。通常の page、database、block 編集経路として使うものではありません。

## コマンド

| Command | Purpose |
| --- | --- |
| `nilo raw-api operations` | 登録済み raw API operation 名を一覧します。 |
| `nilo raw-api invoke <operation>` | 登録済み raw API operation を呼び出します。 |

## 例

```bash
nilo raw-api operations
nilo raw-api invoke search --arguments '{"query": "Tasks"}' --json
```
