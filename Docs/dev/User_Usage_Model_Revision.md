# 用户使用模型变更记录

本文已被正式 ADR 取代：

- `Docs/dev/ADR-002-local-context-and-cli-v2.md`
- `Docs/dev/ADR-003-project-attach-context.md`

ADR-002 的状态为 `Accepted / 待实施`，并记录以下 v2 设计决议：

- Git-like 本地目录上下文配置。
- 全局配置保存 token，本地配置不保存 token。
- Page CLI 作为普通用户编辑页面内容的主入口。
- Block CLI 作为高级/底层入口。
- Database 和 DataSource 在 Core/API/MCP 层严格分离。
- Raw API 只作为兜底和高级入口。

ADR-003 的状态为 `Design Accepted / 待实现`，并覆盖 ADR-002 中项目级目录命名的早期设计：

- ADR-002 早期命名：`.notion-mcp/config.json`
- ADR-003 最终命名：`.notion_mcp/config.json`

ADR-003 还新增 page/database attach workflow：

- `.notion_mcp/state/page.attach.json`
- `.notion_mcp/state/database.attach.json`
- `project init/status/root`
- `page attach/status/refresh/detach/deattach`
- `database attach/status/refresh/detach/deattach`

当前已实现命令仍以 `Docs/User/Cli.md`、`Docs/Developer/api/cli.md` 和源码为准。ADR-002/ADR-003 中列出的新增命令是计划能力，不表示当前 CLI 已经可用。
