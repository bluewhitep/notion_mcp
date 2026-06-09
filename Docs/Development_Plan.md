# 开发计划与追踪

本文档记录 legacy prototype 的历史完成范围。当前开发计划、进度记录和测试策略保存在开发文档目录中。

## 当前定位

本文件中的已完成项目只表示 FastAPI REST 原型完成，不表示真正的本地 Notion MCP server 已完成。

当前仓库已从 legacy REST 原型扩展为包含 Core、CLI 和 MCP Tool 的本地 Notion MCP 项目。

## legacy prototype 已完成范围

以下内容属于 legacy prototype：

- 配置模型和配置读写。
- `notion-mcp init`、`set-token`、`set-user`、`show`、`run`。
- FastAPI 根路由健康检查。
- legacy REST 路由：
  - databases
  - pages
  - blocks
- mock 单元测试。
- 初版 `Docs/Requirements.md`、`Docs/Design.md`、`Docs/TechStack.md`、`Docs/Developer/API.md`、`Docs/User/Guide.md`。

## 新计划入口

后续开发应查看开发文档目录中的计划、进度和测试规则文件。

## 执行规则

- 新功能先写测试，再写实现。
- 现有 legacy 测试不得为了通过而修改。
- 新增补充测试必须在开发进度文档中记录原因。
- 每次功能完成后更新开发者文档。
- 必要时更新使用者文档。
- 真实环境测试默认跳过，并记录启用条件。
