# 開発者 API 索引

この索引は、repository の実装 surface を確認する maintainer / contributor 向けです。現在の実装は、初期 REST prototype ではなく、N.I.L.O. のローカル MCP server を中心に構成されています。

## 現在の interface 状態

- `src/nilo/core/` は唯一の business logic layer です。CLI、MCP tools、compatibility code から共有されます。
- `src/nilo/server.py` と `src/nilo/routes/` は内部 REST prototype compatibility code です。公開 server CLI entrypoint でも、最終 MCP tool interface でもありません。
- `src/nilo/cli/` は人間向けの git-like CLI です。Core services を呼び出します。
- `src/nilo/mcp_server/` は MCP server と MCP tools を含みます。Agent/LLM 向けの structured entrypoint で、Core services を呼び出します。

## 文書入口

- Core API: [api/core.md](api/core.md)
- CLI API: [api/cli.md](api/cli.md)
- Core tests: [testing/core.md](testing/core.md)
- CLI tests: [testing/cli.md](testing/cli.md)
- MCP tests: [testing/mcp.md](testing/mcp.md)
- Live tests: [testing/live.md](testing/live.md)
- Scenario tests: [testing/scenarios.md](testing/scenarios.md)
- MCP tool contracts: [mcp_tools/README.md](mcp_tools/README.md)

## 呼び出し境界

必要な call graph:

```text
Human -> CLI -> Core
Agent / LLM -> MCP Tool -> Core
```

MCP tools は CLI command string を実行してはいけません。CLI/MCP layer は business logic を独自に複製せず、Core services を使います。
