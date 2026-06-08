# notion-mcp

This repository provides a local Notion MCP server with a Core + CLI + MCP Tool architecture.

Current state:

- Core is the only business logic layer.
- CLI is the git-like human entrypoint.
- MCP tools are the structured Agent/LLM entrypoint.
- Legacy FastAPI REST routes are retained only for compatibility.

Use `Docs/User/installation.md` and `Docs/User/mcp_clients.md` for setup and client configuration.
