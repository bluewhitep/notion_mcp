# CLI Documentation

This page is the entrypoint for the `nilo` command-line interface. Commands are split by topic so page, block, database, configuration, and advanced fallback commands stay easy to scan.

## Start Here

- [Installation](Installation.md): install the `nilo` command.
- [Uninstallation](Uninstallation.md): uninstall the command and clean MCP client configuration, local token configuration, and project context.
- [Configuration](Configuration.md): prepare Notion access, save the token, and create project-local context.
- [MCP Clients](MCP_Clients.md): connect MCP-compatible tools to the local N.I.L.O. server.
- [Troubleshooting](Troubleshooting.md): diagnose common local and Notion API issues.

## CLI Sections

- [Overview](Cli/Overview.md): global rules, JSON payloads, `--dry-run`, and aliases.
- [Project Config](Cli/Project_Config.md): `init`, `pwd`, `version`, and `config --global/--local`.
- [Page](Cli/Page.md): attach a default page, read pages and blocks, create pages, and update pages.
- [Block](Cli/Block.md): append, insert-after, update, and trash block content.
- [Database DataSource](Cli/Database_DataSource.md): database containers, data source operations, and database shortcuts.
- [Auth And User](Cli/Auth_And_User.md): token validation, `whoami`, and user lookup.
- [Comments](Cli/Comments.md): list, create, and reply to comments.
- [Views](Cli/Views.md): retrieve, list, query, create, and update views.
- [File Uploads](Cli/File_Uploads.md): file upload lifecycle commands.
- [Search And Custom Emoji](Cli/Search_And_Custom_Emoji.md): workspace search and custom emoji lookup.
- [Raw API](Cli/Raw_API.md): advanced Raw API fallback.
- [MCP Server](Cli/MCP_Server.md): start, stop, inspect, and clean the local MCP server.

## Common First Steps

```bash
nilo config --global user.token ntn_xxx
nilo config --global --show
nilo init --project-name "Demo"
nilo page attach <page_id>
nilo page retrieve
nilo page blocks
```
