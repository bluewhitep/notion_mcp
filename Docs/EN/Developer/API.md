# Developer API Index

This index is for maintainers and contributors who need to understand the repository's public implementation surfaces. The project has moved beyond the original REST prototype and now centers on a local Notion MCP server.

## Current Interface Status

- `src/nilo/core/` is the single business logic layer shared by the CLI, MCP tools, and compatibility code.
- `src/nilo/server.py` and `src/nilo/routes/` are internal REST prototype compatibility code. They are not the public server CLI entrypoint and they are not the final MCP tool interface.
- `src/nilo/cli/` is the git-like human-facing CLI. It calls Core services.
- `src/nilo/mcp_server/` contains the MCP server and MCP tools. It is the structured Agent/LLM entrypoint and calls Core services.

## Documentation Entrypoints

- Core API: [api/core.md](api/core.md)
- CLI API: [api/cli.md](api/cli.md)
- Core tests: [testing/core.md](testing/core.md)
- CLI tests: [testing/cli.md](testing/cli.md)
- MCP tests: [testing/mcp.md](testing/mcp.md)
- Live tests: [testing/live.md](testing/live.md)
- Scenario tests: [testing/scenarios.md](testing/scenarios.md)
- MCP tool contracts: [mcp_tools/README.md](mcp_tools/README.md)

## Call Boundaries

The required call graph is:

```text
Human -> CLI -> Core
Agent / LLM -> MCP Tool -> Core
```

Keep these boundaries intact. MCP tools must not shell out to CLI strings, and CLI/MCP layers must not duplicate business logic independently.
