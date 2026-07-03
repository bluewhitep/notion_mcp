# Project Config CLI

This page covers project context and configuration commands.

## Commands

| Command | Purpose |
| --- | --- |
| `nilo init` | Create project-local `.notion_mcp/` context in the current directory. |
| `nilo pwd` | Resolve the current project root by walking upward from the current directory. |
| `nilo version` | Show the package version and configured Notion API version. |
| `nilo config --global --show` | Show global configuration status without revealing the token. |
| `nilo config --global user.token <token>` | Set the user-level Notion token. |
| `nilo config --global user.name <name>` | Set the user-level display name. |
| `nilo config --local --show` | Show project-local configuration for the current directory tree. |

## Examples

```bash
nilo init --project-name "Demo"
nilo pwd
nilo version --json
nilo config --global user.token ntn_xxx
nilo config --global user.name "Ada"
nilo config --global --show
nilo config --local --show --json
```

Global configuration stores the token and runtime settings. Project-local configuration does not store the token. Most users do not need to set `user_id`; run `nilo auth whoami --json` when you need to inspect the current token identity.
