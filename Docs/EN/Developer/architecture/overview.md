# Architecture Overview

This document defines the implementation boundaries for the current N.I.L.O. repository.

## Goal

N.I.L.O. provides a local Notion MCP server with three main layers:

- Core: the single business logic layer.
- CLI: the git-like local command interface for humans.
- MCP Tool: the structured Agent/LLM interface.

User installation, Notion connection setup, and command usage live under `Docs/EN/User/`. This developer section documents implementation boundaries.

## Target Structure

```text
Human -> CLI -> Core
Agent / LLM -> MCP Tool -> Core
```

Required:

```text
CLI -> Core
MCP Tool -> Core
```

Forbidden:

```text
MCP tools invoking shell command strings
CLI -> Notion SDK
MCP Tool -> Notion SDK
```

## Core

Core is the only business logic layer. It owns:

- Global configuration reads/writes, project context resolution, and token redaction.
- Centralized Notion API version, timeout, and retry handling.
- Notion SDK-compatible client creation.
- Auth validation and user/bot identity lookup.
- Domain services for:
  - pages
  - blocks
  - databases
  - data sources
  - users
  - comments
  - views
  - file uploads
  - search
  - custom emojis
- The Raw API registry and controlled fallback calls.
- Local audit records and a shared error model.

## CLI

The CLI is the human entrypoint. It owns:

- Git-like command structure.
- Human-readable output.
- `--json` output.
- `--dry-run` previews.
- Local MCP server lifecycle commands.

Public server commands include:

```text
nilo server run
nilo server status
nilo server stop
nilo server logs
nilo server remove
nilo server stdio
```

CLI resource commands call Core services for Notion operations.

The project-local `.notion_mcp/` directory stores only project context and attachment state. It does not store tokens. Global configuration stores the token, display name, and Notion API version.

## MCP Tool

MCP tools are the Agent/LLM entrypoint. They own:

- Tool inventory.
- Input schemas.
- Tool annotations.
- Structured errors.
- Confirmation requirements for dangerous operations.

MCP tools call Core services directly. They do not construct CLI command strings.

## Non-Functional Boundaries

- Tokens must not appear in normal CLI output or MCP configuration status.
- CLI and MCP write operations must support dry-run previews or dangerous-operation confirmation where appropriate.
- Live tests are skipped by default and must run only against explicit test pages, databases, data sources, or workspaces.
- Notion-Version is managed by Core configuration and must not be scattered through CLI, MCP tools, or individual services.
