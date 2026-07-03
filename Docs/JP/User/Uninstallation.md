# アンインストール

この文書では、ローカルの `nilo` コマンドを削除し、必要に応じてローカル設定と MCP runtime state を削除する方法を説明します。

N.I.L.O. をアンインストールしても、Notion の page、database、block、comment は削除されません。また、Notion Developer portal の internal connection token も自動では失効しません。

## 簡単なアンインストール

最初に使ったインストール方法に対応するコマンドを実行します。

### uv による永続インストール

```bash
uv tool uninstall notion-nilo
```

### uv による一時実行

一時的な `uv run --with ...` は永続的な `nilo` 実行ファイルをインストールしないため、アンインストールは不要です。

### pip インストール

```bash
pip uninstall notion-nilo
```

## 完全なクリーンアップ

MCP クライアント設定、background server state、ローカル token 設定、またはプロジェクトローカル context も削除したい場合に使います。

### Background server state を停止して削除する

streamable HTTP server が起動中か確認します。

```bash
nilo server status
```

停止します。

```bash
nilo server stop
```

ローカル server runtime state とログを削除します。

```bash
nilo server remove
```

実行中プロセスも停止する必要がある場合は次を使います。

```bash
nilo server remove --force
```

デフォルトの runtime directory はグローバル設定パスから決まります。デフォルト設定パスは `~/.notion_mcp/config.json` なので、server state とログも通常 `~/.notion_mcp/` 以下にあります。`NOTION_MCP_RUNTIME_DIR` が設定されている場合は、その値が runtime directory になります。

### MCP クライアント設定を削除する

stdio MCP クライアントでは、`nilo` server entry を削除します。

```json
{
  "mcpServers": {
    "nilo": {
      "command": "nilo",
      "args": ["server", "stdio"]
    }
  }
}
```

streamable HTTP MCP クライアントでは、次のローカル URL を削除します。

```text
http://127.0.0.1:8000/mcp
```

クライアント設定に `NOTION_MCP_CONFIG` がある場合は、その environment entry も削除してください。

### コマンドを削除する

`uv tool install .` の場合:

```bash
uv tool uninstall notion-nilo
```

`pip install /path/to/notion-nilo` の場合:

```bash
pip uninstall notion-nilo
```

アンインストール後、別の環境にまだコマンドが残っていないか確認します。

```bash
nilo --help
```

まだコマンドが存在する場合は、shell の `PATH`、alias、ほかの Python 環境を確認してください。

### 任意: グローバル設定を削除する

グローバル設定には Notion token、表示名、Notion API version、timeout、retry 設定が保存されます。デフォルトパスは次です。

```text
~/.notion_mcp/config.json
```

このローカル token 設定が不要になった場合のみ削除します。

```bash
rm -f ~/.notion_mcp/config.json
```

カスタム設定パスを使った場合は、そのファイルを削除します。

```bash
rm -f /path/to/config.json
```

### 任意: プロジェクトローカル context を削除する

プロジェクトローカル `.notion_mcp/` directory は、default page/database binding、project settings、state、cache、logs などを保存します。グローバル Notion token は保存しません。

そのプロジェクトでローカル Notion context が不要になった場合だけ、プロジェクトルートで削除します。

```bash
rm -rf .notion_mcp
```

これはローカル project context だけを削除します。リモート Notion content は変更しません。

### 任意: Notion access を取り消す

token を無効化したい場合や connection に content access を残したくない場合は、Notion 側で internal connection token を失効させるか、関連 page/database から connection を削除します。

ローカルのアンインストールコマンドでは Notion 側の取り消しは実行できません。

## クリーンアップ確認

永続コマンドをアンインストールした後、次のコマンドは失敗するか、別のインストール元を示します。

```bash
nilo --help
```

グローバル設定も削除した場合、後で再インストールして使うには token を再設定する必要があります。詳しくは [Configuration](Configuration.md) を参照してください。
