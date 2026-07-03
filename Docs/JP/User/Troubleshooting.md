# トラブルシューティング

この文書では、よくあるローカル設定と MCP クライアントの問題をまとめます。

## Token が未設定

グローバル token と任意の表示名を設定します。

```bash
nilo config --global user.token ntn_xxx
nilo config --global user.name "Ada"
```

保存状態を確認します。

```bash
nilo config --global --show
```

状態出力は token をマスクし、生の secret は表示しません。

## Token にアクセス権がない

Notion internal connection が対象 page、database、または workspace content にアクセスできることを確認してください。

page や database が見つからない場合は、まず Notion 側の共有設定と connection access を確認します。対象が connection に共有されていない場合、API は権限エラーのような失敗を返すことがあります。

## Identity が想定と違う

通常は `user_id` を設定する必要はありません。高度な設定で `user_id` を設定していて、`nilo auth validate` が不一致を報告する場合は、token identity を確認します。

```bash
nilo auth whoami --json
```

Notion internal connection は通常 bot user として識別されます。

## MCP クライアントが起動しない

ローカルコマンドが使えるか確認します。

```bash
nilo --help
nilo server stdio --help
nilo server run --help
```

stdio クライアントでは、command と args を別フィールドにします。

```json
{
  "command": "nilo",
  "args": ["server", "stdio"]
}
```

MCP クライアントが明示的に要求しない限り、コマンド全体を 1 つの `command` フィールドに入れないでください。

streamable HTTP クライアントでは background server を確認します。

```bash
nilo server status
nilo server logs --tail 100
```

## Notion API version の不一致

デフォルトの Notion API version は `2026-03-11` です。Notion が payload を拒否する場合は、その version の Notion API ドキュメントと field 名、object 形状を比較してください。

## Rate limit

Notion が rate limit エラーを返す場合は、並列数と batch size を下げてください。Agent workflow では大きな編集を小さな単位に分割します。
