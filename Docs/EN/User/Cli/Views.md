# Views CLI

View commands read and manage Notion views.

## Commands

| Command | Purpose |
| --- | --- |
| `nilo view retrieve <view_id>` | Read view information. |
| `nilo view list <database_id>` | List views under a database. |
| `nilo view query <view_id>` | Query a view. |
| `nilo view create` | Create a view. |
| `nilo view update <view_id>` | Update a view. |

## Examples

```bash
nilo view retrieve <view_id> --json
nilo view list <database_id> --json
nilo view query <view_id> --payload '{"page_size": 10}'
nilo view create --payload '{}'
nilo view update <view_id> --payload '{}'
```
