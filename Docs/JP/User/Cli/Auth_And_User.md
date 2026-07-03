# Auth And User CLI

このページでは、認証確認と Notion user lookup コマンドを説明します。

## コマンド

| Command | Purpose |
| --- | --- |
| `nilo auth validate` | 現在の token が使えるか確認します。 |
| `nilo auth whoami` | 現在の token に対応する Notion identity を表示します。 |
| `nilo user me` | 現在の user または bot を読み取ります。 |
| `nilo user list` | workspace users を一覧します。 |
| `nilo user retrieve <user_id>` | 指定 user を読み取ります。 |

## 例

```bash
nilo auth validate
nilo auth whoami --json
nilo user me --json
nilo user list --json
nilo user retrieve <user_id> --json
```
