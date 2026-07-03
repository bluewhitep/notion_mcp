# Auth And User CLI

This page covers authentication checks and Notion user lookup commands.

## Commands

| Command | Purpose |
| --- | --- |
| `nilo auth validate` | Check whether the current token can be used. |
| `nilo auth whoami` | Show the Notion identity behind the current token. Most users only use this for inspection. |
| `nilo user me` | Read the current user or bot. |
| `nilo user list` | List workspace users. |
| `nilo user retrieve <user_id>` | Read one user by ID. |

## Examples

```bash
nilo auth validate
nilo auth whoami --json
nilo user me --json
nilo user list --json
nilo user retrieve <user_id> --json
```
