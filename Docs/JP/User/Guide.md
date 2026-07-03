# 利用ガイド

このガイドは、N.I.L.O. をローカルで実行し、ターミナル、MCP クライアント、または自動化エージェントから使う人向けです。N.I.L.O. は、利用者自身の Notion internal connection token を使って公式 Notion API に接続します。

## 現在の状態

N.I.L.O. には主に 2 つの入口があります。

- `nilo` という git 風の CLI。
- `nilo server ...` で管理するローカル MCP server。

コマンドの詳細は [CLI リファレンス](Cli.md) を参照してください。MCP クライアントの設定は [MCP Clients](MCP_Clients.md) を参照してください。

## 前提条件

1. Notion internal connection を作成し、installation access token をコピーします。
2. 操作したい page または database をその connection に共有します。
3. Python 3.10 以降を用意します。
4. 推奨インストール手順を使う場合は `uv` を用意します。

## インストール

推奨手順は、リポジトリルートから `uv` でインストールする方法です。

```bash
cd /path/to/notion-nilo
uv tool install .
nilo --help
```

`uv` がない場合は、ローカルパスから `pip` でインストールできます。

```bash
pip install /path/to/notion-nilo
nilo --help
```

詳しいインストール、更新、アンインストール手順は [Installation](Installation.md) と [Uninstallation](Uninstallation.md) を参照してください。

## 初期設定

Notion API を呼び出す前に、グローバル token を設定します。通常の利用では `user_id` を手動設定する必要はありません。

```bash
# グローバル token と任意の表示名を設定します。
nilo config --global user.token ntn_xxx
nilo config --global user.name Ada

# 保存済み設定と token 状態を確認します。
nilo config --global --show --json

# 現在の token に対応する Notion identity を確認します。
nilo auth whoami --json
```

デフォルトのグローバル設定ファイルは `~/.notion_mcp/config.json` です。別のパスを使う場合は `NOTION_MCP_CONFIG` を設定します。

## MCP Server を起動する

stdio 型の MCP クライアントでは、クライアント側から次のコマンドを起動します。

```bash
nilo server stdio
```

streamable HTTP URL に接続するクライアントでは、先にローカル server を起動します。

```bash
nilo server run --host 127.0.0.1 --port 8000
nilo server status
```

クライアントには次の URL を設定します。

```text
http://127.0.0.1:8000/mcp
```

詳しい設定例は [MCP Clients](MCP_Clients.md) を参照してください。

## CLI 例

```bash
nilo page retrieve <page_id> --json
nilo data-source query <data_source_id> --json
nilo block children <block_id> --json
```

ID は通常 Notion の page/database URL からコピーできます。CLI は多くの Notion URL を直接受け取り、内部で ID を正規化します。

## FAQ

### Notion token が未設定と表示される

グローバル token がまだ保存されていません。次を実行してください。

```bash
nilo config --global user.token ntn_xxx
```

### Notion user UUID を入力する必要がありますか

通常は不要です。現在の token の identity を確認したい場合だけ、`nilo auth whoami --json` を実行します。

### OAuth は対応していますか

現在のユーザーフローでは対応していません。現行リリースは Notion internal connection token を使います。

### 呼び出しが失敗した場合は何を確認しますか

多くの失敗は設定、権限、またはリクエスト payload が原因です。

1. token が設定済みで有効か確認します。
2. Notion connection が対象 page/database にアクセスできるか確認します。
3. payload が利用中の Notion API version に合っているか確認します。
4. CLI 出力、MCP クライアントログ、またはローカル server ログを確認します。
