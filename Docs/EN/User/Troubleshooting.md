# Troubleshooting

This document lists common local configuration and MCP client issues.

## Token Is Not Configured

Set the global token and optional display name:

```bash
nilo config --global user.token ntn_xxx
nilo config --global user.name "Ada"
```

Then verify the saved status:

```bash
nilo config --global --show
```

The status output masks the token and does not print the raw secret.

## Token Has No Access

Confirm that the Notion internal connection is allowed to access the target page, database, or workspace content.

If a page or database cannot be found, first check Notion sharing and connection access. The API often returns permission-looking failures when the object was never shared with the connection.

## Identity Does Not Match Expectations

Most users do not need to set `user_id`. If an advanced configuration includes `user_id` and `nilo auth validate` reports a mismatch, inspect the token identity:

```bash
nilo auth whoami --json
```

Internal Notion connections usually identify as bot users.

## MCP Client Does Not Start

Check that the local command exists:

```bash
nilo --help
nilo server stdio --help
nilo server run --help
```

For stdio clients, use command and args as separate fields:

```json
{
  "command": "nilo",
  "args": ["server", "stdio"]
}
```

Do not put the entire command line into a single `command` field unless the MCP client explicitly requires that format.

For streamable HTTP clients, check the background server:

```bash
nilo server status
nilo server logs --tail 100
```

## Notion API Version Mismatch

The default Notion API version is `2026-03-11`. If Notion rejects a payload, compare the field names and object shape with the Notion API documentation for that version.

## Rate Limits

If Notion returns a rate limit error, reduce concurrency and batch size. Agent workflows should split large edits into smaller groups.
