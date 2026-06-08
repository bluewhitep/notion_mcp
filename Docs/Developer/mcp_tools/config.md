# Config Tools

- `config_status`
  - 说明：返回本地配置状态、脱敏配置和能力标记。
  - 必选参数：无。
  - 返回：`configured`、`config`、`capabilities`。
- `config_get`
  - 说明：读取一个配置字段。
  - 必选参数：`key`。
  - 可选参数：`show_secret`，默认 `false`。
  - 安全：`notion_token` 默认返回 `********`。
