# Views CLI

View commands は Notion views を読み取り、管理します。

## コマンド

| Command | Purpose |
| --- | --- |
| `nilo view retrieve <view_id>` | view information を読み取ります。 |
| `nilo view list <database_id>` | database 配下の views を一覧します。 |
| `nilo view query <view_id>` | view を query します。 |
| `nilo view create` | view を作成します。 |
| `nilo view update <view_id>` | view を更新します。 |

## 例

```bash
nilo view retrieve <view_id> --json
nilo view list <database_id> --json
nilo view query <view_id> --payload '{"page_size": 10}'
nilo view create --payload '{}'
nilo view update <view_id> --payload '{}'
```
