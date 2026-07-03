# インストール

この文書では、ローカルの `nilo` コマンドをインストール、更新、アンインストールする方法を説明します。

## 事前準備

推奨手順は `uv tool install` です。これにより `nilo` コマンドが永続的な tool 環境に入り、shell の `PATH` から実行できるようになります。

`uv` がない場合は、ローカルリポジトリパスから `pip` でインストールします。

インストール後、API 呼び出しの前に Notion internal connection token を設定してください。詳細は [Configuration](Configuration.md) を参照してください。

最初によく使うコマンドは次の通りです。

```bash
nilo config --global user.token ntn_xxx
nilo config --global user.name "Ada"
nilo config --global --show
```

## インストール

### uv による永続インストール

通常はこちらを使います。

```bash
cd /path/to/notion-nilo
uv tool install .
nilo --help
```

shell が `nilo` を見つけられない場合は、uv の shell 統合を更新してターミナルを再起動します。

```bash
uv tool update-shell
nilo --help
```

### uv による一時実行

永続的なコマンドをインストールしたくない場合に使います。

```bash
cd /path/to/notion-nilo
uv run --no-project --with . nilo --help
```

### pip インストール

`uv` が使えない場合はこちらを使います。

```bash
pip install /path/to/notion-nilo
nilo --help
```

## 更新

リポジトリが更新された場合は、先にローカル checkout を更新し、その後コマンドを再インストールします。`git pull` がローカル変更を報告した場合は、その変更を処理してから続行してください。

### uv による永続インストール

```bash
cd /path/to/notion-nilo
git pull
uv tool install --force --reinstall .
nilo --help
```

### uv による一時実行

一時実行は現在のローカルパスをそのまま使います。

```bash
cd /path/to/notion-nilo
git pull
uv run --no-project --with . nilo --help
```

### pip インストール

```bash
cd /path/to/notion-nilo
git pull
pip install --force-reinstall /path/to/notion-nilo
nilo --help
```

## アンインストール

### uv による永続インストール

```bash
uv tool uninstall notion-nilo
```

### uv による一時実行

永続的な `nilo` コマンドをインストールしていないため、アンインストールは不要です。

### pip インストール

```bash
pip uninstall notion-nilo
```

### 完全なクリーンアップ

MCP クライアント、background server runtime、グローバル token、またはプロジェクトローカル `.notion_mcp/` context も設定済みの場合は、[Uninstallation](Uninstallation.md) の完全なクリーンアップ手順に従ってください。
