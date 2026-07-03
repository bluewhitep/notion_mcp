# Config Tools

- `config_status`
  - Description: returns local configuration status, redacted configuration, and capability flags.
  - Required parameters: none.
  - Returns: `configured`, `config`, and `capabilities`.
- `config_get`
  - Description: reads one configuration field.
  - Required parameters: `key`.
  - Optional parameters: `show_secret`, default `false`.
  - Security: `notion_token` returns `********` by default.
