# CLI Overview

このページでは CLI 全体の共通動作を説明します。

## 共通ルール

- `-h` と `--help` は同じです。例: `nilo -h`、`nilo page -h`。
- 多くの read command は scripts や agents 向けに `--json` をサポートします。
- write、update、send、complete、trash など副作用のある command は、可能な場合 `--dry-run` で事前確認します。
- JSON input は `--payload`、`--properties`、`--arguments` で渡します。値は JSON object である必要があります。
- `page/pages`、`block/blocks`、`database/databases` などの複数形は alias です。ユーザー文書では通常単数形を使います。
- 実際の Notion call の前に `nilo config --global user.token <token>` で token を設定し、対象 content を Notion connection に共有してください。

## JSON input 例

```bash
nilo page update <page_id> --payload '{"properties": {}}'
nilo database query --payload '{"page_size": 10}'
nilo raw-api invoke search --arguments '{"query": "Tasks"}' --json
```

## 副作用の preview

```bash
nilo block append <block_id> --payload '{"children": []}' --dry-run --json
nilo block trash <block_id> --dry-run
```
