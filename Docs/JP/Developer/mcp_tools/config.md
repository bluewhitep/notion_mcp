# Config Tools

- `config_status`
  - 説明: local configuration status、redacted configuration、capability flags を返します。
  - Required parameters: none.
  - Returns: `configured`, `config`, `capabilities`.
- `config_get`
  - 説明: configuration field を 1 つ読み取ります。
  - Required parameters: `key`.
  - Optional parameters: `show_secret`, default `false`.
  - Security: `notion_token` は default で `********` を返します。
