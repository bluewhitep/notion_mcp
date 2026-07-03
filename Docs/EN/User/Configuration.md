# Configuration

This document explains how to prepare a Notion internal connection, save the global token, and create project-local `.notion_mcp/` context.

## Prepare Notion Access

Before configuring `nilo`, create a Notion internal connection and grant it access to the pages or databases you want to use.

1. Create a Notion internal connection.
   - Open the Notion Developer portal.
   - Create a new connection under Build / Internal connections.
   - Set a clear `Connection name`, for example `nilo-local`.
   - Use `Access token` as the authentication method. N.I.L.O. uses Notion bearer tokens and does not use OAuth in the current user flow.
   - Select the workspace.
   - Copy the installation access token from the connection configuration page.
   - The token usually starts with `ntn_` or `secret_`.

2. Configure connection capabilities.
   - Content capabilities:
     - `Read content` is required for reading pages, blocks, databases, and data sources.
     - `Update content` is required for updating page properties, updating blocks, and trashing pages or blocks.
     - `Insert content` is required for creating pages, database entries, child pages, child databases, and appended blocks.
   - Comment capabilities:
     - `Read comments` is required for listing comments.
     - `Insert comments` is required for creating comments or replies.
   - User capabilities:
     - `Read user information without email addresses` is usually enough for `nilo auth whoami` and identity validation.
     - Enable email access only when you explicitly need email addresses.

3. Share the connection with target content.
   - Option A: select allowed pages or databases from the connection's Content access page in the Developer portal.
   - Option B: open a Notion page, use the `...` menu, choose Connections / Add connection, and select the connection.
   - After a parent page is shared, child pages under it are usually accessible too.
   - If the API returns 403 or cannot find an object, first check that the page or database is shared with the connection.

4. Get a page ID.
   - Open the target page in Notion.
   - Use Share / Copy link.
   - The 32-character UUID, with or without hyphens, is the page ID.
   - The CLI can also parse Notion URLs and Markdown links directly:

```bash
nilo page attach "https://www.notion.so/Example-3799a1afb97a80489bb0e7384f334958?source=copy_link"
nilo page retrieve "[Example](https://www.notion.so/Example-3799a1afb97a80489bb0e7384f334958?source=copy_link)"
```

5. Get a database ID.
   - Open the database as a full page.
   - Use Share / Copy link.
   - The database ID is the UUID segment after the workspace path and before query parameters such as `?v=`.
   - A linked database is not the original database. Share the original database with the connection.

6. Get a data source ID.
   - In the current Notion API, a database is a container and a data source is a concrete table under that container.
   - After setting the token and sharing the database, run:

```bash
nilo database sources <database_id>
```

   - If the database has one data source, `database attach` can select it automatically.
   - If it has multiple data sources, pass `--data-source <data_source_id_or_name>`.

7. Check the token identity.
   - Most users do not need to set `user_id`.
   - Save the global token, then inspect the identity:

```bash
nilo config --global user.token ntn_xxx
nilo auth whoami --json
```

   - Internal connections usually identify as bot users.
   - `nilo auth validate` checks whether the token can be used.

Reference:

- [Notion Internal connections](https://developers.notion.com/guides/get-started/internal-integrations)
- [Notion Developer quickstart](https://developers.notion.com/docs/create-a-notion-integration)
- [Notion Working with databases](https://developers.notion.com/guides/data-apis/working-with-databases)
- [Notion User object](https://developers.notion.com/reference/user)

## Global Configuration

Global configuration stores user-level runtime settings such as the Notion token, display name, Notion API version, timeout, and retry settings.

The default path is:

```text
~/.notion_mcp/config.json
```

Use `NOTION_MCP_CONFIG` to point to another file:

```bash
NOTION_MCP_CONFIG=/path/to/config.json nilo config --global --show
```

Common commands:

```bash
nilo config --global user.token ntn_xxx
nilo config --global user.name "Ada"
nilo config --global --show
nilo config --global --show --json
```

`nilo config --global --show` reports whether a token is set, but it does not print the raw token.

## Project-Local Configuration

Project-local configuration lets the CLI discover context by walking upward from the current directory, similar to Git. Inside a project directory, you can avoid repeatedly passing page IDs, database IDs, and data source IDs.

Project-local configuration lives at:

```text
.notion_mcp/config.json
```

It does not store the token. Tokens stay in global configuration.

Initialize the current directory:

```bash
nilo init --project-name "Demo"
nilo init --workspace-hint "Team Workspace" --json
```

Inspect local context:

```bash
nilo config --local --show
nilo config --local --show --json
nilo pwd
```

Example local configuration:

```json
{
  "schema_version": 1,
  "project_name": "Demo",
  "workspace_hint": "Team Workspace",
  "settings": {
    "prefer_attached_page": true,
    "prefer_attached_database": true,
    "json_output_default": false
  }
}
```

## Page Attachment

`page attach` binds a default page for the current project. It does not upload files.

```bash
nilo page attach <page_id>
nilo page status
nilo page retrieve
nilo page blocks
```

Detach the default page:

```bash
nilo page detach
```

Refresh local page state:

```bash
nilo page refresh
```

`page refresh` pulls title, URL, and status from Notion and updates local state. It does not modify the remote page.

## Database Attachment

A database is a container, and a data source is the concrete table under that container. Database attachment stores both the bound database and the active data source.

```bash
nilo database attach <database_id>
nilo database attach <database_id> --data-source <data_source_id_or_name>
nilo database status
nilo database query --payload '{"page_size": 10}'
```

Detach the database:

```bash
nilo database detach
```

Refresh local database state:

```bash
nilo database refresh
```

`database refresh` pulls database title, URL, data sources, and status from Notion. It does not modify the remote database.

## Common Workflows

Set the global token and initialize the current repository:

```bash
nilo config --global user.token ntn_xxx
nilo config --global user.name "Ada"
nilo config --global --show
nilo init --project-name "Demo"
nilo config --local --show
```

Attach a page and read it:

```bash
nilo page attach <page_id>
nilo page retrieve
nilo page blocks --tree
```

Attach a database and query the active data source:

```bash
nilo database attach <database_id> --data-source Tasks
nilo database sources
nilo database query --payload '{"page_size": 10}'
```

Operate on a data source explicitly:

```bash
nilo data-source query <data_source_id> --payload '{"page_size": 10}'
nilo data-source property rename <data_source_id> Status State
```
