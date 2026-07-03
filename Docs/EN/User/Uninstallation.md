# Uninstallation

This document explains how to remove the local `nilo` command and, when needed, clean local configuration and MCP runtime state.

Uninstalling N.I.L.O. does not delete Notion pages, databases, blocks, or comments. It also does not revoke the Notion internal connection token in the Notion Developer portal.

## Quick Uninstall

Use the command that matches your original installation method.

### Persistent uv Install

```bash
uv tool uninstall notion-nilo
```

### Temporary uv Run

No uninstall step is needed. A temporary `uv run --with ...` command does not install a persistent `nilo` executable.

### pip Install

```bash
pip uninstall notion-nilo
```

## Full Cleanup

Use this section when you also want to remove MCP client configuration, background server state, local token configuration, or project-local context.

### Stop and Remove Background Server State

Check whether a streamable HTTP server is running:

```bash
nilo server status
```

Stop it:

```bash
nilo server stop
```

Remove local server runtime state and logs:

```bash
nilo server remove
```

If cleanup needs to stop a still-running process, use:

```bash
nilo server remove --force
```

The default runtime directory is derived from the global configuration path. The default global configuration path is `~/.notion_mcp/config.json`, so server state and logs usually live under `~/.notion_mcp/`. If `NOTION_MCP_RUNTIME_DIR` is set, that environment variable controls the runtime directory.

### Remove MCP Client Configuration

For a stdio MCP client, remove the `nilo` server entry:

```json
{
  "mcpServers": {
    "nilo": {
      "command": "nilo",
      "args": ["server", "stdio"]
    }
  }
}
```

For a streamable HTTP MCP client, remove this local URL:

```text
http://127.0.0.1:8000/mcp
```

If the client configuration includes `NOTION_MCP_CONFIG`, remove that environment entry too.

### Uninstall the Command

For `uv tool install .`:

```bash
uv tool uninstall notion-nilo
```

For `pip install /path/to/notion-nilo`:

```bash
pip uninstall notion-nilo
```

After uninstalling, check whether another installation still provides the command:

```bash
nilo --help
```

If the command still exists, inspect your shell `PATH`, shell aliases, and other Python environments.

### Optional: Delete Global Configuration

The global configuration stores the Notion token, display name, Notion API version, timeout, and retry settings. The default path is:

```text
~/.notion_mcp/config.json
```

Delete it only when you no longer need this local token configuration:

```bash
rm -f ~/.notion_mcp/config.json
```

If you used a custom configuration path, delete that file instead:

```bash
rm -f /path/to/config.json
```

### Optional: Delete Project-Local Context

The project-local `.notion_mcp/` directory stores local context such as default page/database bindings, project settings, state, cache, and logs. It does not store the global Notion token.

From the project root, remove it only when that project no longer needs its local Notion context:

```bash
rm -rf .notion_mcp
```

This deletes only local project context. It does not modify remote Notion content.

### Optional: Revoke Notion Access

To invalidate the token or prevent the connection from accessing content, revoke the internal connection token in Notion or remove the connection from the relevant pages and databases.

Local uninstall commands cannot perform this Notion-side revocation.

## Verify Cleanup

After uninstalling the persistent command, this should either fail or reveal another installation:

```bash
nilo --help
```

If you deleted the global configuration too, reinstalling N.I.L.O. later requires setting the token again. See [Configuration](Configuration.md).
