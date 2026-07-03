# MCP Server CLI

This page covers local MCP server lifecycle commands.

## Background HTTP Server

| Command | Purpose |
| --- | --- |
| `nilo server run` | Start the streamable HTTP MCP server in the background. |
| `nilo server status` | Show whether the server is running, plus PID, URL, and log path. |
| `nilo server stop` | Stop the background server process. |
| `nilo server logs` | Read background server logs. |
| `nilo server remove` | Stop the server and remove local runtime state. Logs are deleted by default. |

The default local server command is:

```bash
nilo server run --host 127.0.0.1 --port 8000
```

The MCP URL is:

```text
http://127.0.0.1:8000/mcp
```

Common management commands:

```bash
nilo server status
nilo server logs --tail 100
nilo server stop
nilo server remove
```

If a process does not exit normally, force stop it:

```bash
nilo server stop --force
```

## Stdio Server

For command-based MCP clients that launch a stdio process, use:

```bash
nilo server stdio
```

This command runs in the foreground until the MCP client closes it or the user interrupts it.

## Serve Alias

`nilo serve ...` is a compatibility alias for `nilo server ...`:

```bash
nilo serve run --host 127.0.0.1 --port 8000
```

New documentation should prefer `nilo server ...`.

For MCP client configuration fields, see [MCP Clients](../MCP_Clients.md).
