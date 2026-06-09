# ADR-004: CLI Command Surface Consolidation

Status: Accepted / implementation in progress.

This ADR records the command naming decisions for the human-facing CLI. It supersedes older examples that exposed `project`, `local`, `page content`, page-scoped block editing, `current`, `deattach`, and explicit data source operations under `database`.

## Decisions

1. Project initialization is `notion-mcp init`.
2. Project root lookup is `notion-mcp pwd`.
3. Global config uses `notion-mcp config --global`.
4. Project-local config uses `notion-mcp config --local`.
5. Global status is `notion-mcp config --global --show`.
6. Project-local status is `notion-mcp config --local --show`.
7. Token setup is `notion-mcp config --global user.token <token>`.
8. User display name setup is `notion-mcp config --global user.name <name>`.
9. Root `status`, `project *`, `local *`, `config global *`, `config local *`, and `config set/get/unset/list` are not public commands. They may remain hidden compatibility entries only.
10. `notion-mcp version` shows the Notion MCP package version and configured Notion API version.
11. `page attach` means binding the current project default page. It is not a file attachment workflow.
12. `page retrieve` reads page metadata. `page blocks` reads block summaries. `page content` is not public.
13. Block editing is top-level: `block append`, `block insert-after`, `block update`, and `block trash`.
14. Page creation is `page create`; when an attached page exists, it can provide the default parent.
15. Database creation is `database create`; it creates a database container and initial data source.
16. Database update is container-level only. Data source schema updates use `data-source update`.
17. Explicit data source operations use `data-source`.
18. `database query`, `database page create`, and `database property rename` are shortcuts for the current attached database active data source only.
19. `page current`, `database current`, `page deattach`, and `database deattach` are not public commands.
20. `insert-before` is not a stable public command.

## Public Command List

```text
notion-mcp init
notion-mcp pwd
notion-mcp version
notion-mcp config --global --show
notion-mcp config --local --show
notion-mcp config --global user.token <token>
notion-mcp config --global user.name <name>

notion-mcp page attach <page_id>
notion-mcp page status
notion-mcp page refresh
notion-mcp page detach
notion-mcp page retrieve
notion-mcp page retrieve <page_id>
notion-mcp page blocks
notion-mcp page blocks <page_id>
notion-mcp page create
notion-mcp page create --parent-page <page_id>
notion-mcp page update <page_id>

notion-mcp block append <block_id>
notion-mcp block insert-after <block_id>
notion-mcp block update <block_id>
notion-mcp block trash <block_id>

notion-mcp database attach <database_id>
notion-mcp database attach <database_id> --data-source <id_or_name>
notion-mcp database status
notion-mcp database refresh
notion-mcp database detach
notion-mcp database retrieve
notion-mcp database retrieve <database_id>
notion-mcp database sources
notion-mcp database sources <database_id>
notion-mcp database create
notion-mcp database create --parent-page <page_id>
notion-mcp database update <database_id>
notion-mcp database rename <database_id> <new_name>
notion-mcp database query --payload <json>
notion-mcp database page create
notion-mcp database property rename <property> <new_name>

notion-mcp data-source retrieve <data_source_id>
notion-mcp data-source query <data_source_id>
notion-mcp data-source create
notion-mcp data-source create <database_id>
notion-mcp data-source update <data_source_id>
notion-mcp data-source templates <data_source_id>
notion-mcp data-source property rename <data_source_id> <property> <new_name>
notion-mcp data-source page create <data_source_id>
```

Other already implemented Notion object domains remain available: auth, user, comment, view, file-upload, search, custom-emoji, raw-api, mcp, and legacy compatibility root commands.
