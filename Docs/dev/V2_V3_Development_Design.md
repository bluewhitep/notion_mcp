# V2/V3 Development Design: Local Context, Attach Runtime, and Human-Friendly CLI

Status: Drafted from accepted designs / Pending implementation.

This document converts accepted design decisions into an implementation-oriented development design. ADR-004 is the current source of truth for the public CLI command surface and supersedes older command examples in this document. Current behavior remains defined by source code, `Docs/User/Cli.md`, `Docs/Developer/api/cli.md`, and `Docs/dev/progress.md`.

Source decisions:

- `Docs/dev/ADR-002-local-context-and-cli-v2.md`
- `Docs/dev/ADR-003-project-attach-context.md`
- `Docs/dev/ADR-004-cli-command-surface-consolidation.md`

## Current Command Surface Revision

The public CLI command surface is now:

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
notion-mcp page retrieve [page_id]
notion-mcp page blocks [page_id]
notion-mcp page create [--parent-page <page_id>]
notion-mcp page update <page_id>

notion-mcp block append <block_id>
notion-mcp block insert-after <block_id>
notion-mcp block update <block_id>
notion-mcp block trash <block_id>

notion-mcp database attach <database_id> [--data-source <id_or_name>]
notion-mcp database status
notion-mcp database refresh
notion-mcp database detach
notion-mcp database retrieve [database_id]
notion-mcp database sources [database_id]
notion-mcp database create [--parent-page <page_id>]
notion-mcp database update <database_id>
notion-mcp database rename <database_id> <new_name>
notion-mcp database query --payload <json>
notion-mcp database page create
notion-mcp database property rename <property> <new_name>

notion-mcp data-source retrieve <data_source_id>
notion-mcp data-source query <data_source_id>
notion-mcp data-source create [database_id]
notion-mcp data-source update <data_source_id>
notion-mcp data-source templates <data_source_id>
notion-mcp data-source property rename <data_source_id> <property> <new_name>
notion-mcp data-source page create <data_source_id>
```

Hidden compatibility entries may remain for old scripts, but user docs and public help must not present them as official commands.

## Implementation Goals

The implementation adds a product layer above the existing Notion API wrapper:

1. Git-like project context discovery from `cwd`.
2. Project-local `.notion_mcp/` runtime state that never stores tokens.
3. Page attach workflow so users can run page commands without repeatedly passing `page_id`.
4. Database attach workflow with strict `database` / `data_source` separation.
5. Page CLI as the normal human editing entrypoint.
6. Block CLI as the lower-level advanced entrypoint.
7. Database CLI as a human-friendly shortcut layer and `data-source` CLI as the explicit table-level namespace.
8. MCP tools and CLI share Core services; neither calls the Notion SDK directly.
9. Raw API remains an advanced fallback, not the common page/database editing path.

## Non-Goals

This development track does not implement:

- OAuth.
- GUI.
- Remote Notion permission management.
- Full local cache/index.
- Synchronizing attach state to Notion.
- Multi-user conflict resolution for shared `.notion_mcp/state`.
- Stable `insert-before` support in the first implementation batch.

## Architecture

Target call graph:

```text
CLI ─────┐
         ├── Core ─── Notion SDK/API
MCP Tool ┘
```

Required boundaries:

- CLI parses human commands, formats human/JSON output, and delegates to Core.
- MCP tools expose structured Agent/LLM operations and delegate to Core.
- Core owns Notion object semantics, validation, retry behavior, error wrapping, and service boundaries.
- SDK client initialization receives `Notion-Version` from configuration only.
- No Core, CLI, route, or MCP module hardcodes `Notion-Version`.

## Configuration Model

Global configuration remains under the user home directory:

```text
~/.notion_mcp/config.json
```

It stores authentication and runtime settings:

- `notion_token`
- `user_id`
- `notion_version`
- `timeout_ms`
- `retry`

Project configuration is stored in the project tree:

```text
.notion_mcp/config.json
```

It stores project-local runtime settings only:

- `schema_version`
- `project_name`
- `workspace_hint`
- timestamps
- settings such as `prefer_attached_page`, `prefer_attached_database`, and `json_output_default`

Project configuration must never store:

- Notion token.
- OAuth refresh token.
- private key.
- long-lived credential.

## Project Runtime Directory

The implementation must create and maintain:

```text
.notion_mcp/
  config.json
  state/
    page.attach.json
    database.attach.json
  cache/
  logs/
  .gitignore
```

Default `.notion_mcp/.gitignore` content:

```text
state/
cache/
logs/
```

Rationale:

- Attach state can reveal page/database ids and titles.
- State/cache/logs are local runtime files by default.
- Teams can opt into sharing project state by editing `.notion_mcp/.gitignore`.

## Project Discovery

Commands that need project context resolve the project root as follows:

1. Start at `cwd`.
2. Check for `.notion_mcp/config.json`.
3. Walk upward to parent directories.
4. Stop at the first matching config.
5. If no config is found:
   - `project init`, `local init`, `page attach`, and `database attach` may initialize context.
   - context-dependent commands must return a clear error.

Future explicit override:

```bash
notion-mcp --project /path/to/project ...
```

The first implementation may defer `--project`, but Core design should not block it.

## Core Modules

Recommended additions:

```text
src/notion_mcp/core/project/
  project_config.py
  project_paths.py
  project_resolver.py

src/notion_mcp/core/attachments/
  attachment_store.py
  context_resolver.py
  page_attachment.py
  database_attachment.py

src/notion_mcp/core/notion/
  pages.py
  blocks.py
  databases.py
  data_sources.py
```

If the repository already has equivalent service modules, use existing patterns and place these responsibilities there instead of creating duplicate abstractions.

## Project Services

`ProjectResolver` responsibilities:

- `find_project_root(cwd)`
- `find_project_config(cwd)`
- `ensure_project(cwd)`
- `init_project(cwd, force=False, private=False)`

`ProjectConfigStore` responsibilities:

- Load project config.
- Validate schema version.
- Write config with stable JSON formatting.
- Update `updated_at`.
- Enforce no-token rule.

`ProjectPaths` responsibilities:

- Derive `.notion_mcp` file paths from project root.
- Avoid path string duplication in CLI and Core.

## Attachment Services

`AttachmentStore` responsibilities:

- `load_page_attachment(project_root)`
- `save_page_attachment(project_root, attachment)`
- `delete_page_attachment(project_root)`
- `load_database_attachment(project_root)`
- `save_database_attachment(project_root, attachment)`
- `delete_database_attachment(project_root)`

`ContextResolver` responsibilities:

- `resolve_page_id(explicit_page_id=None)`
- `resolve_database_id(explicit_database_id=None)`
- `resolve_data_source_id(explicit_data_source_id=None)`

Resolution order:

```text
explicit id > attachment > error
```

## Atomic File Writes

All `.notion_mcp` JSON writes must be atomic:

1. Write to a temporary file in the same directory.
2. Flush and fsync.
3. Rename to the final path.

JSON requirements:

- UTF-8.
- 2-space indentation.
- Stable field order.
- Trailing newline.

Permissions:

- Global config: `0600`.
- Project config/state: `0644`.
- `project init --private`: project files may use `0600`.

## Page Attachment

State file:

```text
.notion_mcp/state/page.attach.json
```

Standard commands:

```bash
notion-mcp page attach <page_id>
notion-mcp page status
notion-mcp page current
notion-mcp page refresh
notion-mcp page detach
notion-mcp page deattach
```

Attach behavior:

1. Find existing project root from `cwd`.
2. If missing, initialize `.notion_mcp` in `cwd` unless `--require-project` is set.
3. With `--verify` or default verify, retrieve the page from Notion and store title, URL, parent, archived, and in-trash status.
4. With `--no-verify`, require or accept a manual title and store limited state.
5. Write state atomically.

Detach behavior:

- Remove `page.attach.json` by default.
- Do not modify, trash, delete, or alter the Notion page.
- `deattach` is a compatibility alias.

Page command defaulting:

```text
explicit page_id > attached page id > error
```

Commands that may omit page id after attach:

```bash
notion-mcp page content
notion-mcp page blocks
notion-mcp page tree
notion-mcp page insert page --payload '<json>'
notion-mcp page insert database --payload '<json>'
```

Page block editing commands still require `block_id`:

```bash
notion-mcp page block update <block_id> --payload '<json>'
notion-mcp page block append <block_id> --payload '<json>'
notion-mcp page block insert-after <block_id> --payload '<json>'
notion-mcp page block remove <block_id>
```

Attached page context can be used for output context and optional safety checks. Expensive recursive block ownership checks should be opt-in through `--strict-page-check`.

## Page Content

Required commands:

```bash
notion-mcp page content
notion-mcp page content <page_id>
notion-mcp page content --json
notion-mcp page content --tree
```

Human output must include:

- page title.
- page id.
- page properties summary.
- block list with index, type, block id, and text summary.

JSON output must include:

- `page.id`.
- `page.properties`.
- `blocks[*].id`.
- `blocks[*].type`.
- `blocks[*].text`.
- `blocks[*].parent_id`.
- `blocks[*].has_children`.
- `blocks[*].children`.

## Block CLI

Block CLI remains the advanced/lower-level entrypoint:

```bash
notion-mcp block retrieve <block_id>
notion-mcp block children <block_id>
notion-mcp block children <block_id> --recursive
notion-mcp block append <block_id> --payload '<json>'
notion-mcp block update <block_id> --payload '<json>'
notion-mcp block trash <block_id>
```

User-facing docs should show page editing through `page block ...` first and place Block CLI in advanced usage.

## Database and DataSource Separation

Core must model both objects:

- `database`: container object.
- `data_source`: table-level object under a database.

Boundaries:

- DatabaseService: create/update/retrieve database containers and list child data sources.
- DataSourceService: retrieve/query/update data source schema, templates, and table entries/pages.
- PageService: ordinary pages and data source entry pages.
- BlockService: page content nodes.
- RawApiService: escape hatch for unsupported operations.

Forbidden modeling:

- Treating `data_source` as a database alias.
- Assuming `database_id == data_source_id`.
- Putting database container, data source schema, query, and database pages into one mixed service.

## Database Attachment

State file:

```text
.notion_mcp/state/database.attach.json
```

Standard commands:

```bash
notion-mcp database attach <database_id>
notion-mcp database attach <database_id> --data-source <data_source_id_or_name>
notion-mcp database status
notion-mcp database current
notion-mcp database refresh
notion-mcp database detach
notion-mcp database deattach
```

Attach behavior:

1. Find or initialize project context.
2. Retrieve database when verification is enabled.
3. Store database id, title, URL, inline/archive/trash status.
4. List child data sources.
5. If one data source exists, set it as `active_data_source`.
6. If multiple data sources exist and no `--data-source` is provided, fail and list choices.
7. If `--data-source` is provided, match by id or name.
8. Write `database.attach.json` atomically.

No-verify behavior:

- Store database id and manual title only.
- `active_data_source` is `null`.
- Any table-level operation must fail until active data source is resolved.

Database command defaulting:

For container-level operations:

```text
explicit database_id > attached database.database.id > error
```

For table-level operations:

```text
explicit data_source_id > attached database.active_data_source.id > error
```

Commands that can use attached state:

```bash
notion-mcp database retrieve
notion-mcp database sources
notion-mcp database query --payload '<json>'
notion-mcp database page create --properties '<json>'
notion-mcp database property rename <property_id_or_name> <new_name>
```

## Database and DataSource CLI

Container-level database commands:

```bash
notion-mcp database retrieve <database_id>
notion-mcp database sources <database_id>
notion-mcp database create --payload '<json>'
notion-mcp database update <database_id> --payload '<json>'
notion-mcp database rename <database_id> <new_name>
```

Explicit table-level data source commands:

```bash
notion-mcp data-source retrieve <data_source_id>
notion-mcp data-source query <data_source_id> --payload '<json>'
notion-mcp data-source create <database_id> --payload '<json>'
notion-mcp data-source update <data_source_id> --payload '<json>'
notion-mcp data-source templates <data_source_id>
notion-mcp data-source property rename <data_source_id> <property_id_or_name> <new_name>
```

Human-friendly shortcuts:

```bash
notion-mcp database page create <database_id_or_data_source_id> --properties '<json>'
notion-mcp database page update <page_id> --properties '<json>'
notion-mcp database query <database_id_or_data_source_id> --payload '<json>'
```

Shortcut resolution:

- If input is a data source id, call `DataSourceService`.
- If input is a database id, retrieve database and inspect data sources.
- If one data source exists, use it.
- If multiple data sources exist, require `--data-source`.

## Insert Positioning

Stable first implementation:

```bash
notion-mcp page block insert-after <block_id> --payload '<json>'
```

Do not include `insert-before` in the first stable batch.

If implemented later, `insert-before` must be explicit best-effort and fail when exact placement is unsupported by the configured `Notion-Version`.

## MCP Tools

MCP tools must share Core services with CLI.

Planned tool groups:

```text
page.retrieve
page.create
page.update
page.trash
page.property.retrieve
block.children
block.append
block.update
block.trash
database.retrieve
database.create
database.update
database.sources
data_source.retrieve
data_source.query
data_source.create
data_source.update
data_source.templates
raw.invoke
```

MCP tool design priorities:

- structured parameters.
- stable JSON results.
- explicit error objects.
- no CLI string invocation.
- no direct SDK calls outside Core.

## Raw API

Raw API remains available:

```bash
notion-mcp raw-api invoke --method GET --path /v1/...
notion-mcp raw-api invoke --method POST --path /v1/... --payload '<json>'
```

It is for:

- uncommon API operations not yet wrapped.
- new API experiments.
- debugging.
- advanced developer workflows.

It is not the normal path for page/database editing after v2/v3 commands land.

## Testing Design

Testing rules:

- Add tests before implementation.
- Do not modify already-created tests just to make them pass.
- If coverage is insufficient, add new v2/v3 tests.
- Real Notion tests are marked integration and skipped by default.

ADR-002 test families:

```text
tests/v2/cli/
tests/v2/core/
tests/v2/scenarios/
tests/v2/mcp_tools/
```

ADR-003 attach workflow test families:

```text
tests/v3/core/
tests/v3/cli/
tests/v3/scenarios/
```

Integration tests:

```python
@pytest.mark.integration
@pytest.mark.skipif(not REAL_NOTION_TOKEN, reason="requires real Notion workspace")
```

## Documentation Synchronization

After implementation, synchronize:

- `Docs/User/Configuration.md`
- `Docs/User/Cli.md`
- `Docs/Developer/api/cli.md`
- `Docs/Developer/mcp_tools/databases.md`
- `Docs/Developer/mcp_tools/data_sources.md`
- `Docs/Developer/testing/cli.md`
- `Docs/dev/Feature_Completion_Plan.md`
- `Docs/dev/progress.md`
- `Docs/Requirements.md`

Docs must distinguish:

- accepted design.
- implemented commands.
- planned commands.
- compatibility aliases.
- advanced raw API fallback.

## Minimum Delivery Loop

The first end-to-end delivery target is:

```bash
cd my-project
notion-mcp page attach <page_id>
notion-mcp page status
notion-mcp page content
notion-mcp page detach
notion-mcp database attach <database_id> --data-source <data_source_id_or_name>
notion-mcp database status
notion-mcp database query --payload '<json>'
notion-mcp database detach
```

It must also work from a child directory:

```bash
cd my-project/sub/dir
notion-mcp page content
```

Expected behavior:

```text
my-project/.notion_mcp/config.json
```

is discovered automatically.
