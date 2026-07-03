# Database DataSource CLI

This page covers database container commands, data source commands, and database shortcuts.

In the current Notion API model, a database is a container and a data source is the concrete table inside that container.

- Use `database` for container-level operations.
- Use `data-source` when operating on an explicit data source.
- Use database shortcuts only when they target the active data source attached to the current project.

## Database Container Commands

| Command | Purpose |
| --- | --- |
| `nilo database attach <database_id>` | Attach a default database for the current project. If there is one data source, it can be selected automatically. |
| `nilo database attach <database_id> --data-source <id_or_name>` | Attach a database and explicitly select the active data source. |
| `nilo database status` | Show the attached database and active data source. |
| `nilo database refresh` | Refresh local title, URL, data source list, and status without changing the remote database. |
| `nilo database detach` | Remove the local database binding without changing the remote database. |
| `nilo database retrieve` | Read the attached database container. |
| `nilo database retrieve <database_id>` | Read a specific database container. |
| `nilo database sources` | List data sources under the attached database. |
| `nilo database sources <database_id>` | List data sources under a specific database. |
| `nilo database create` | Create a database container and its initial data source. |
| `nilo database create --parent-page <page_id>` | Create a database container under a specific parent page. |
| `nilo database update <database_id>` | Update container-level fields such as title, description, icon, or cover. |
| `nilo database rename <database_id> <new_name>` | Rename the database container. |

Examples:

```bash
nilo database attach <database_id> --data-source Tasks
nilo database status
nilo database sources
nilo database create --parent-page <page_id> --payload '{"title": []}'
nilo database update <database_id> --payload '{"title": []}'
```

## Database Shortcuts

These commands operate on the active data source of the attached database.

| Command | Purpose |
| --- | --- |
| `nilo database query --payload '<json>'` | Query the active data source. |
| `nilo database page create` | Create a page or entry in the active data source. |
| `nilo database property rename <property> <new_name>` | Rename a property in the active data source. |

Examples:

```bash
nilo database query --payload '{"page_size": 10}'
nilo database page create --properties '{"Name": {"title": []}}'
nilo database property rename Status State
```

## DataSource Commands

| Command | Purpose |
| --- | --- |
| `nilo data-source retrieve <data_source_id>` | Read table-level data source information and schema. |
| `nilo data-source query <data_source_id>` | Query entries or pages in a specific data source. |
| `nilo data-source create` | Create a data source under the attached database. |
| `nilo data-source create <database_id>` | Create a data source under a specific database container. |
| `nilo data-source update <data_source_id>` | Update table-level properties or schema. |
| `nilo data-source templates <data_source_id>` | List available page templates for a data source. |
| `nilo data-source property rename <data_source_id> <property> <new_name>` | Rename a property in a specific data source. |
| `nilo data-source page create <data_source_id>` | Create a page or entry in a specific data source. |

Examples:

```bash
nilo data-source query <data_source_id> --payload '{"page_size": 10}'
nilo data-source create <database_id> --payload '{"name": "Tasks", "properties": {}}'
nilo data-source property rename <data_source_id> Status State
nilo data-source page create <data_source_id> --properties '{"Name": {"title": []}}'
```
