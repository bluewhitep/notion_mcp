# Project Config CLI

このページでは project context と configuration commands を説明します。

## コマンド

| Command | Purpose |
| --- | --- |
| `nilo init` | 現在の directory に project-local `.notion_mcp/` context を作成します。 |
| `nilo pwd` | 現在の directory から上位へ探索し、project root を解決します。 |
| `nilo version` | package version と configured Notion API version を表示します。 |
| `nilo config --global --show` | token を表示せず、global configuration status を表示します。 |
| `nilo config --global user.token <token>` | user-level Notion token を設定します。 |
| `nilo config --global user.name <name>` | user-level display name を設定します。 |
| `nilo config --local --show` | 現在の directory tree の project-local configuration を表示します。 |

## 例

```bash
nilo init --project-name "Demo"
nilo pwd
nilo version --json
nilo config --global user.token ntn_xxx
nilo config --global user.name "Ada"
nilo config --global --show
nilo config --local --show --json
```

グローバル設定は token と runtime settings を保存します。project-local configuration は token を保存しません。通常の利用では `user_id` の設定は不要です。現在の token identity を確認する場合は `nilo auth whoami --json` を使います。
