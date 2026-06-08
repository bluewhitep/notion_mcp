# 测试政策

本文档记录本仓库补全 Notion MCP 功能时必须遵守的测试规则。它面向开发者，不面向普通使用者。

## 基本规则

- 所有新功能、函数、命令、MCP tool、文档检查和场景能力必须先创建测试，再实现代码。
- 已存在测试不得为了通过而修改。
- 当既有测试覆盖不足或需求变化需要补充断言时，只能新增测试文件或新增版本化测试，例如 `tests/v2/`、`tests/v3/` 或更明确的场景测试。
- 每次新增补充测试时，必须在 `Docs/dev/progress.md` 记录新增原因。
- 若重构导致旧测试失败，优先通过兼容层或实现修复保持旧行为，不能直接改旧测试绕过失败。

## 测试分层

- `tests/test_*.py`：legacy 原型测试，保持不修改。
- `tests/v2/core/`：Core 层测试。
- `tests/v2/cli/`：CLI 命令测试。
- `tests/v2/mcp_server/`：MCP server 和 MCP tool 测试。
- `tests/v2/scenarios/`：安装、运行、CLI 到 Core、MCP 到 Core 等场景测试。
- `tests/live/`：需要真实 Notion token、测试 workspace、付费计划或 Notion AI 权限的测试；默认跳过。

## live 测试规则

- live 测试默认跳过。
- live 测试必须声明启用环境变量、所需 token、测试页面或测试 workspace。
- live 写入测试不得修改生产页面；只能写入明确授权的测试页面或测试 workspace。
- 未运行 live 测试时，不得声称真实环境已通过。
