# 开发计划与追踪

本文档记录当前 legacy prototype 的历史完成范围。完整补全计划以 `Docs/dev/Feature_Completion_Plan.md` 为准。

## 当前定位

本文件中的已完成项目只表示 FastAPI REST 原型完成，不表示真正的本地 Notion MCP server 已完成。

当前仓库已经进入新的补全阶段：

- 阶段 0：修复 packaging 和 `src/` layout。
- 阶段 1：修正顶层文档。
- 阶段 2：建立 Core 层。
- 阶段 3：补全 git-like CLI。
- 阶段 4：实现真正 MCP server 和 MCP tools。
- 阶段 5：补齐 Notion SDK/API 覆盖。
- 阶段 6：补齐场景测试和 live 测试。
- 阶段 7：同步开发者和使用者文档。
- 阶段 8：发布前验收。

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

后续开发必须从 `Docs/dev/Feature_Completion_Plan.md` 推进。

阶段进度记录在：

```text
Docs/dev/progress.md
```

测试规则记录在：

```text
Docs/dev/test_policy.md
```

## 执行规则

- 每个阶段先写测试，再写实现。
- 现有 legacy 测试不得为了通过而修改。
- 新增补充测试必须在 `Docs/dev/progress.md` 记录原因。
- 每个阶段完成后更新开发者文档。
- 必要时更新使用者文档。
- 真实环境测试默认跳过，并记录启用条件。
