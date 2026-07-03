# 开发者接口索引

本文档面向开发者，说明当前仓库的接口文档入口。当前项目已经从 REST 原型补全为 N.I.L.O. 本地 MCP server。

## 当前接口状态

- `src/nilo/core/`：唯一业务逻辑层，供 CLI、MCP Tool 和兼容代码复用。
- `src/nilo/server.py` 与 `src/nilo/routes/`：内部 REST 原型兼容代码，不是公开 server CLI 入口，也不是最终 MCP Tool 接口。
- `src/nilo/cli/`：git-like CLI，人类入口，调用 Core。
- `src/nilo/mcp_server/`：MCP server 和 MCP tools，Agent/LLM 结构化入口，调用 Core。

## 文档入口

- Core API：`Docs/ZH/Developer/api/core.md`
- CLI API：`Docs/ZH/Developer/api/cli.md`
- Core 测试：`Docs/ZH/Developer/testing/core.md`
- CLI 测试：`Docs/ZH/Developer/testing/cli.md`
- MCP 测试：`Docs/ZH/Developer/testing/mcp.md`
- Live 测试：`Docs/ZH/Developer/testing/live.md`
- 场景测试：`Docs/ZH/Developer/testing/scenarios.md`
- MCP Tool contract：`Docs/ZH/Developer/mcp_tools/README.md`

## 调用边界

目标调用关系必须保持为：

```text
Human -> CLI -> Core
Agent / LLM -> MCP Tool -> Core
```

禁止 MCP Tool 通过 CLI 字符串调用，也禁止 CLI 和 MCP Tool 各自复制业务逻辑。
