# User Guide

This guide is for people who want to run N.I.L.O. locally and use it from a terminal, an MCP client, or an automation agent. N.I.L.O. connects to the official Notion API through your own Notion internal connection token.

## Current Status

N.I.L.O. currently exposes two user-facing entrypoints:

- A git-like CLI named `nilo`.
- A local MCP server managed by `nilo server ...`.

For command details, see [CLI reference](Cli.md). For MCP client setup, see [MCP Clients](MCP_Clients.md).

## Prerequisites

1. Create a Notion internal connection and copy its installation access token.
2. Grant that connection access to the pages or databases you want to use.
3. Install Python 3.10 or newer.
4. Install `uv` if you want the recommended installation flow.

## Installation

The recommended local installation flow uses `uv` from the repository root:

```bash
cd /path/to/notion-nilo
uv tool install .
nilo --help
```

If `uv` is not available, install from the local path with `pip`:

```bash
pip install /path/to/notion-nilo
nilo --help
```

For the full installation, update, and uninstall flows, see [Installation](Installation.md) and [Uninstallation](Uninstallation.md).

## Initial Configuration

Set the global Notion token before calling Notion APIs. Most users do not need to set a `user_id` manually.

```bash
# Set the global token and optional display name.
nilo config --global user.token ntn_xxx
nilo config --global user.name Ada

# Check the saved configuration and token status.
nilo config --global --show --json

# Check the Notion identity behind the current token.
nilo auth whoami --json
```

The default global configuration file is `~/.notion_mcp/config.json`. Set `NOTION_MCP_CONFIG` if you need a different path.

## Start the MCP Server

For command-based stdio MCP clients, configure the client to run:

```bash
nilo server stdio
```

For clients that connect to a streamable HTTP MCP URL, start the local server first:

```bash
nilo server run --host 127.0.0.1 --port 8000
nilo server status
```

Then configure the client with:

```text
http://127.0.0.1:8000/mcp
```

See [MCP Clients](MCP_Clients.md) for complete client configuration examples.

## CLI Examples

```bash
nilo page retrieve <page_id> --json
nilo data-source query <data_source_id> --json
nilo block children <block_id> --json
```

IDs can usually be copied from Notion page or database URLs. The CLI also accepts many Notion URLs directly and normalizes the ID internally.

## FAQ

### Why does N.I.L.O. say the Notion token is not configured?

The global token has not been saved yet. Run:

```bash
nilo config --global user.token ntn_xxx
```

### Do I need to enter my Notion user UUID?

Usually no. Run `nilo auth whoami --json` only when you need to inspect the identity behind the current token.

### Does N.I.L.O. support OAuth?

Not in the current user flow. The current release uses Notion internal connection tokens.

### What should I check when a call fails?

Most failures come from configuration, permissions, or request parameters:

1. Confirm the token is set and still valid.
2. Confirm the Notion connection can access the target page or database.
3. Confirm the payload matches the Notion API version in use.
4. Check the CLI output, MCP client log, or local server log.
