# CLI ドキュメント

このページは `nilo` CLI の入口です。page、block、database、設定、高度な fallback 入口を混ぜないよう、コマンドを topic ごとに分けています。

## 最初に読む文書

- [Installation](Installation.md): `nilo` コマンドのインストール。
- [Uninstallation](Uninstallation.md): コマンド、MCP client 設定、ローカル token、project context の削除。
- [Configuration](Configuration.md): Notion access、token、project-local context の設定。
- [MCP Clients](MCP_Clients.md): MCP 対応ツールをローカル N.I.L.O. server に接続する方法。
- [Troubleshooting](Troubleshooting.md): よくある問題の確認。

## CLI 分冊

- [Overview](Cli/Overview.md): 共通ルール、JSON payload、`--dry-run`、alias。
- [Project Config](Cli/Project_Config.md): `init`、`pwd`、`version`、`config --global/--local`。
- [Page](Cli/Page.md): default page の attach、page/block 読み取り、page 作成、page 更新。
- [Block](Cli/Block.md): block content の append、insert-after、update、trash。
- [Database DataSource](Cli/Database_DataSource.md): database container、data source 操作、database shortcut。
- [Auth And User](Cli/Auth_And_User.md): token validation、`whoami`、user lookup。
- [Comments](Cli/Comments.md): comment の list、create、reply。
- [Views](Cli/Views.md): view の retrieve、list、query、create、update。
- [File Uploads](Cli/File_Uploads.md): file upload lifecycle。
- [Search And Custom Emoji](Cli/Search_And_Custom_Emoji.md): workspace search と custom emoji。
- [Raw API](Cli/Raw_API.md): 高度な Raw API fallback。
- [MCP Server](Cli/MCP_Server.md): local MCP server の start、stop、status、cleanup。

## よく使う最初の手順

```bash
nilo config --global user.token ntn_xxx
nilo config --global --show
nilo init --project-name "Demo"
nilo page attach <page_id>
nilo page retrieve
nilo page blocks
```
