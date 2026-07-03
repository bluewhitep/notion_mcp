# Raw API CLI

Raw API is an advanced fallback entrypoint. It should not be the normal path for page, database, or block editing.

## Commands

| Command | Purpose |
| --- | --- |
| `nilo raw-api operations` | List currently registered raw API operation names. |
| `nilo raw-api invoke <operation>` | Call a registered raw API operation. |

## Examples

```bash
nilo raw-api operations
nilo raw-api invoke search --arguments '{"query": "Tasks"}' --json
```
