# V2/V3 Trackable Tasks: Local Context, Attach Runtime, and CLI Expansion

Status: Active planning list / Pending implementation.

This file turns `Docs/dev/ADR-002-local-context-and-cli-v2.md`, `Docs/dev/ADR-003-project-attach-context.md`, and `Docs/dev/ADR-004-cli-command-surface-consolidation.md` into a task list that can be tracked during implementation.

Status legend:

- `[ ]`: not started.
- `[~]`: in progress.
- `[x]`: complete.
- `[>]`: deferred.
- `[!]`: blocked.

Implementation rule:

- Add tests before source implementation.
- Do not change already-created tests only to make them pass.
- Record every completed phase and verification command in `Docs/dev/progress.md`.

## Phase D0: Design Consolidation

- `[x] V2V3-D0-005` Create ADR-004 for the revised public CLI command surface.
  - Output: `Docs/dev/ADR-004-cli-command-surface-consolidation.md`.
  - Acceptance: ADR states `init`, `pwd`, `version`, `config --global`, `config --local`, `page retrieve`, `page blocks`, top-level block editing, and data-source namespace rules.

- `[x] V2V3-D0-006` Update user/developer docs to remove old public command names.
  - Depends on: `V2V3-D0-005`.
  - Acceptance: User docs do not present `project`, `local`, root `status`, `page current`, `page deattach`, `page content`, `page block *`, `page insert *`, `database current`, `database deattach`, or explicit data source operations under `database` as public commands.

- `[x] V2V3-D0-007` Add public command surface regression tests.
  - Output: `tests/v3/cli/test_public_command_surface_revision.py`.
  - Acceptance: tests assert public help exposes new commands and hides old aliases.

- `[x] V2V3-D0-001` Create ADR-002 for local context, Page CLI, Database/DataSource separation, Raw API positioning, and MCP/CLI/Core separation.
  - Source: `Docs/dev/ADR-002-local-context-and-cli-v2.md`.
  - Acceptance: ADR states Accepted / pending implementation and does not claim planned commands are already shipped.

- `[x] V2V3-D0-002` Create ADR-003 for `.notion_mcp` project config and page/database attach workflow.
  - Source: `Docs/dev/ADR-003-project-attach-context.md`.
  - Acceptance: ADR states Design Accepted / pending implementation and names `.notion_mcp/config.json`.

- `[x] V2V3-D0-003` Mark ADR-003 as the source of truth for project directory naming and attach runtime.
  - Depends on: `V2V3-D0-001`, `V2V3-D0-002`.
  - Acceptance: ADR-002 and developer/user docs say `.notion_mcp` supersedes the earlier `.notion-mcp` design.

- `[x] V2V3-D0-004` Create implementation design and trackable task list.
  - Output: `Docs/dev/V2_V3_Development_Design.md`, `Docs/dev/V2_V3_Trackable_Tasks.md`.
  - Acceptance: Tasks include ids, dependencies, outputs, tests, and acceptance criteria.

## Phase P1: Project Configuration Tests

- `[x] V2V3-P1-001` Add core tests for project root discovery.
  - Output: `tests/v3/core/test_project_resolver.py`.
  - Covers: find from cwd, find from child directory, missing config error, explicit future project root behavior if implemented.
  - Acceptance: tests fail before implementation and describe expected `.notion_mcp/config.json` lookup.

- `[x] V2V3-P1-002` Add CLI tests for `project init`.
  - Output: `tests/v3/cli/test_project_init.py`.
  - Covers: creates `.notion_mcp/config.json`, `state/`, `cache/`, `logs/`, `.gitignore`; duplicate init fails; `--force` overwrites safely.
  - Acceptance: tests validate no token is written to project config.

- `[x] V2V3-P1-003` Add CLI tests for `project status` and `project root`.
  - Output: `tests/v3/cli/test_project_status.py`.
  - Covers: human output, `--json` output if supported, root path from child directory, missing project error.
  - Acceptance: output includes project root and config path.

## Phase P2: Project Configuration Implementation

- `[x] V2V3-P2-001` Implement project path helpers.
  - Source target: `src/notion_mcp/core/project/project_paths.py` or existing equivalent module.
  - Depends on: `V2V3-P1-001`.
  - Acceptance: one module owns `.notion_mcp` path constants and state file paths.

- `[x] V2V3-P2-002` Implement `ProjectResolver`.
  - Source target: `src/notion_mcp/core/project/project_resolver.py`.
  - Depends on: `V2V3-P1-001`, `V2V3-P2-001`.
  - Acceptance: resolves project root from cwd and returns clear errors when missing.

- `[x] V2V3-P2-003` Implement `ProjectConfigStore`.
  - Source target: `src/notion_mcp/core/project/project_config.py`.
  - Depends on: `V2V3-P1-002`, `V2V3-P2-001`.
  - Acceptance: stable JSON format, schema version validation, no-token validation, timestamps.

- `[x] V2V3-P2-004` Implement atomic JSON write utility for project state.
  - Source target: reuse existing file utility if available, otherwise add Core utility.
  - Depends on: `V2V3-P2-003`.
  - Acceptance: writes temp file, fsyncs, renames, and preserves trailing newline.

- `[x] V2V3-P2-005` Implement CLI `project init`, `project status`, and `project root`.
  - Source target: CLI project/local command module.
  - Depends on: `V2V3-P1-002`, `V2V3-P1-003`, `V2V3-P2-002`, `V2V3-P2-003`.
  - Acceptance: tests pass; user output says project `.notion_mcp` does not store tokens.

- `[x] V2V3-P2-006` Add compatibility aliases `local init`, `local status`, and `local root`.
  - Depends on: `V2V3-P2-005`.
  - Acceptance: aliases call the same Core path as `project ...`.

## Phase P3: Page Attachment Tests

- `[x] V2V3-P3-001` Add attachment store tests for page attach state.
  - Output: `tests/v3/core/test_page_attachment_store.py`.
  - Covers: load/save/delete, atomic write behavior, JSON shape, detached state if `--keep-state` is implemented.
  - Acceptance: validates `.notion_mcp/state/page.attach.json` schema.

- `[x] V2V3-P3-002` Add CLI tests for `page attach`.
  - Output: `tests/v3/cli/test_page_attach.py`.
  - Covers: verified attach, `--no-verify --title`, auto-init project context, `--require-project` error.
  - Acceptance: state file contains page id/title and no token.

- `[x] V2V3-P3-003` Add CLI tests for `page status`, `page current`, and `page refresh`.
  - Output: `tests/v3/cli/test_page_status.py`.
  - Covers: human output, `--json`, refresh updates title/url/trash fields.
  - Acceptance: output includes project root and state file path.

- `[x] V2V3-P3-004` Add CLI tests for `page detach` and `page deattach`.
  - Output: `tests/v3/cli/test_page_detach.py`.
  - Covers: default state file removal, alias behavior, no remote Notion mutation.
  - Acceptance: detach only changes local state.

- `[x] V2V3-P3-005` Add tests for page id resolution.
  - Output: `tests/v3/cli/test_page_context_resolution.py`.
  - Covers: explicit page id overrides attachment, attached page used when omitted, missing attachment error.
  - Acceptance: error text suggests `page attach <page_id>` or explicit `page content <page_id>`.

## Phase P4: Page Attachment Implementation

- `[x] V2V3-P4-001` Implement `PageAttachment` model.
  - Source target: `src/notion_mcp/core/attachments/page_attachment.py`.
  - Depends on: `V2V3-P3-001`.
  - Acceptance: model represents verified and no-verify state.

- `[x] V2V3-P4-002` Implement page attachment store operations.
  - Source target: `src/notion_mcp/core/attachments/attachment_store.py`.
  - Depends on: `V2V3-P3-001`, `V2V3-P4-001`, `V2V3-P2-004`.
  - Acceptance: load/save/delete pass core tests.

- `[x] V2V3-P4-003` Implement page context resolution.
  - Source target: `src/notion_mcp/core/attachments/context_resolver.py`.
  - Depends on: `V2V3-P3-005`, `V2V3-P4-002`.
  - Acceptance: explicit id > attachment > error.

- `[x] V2V3-P4-004` Implement CLI `page attach`.
  - Depends on: `V2V3-P3-002`, `V2V3-P4-002`.
  - Acceptance: creates project context if missing unless strict mode is set.

- `[x] V2V3-P4-005` Implement CLI `page status`, `page current`, and `page refresh`.
  - Depends on: `V2V3-P3-003`, `V2V3-P4-002`.
  - Acceptance: human and JSON outputs match tests.

- `[x] V2V3-P4-006` Implement CLI `page detach` and `page deattach`.
  - Depends on: `V2V3-P3-004`, `V2V3-P4-002`.
  - Acceptance: local state removed; no Notion page mutation.

## Phase P5: Page Content and Page Block Tests

- `[x] V2V3-P5-001` Add tests for `page content`.
  - Output: `tests/v2/cli/test_page_content.py` or `tests/v3/cli/test_page_content_attach.py`.
  - Covers: attached page default, explicit id override, human output, JSON output, tree output.
  - Acceptance: block id/type/text/parent-child shape is stable.

- `[x] V2V3-P5-002` Add tests for page-scoped block editing.
  - Output: `tests/v2/cli/test_page_block_edit.py` or `tests/v3/cli/test_page_block_edit_attach.py`.
  - Covers: append, insert-after, update, remove/trash, attached page context output.
  - Acceptance: no stable `insert-before` expectation in first batch.

- `[x] V2V3-P5-003` Add tests for `page insert page` and `page insert database`.
  - Output: `tests/v2/cli/test_page_insert.py`.
  - Covers: attached page parent default and explicit payload handling.
  - Acceptance: page/database creation delegates through Core.

## Phase P6: Page Content and Page Block Implementation

- `[x] V2V3-P6-001` Implement `PageService.content`.
  - Source target: existing `PageService` or `src/notion_mcp/core/notion/pages.py`.
  - Depends on: `V2V3-P5-001`.
  - Acceptance: retrieves page properties and blocks; supports non-recursive and tree modes.

- `[x] V2V3-P6-002` Implement human and JSON renderers for page content.
  - Depends on: `V2V3-P5-001`, `V2V3-P6-001`.
  - Acceptance: stable output for scripts and readable output for users.

- `[x] V2V3-P6-003` Implement `page content` attached defaulting.
  - Depends on: `V2V3-P4-003`, `V2V3-P6-001`.
  - Acceptance: `notion-mcp page content` uses attached page.

- `[x] V2V3-P6-004` Implement page-scoped block append/update/insert-after/remove.
  - Depends on: `V2V3-P5-002`.
  - Acceptance: commands use BlockService through Core and keep `insert-before` deferred.

- `[x] V2V3-P6-005` Implement `page insert page` and `page insert database`.
  - Depends on: `V2V3-P5-003`.
  - Acceptance: attached page is used as parent when explicit parent is omitted.

## Phase P7: Database/DataSource Tests

- `[x] V2V3-P7-001` Add core tests for database/data source service separation.
  - Output: `tests/v2/core/test_database_data_source_services.py`.
  - Covers: database container retrieval/sources and data source table-level query/update/templates.
  - Acceptance: tests fail if `database_id == data_source_id` is assumed.

- `[x] V2V3-P7-002` Add CLI tests for database container commands.
  - Output: `tests/v2/cli/test_database_container.py`.
  - Covers: retrieve, sources, create, update, rename.
  - Acceptance: commands delegate to DatabaseService.

- `[x] V2V3-P7-003` Add CLI tests for explicit `data-source` namespace.
  - Output: `tests/v2/cli/test_data_source_namespace.py`.
  - Covers: retrieve, query, create, update, templates, property rename.
  - Acceptance: commands delegate to DataSourceService.

- `[x] V2V3-P7-004` Add CLI tests for database shortcut resolution.
  - Output: `tests/v2/cli/test_database_shortcuts.py`.
  - Covers: database id with one data source, database id with multiple data sources, explicit `--data-source`.
  - Acceptance: multiple data sources fail clearly unless explicit.
  - Current note: explicit `--data-source`, `database page`, and `database property` shortcut tests exist in `tests/v2/cli/test_database_shortcut_commands.py`; attached database/defaulting coverage exists in `tests/v3/cli/test_database_context_resolution.py`.

## Phase P8: Database/DataSource Implementation

- `[x] V2V3-P8-001` Implement or finalize `DatabaseService`.
  - Source target: existing service or `src/notion_mcp/core/notion/databases.py`.
  - Depends on: `V2V3-P7-001`, `V2V3-P7-002`.
  - Acceptance: database container operations do not include table-level query/schema mutation.
  - Current note: container `retrieve/create/update/list_data_sources/rename` are implemented. Table-level query is not exposed on `DatabasesService`; legacy `database query <database_id>` is routed through Core Raw API compatibility.

- `[x] V2V3-P8-002` Implement or finalize `DataSourceService`.
  - Source target: existing service or `src/notion_mcp/core/notion/data_sources.py`.
  - Depends on: `V2V3-P7-001`, `V2V3-P7-003`.
  - Acceptance: data source query/update/templates/property rename pass tests.

- `[x] V2V3-P8-003` Implement database CLI container commands.
  - Depends on: `V2V3-P7-002`, `V2V3-P8-001`.
  - Acceptance: container commands use DatabaseService only.

- `[x] V2V3-P8-004` Implement explicit `data-source` CLI namespace.
  - Depends on: `V2V3-P7-003`, `V2V3-P8-002`.
  - Acceptance: data-source commands use DataSourceService only.

- `[x] V2V3-P8-005` Implement database shortcut resolver.
  - Depends on: `V2V3-P7-004`, `V2V3-P8-001`, `V2V3-P8-002`.
  - Acceptance: shortcut behavior matches single/multiple data source rules.
  - Current note: `database query --data-source`, `database page create/update`, explicit `database property rename`, and attached active data source defaults are implemented. Legacy `database query <database_id>` remains as a Core Raw API compatibility path.

## Phase P9: Database Attachment Tests

- `[x] V2V3-P9-001` Add attachment store tests for database attach state.
  - Output: `tests/v3/core/test_database_attachment_store.py`.
  - Covers: load/save/delete, active data source, available data sources, no-verify state.
  - Acceptance: validates `.notion_mcp/state/database.attach.json`.

- `[x] V2V3-P9-002` Add CLI tests for `database attach`.
  - Output: `tests/v3/cli/test_database_attach.py`.
  - Covers: verified attach, no-verify attach, single source auto-select, multiple source error, explicit source match by id/name.
  - Acceptance: state stores database and active data source information.

- `[x] V2V3-P9-003` Add CLI tests for `database status`, `current`, and `refresh`.
  - Output: `tests/v3/cli/test_database_status.py`.
  - Covers: human output, JSON output, refresh updates sources and active source validity.
  - Acceptance: output includes project root and state file path.

- `[x] V2V3-P9-004` Add CLI tests for `database detach` and `database deattach`.
  - Output: `tests/v3/cli/test_database_detach.py`.
  - Covers: state removal and no remote mutation.
  - Acceptance: detach only changes local state.

- `[x] V2V3-P9-005` Add tests for attached database defaulting.
  - Output: `tests/v3/cli/test_database_context_resolution.py`.
  - Covers: `database retrieve`, `database sources`, `database query`, `database page create`, and property rename defaulting.
  - Acceptance: explicit id overrides attachment; missing active data source errors clearly.

## Phase P10: Database Attachment Implementation

- `[x] V2V3-P10-001` Implement `DatabaseAttachment` model.
  - Source target: `src/notion_mcp/core/attachments/database_attachment.py`.
  - Depends on: `V2V3-P9-001`.
  - Acceptance: model represents verified, no-verify, active source, and available source states.

- `[x] V2V3-P10-002` Implement database attachment store operations.
  - Source target: `src/notion_mcp/core/attachments/attachment_store.py`.
  - Depends on: `V2V3-P9-001`, `V2V3-P10-001`, `V2V3-P2-004`.
  - Acceptance: load/save/delete pass tests.

- `[x] V2V3-P10-003` Implement data source matching by id or name.
  - Depends on: `V2V3-P9-002`.
  - Acceptance: multiple-source errors list candidates and suggested command.

- `[x] V2V3-P10-004` Implement CLI `database attach`.
  - Depends on: `V2V3-P9-002`, `V2V3-P10-002`, `V2V3-P10-003`.
  - Acceptance: single/multiple/no-verify flows pass tests.

- `[x] V2V3-P10-005` Implement CLI `database status`, `current`, and `refresh`.
  - Depends on: `V2V3-P9-003`, `V2V3-P10-002`.
  - Acceptance: refresh updates database and data source state.

- `[x] V2V3-P10-006` Implement CLI `database detach` and `database deattach`.
  - Depends on: `V2V3-P9-004`, `V2V3-P10-002`.
  - Acceptance: local state removed; no Notion database mutation.

- `[x] V2V3-P10-007` Implement attached database/data source context resolution.
  - Depends on: `V2V3-P9-005`, `V2V3-P10-002`.
  - Acceptance: container-level and table-level defaulting rules pass tests.

## Phase P11: MCP Tool Alignment

- `[x] V2V3-P11-001` Add or update MCP tool tests for database/data source separation.
  - Output: `tests/v2/mcp_tools/test_database_data_source_tools.py`.
  - Covers: database tools call DatabaseService; data_source tools call DataSourceService.
  - Acceptance: no MCP tool calls CLI strings or Notion SDK directly.

- `[x] V2V3-P11-002` Implement or adjust MCP tools for database/data_source.
  - Depends on: `V2V3-P11-001`, `V2V3-P8-001`, `V2V3-P8-002`.
  - Acceptance: tool names include `database.sources` and `data_source.query`.
  - Current note: repository MCP tool naming uses underscores. Implemented tools are `database_sources`, `database_rename`, `data_source_templates`, and `data_source_property_rename`, alongside existing `data_source_query`.

- `[x] V2V3-P11-003` Verify page/block MCP tools still share Core behavior.
  - Depends on: `V2V3-P6-004`.
  - Acceptance: page/block MCP tool behavior stays aligned with CLI/Core behavior.
  - Current note: P11 MCP verification ran `tests/v2/mcp_server`, `tests/v2/mcp_tools`, and existing MCP scenario tests.

## Phase P12: Raw API and Version Policy

- `[x] V2V3-P12-001` Add tests proving Raw API is available but not required for common page/database workflows.
  - Output: `tests/v2/cli/test_raw_api_positioning.py`.
  - Acceptance: docs and command help identify Raw API as advanced fallback.

- `[x] V2V3-P12-002` Add compatibility tests for configured `Notion-Version`.
  - Output: `tests/v2/core/test_notion_version_policy.py`.
  - Covers: version read from global config, default pinned, no scattered hardcoding.
  - Acceptance: implementation can change version through config only.

- `[x] V2V3-P12-003` Re-check official Notion API and SDK docs before implementing version-sensitive endpoints.
  - Depends on: implementation start for block positioning, database/data source, or Notion-Version changes.
  - Acceptance: `Docs/dev/progress.md` records checked official URLs and date.
  - Current note: P12 rechecked official Notion versioning and 2026-03-11 upgrade guide on 2026-06-08.

## Phase P13: Scenario Tests

- `[x] V2V3-P13-001` Add local page context workflow scenario.
  - Output: `tests/v3/scenarios/test_attach_page_workflow.py`.
  - Covers: attach page, status, child directory discovery, content, detach, missing attach error.
  - Acceptance: simulates user workflow without real Notion token.

- `[x] V2V3-P13-002` Add page content edit workflow scenario.
  - Output: `tests/v2/scenarios/test_page_content_edit_workflow.py`.
  - Covers: content read, insert-after, append, update, remove.
  - Acceptance: uses fake Notion client and stable block ids.

- `[x] V2V3-P13-003` Add database attach/query workflow scenario.
  - Output: `tests/v3/scenarios/test_attach_database_workflow.py`.
  - Covers: attach database, active data source, query without id, create page, detach.
  - Acceptance: explicit id overrides attached source.

- `[x] V2V3-P13-004` Add project context discovery scenario.
  - Output: `tests/v3/scenarios/test_project_context_discovery.py`.
  - Covers: commands from nested directories find project root.
  - Acceptance: missing config errors include remediation commands.

## Phase P14: Documentation Sync

- `[x] V2V3-P14-001` Update user configuration docs after project config implementation.
  - Output: `Docs/User/Configuration.md`.
  - Depends on: `V2V3-P2-005`.
  - Acceptance: planned wording is replaced with implemented command status.

- `[x] V2V3-P14-002` Update user CLI docs after page/database attach implementation.
  - Output: `Docs/User/Cli.md`.
  - Depends on: `V2V3-P4-006`, `V2V3-P10-007`.
  - Acceptance: commands are documented as implemented only after tests pass.

- `[x] V2V3-P14-003` Update developer CLI API docs.
  - Output: `Docs/Developer/api/cli.md`.
  - Depends on: implementation phases touched.
  - Acceptance: CLI-to-Core boundaries and command mappings match source.

- `[x] V2V3-P14-004` Update MCP tool docs.
  - Output: `Docs/Developer/mcp_tools/databases.md`, `Docs/Developer/mcp_tools/data_sources.md`.
  - Depends on: `V2V3-P11-002`.
  - Acceptance: database and data_source docs are not synonyms.

- `[x] V2V3-P14-005` Update testing docs.
  - Output: `Docs/Developer/testing/cli.md`.
  - Depends on: new tests created.
  - Acceptance: documents v2/v3 test layout and integration skip rules.

- `[x] V2V3-P14-006` Update progress after each phase.
  - Output: `Docs/dev/progress.md`.
  - Acceptance: each phase records files changed, commands run, verification results, and deferred live tests.

## Phase P15: Minimum Delivery Verification

- `[x] V2V3-P15-001` Verify page attach minimum loop.
  - Command target:
    - `notion-mcp page attach <page_id>`
    - `notion-mcp page status`
    - `notion-mcp page content`
    - `notion-mcp page detach`
  - Acceptance: passes with fake tests; real integration remains skipped unless configured.

- `[x] V2V3-P15-002` Verify database attach minimum loop.
  - Command target:
    - `notion-mcp database attach <database_id> --data-source <data_source_id_or_name>`
    - `notion-mcp database status`
    - `notion-mcp database query --payload '<json>'`
    - `notion-mcp database detach`
  - Acceptance: active data source defaulting works and errors clearly when missing.

- `[x] V2V3-P15-003` Verify child directory discovery.
  - Command target:
    - `cd my-project/sub/dir`
    - `notion-mcp page content`
  - Acceptance: command finds `my-project/.notion_mcp/config.json`.

- `[x] V2V3-P15-004` Run release-relevant local checks.
  - Commands:
    - `uv run pytest -q -p no:cacheprovider`
    - `uv run ruff check .`
    - `uv run mypy src`
    - `uv run --no-project --with . notion-mcp --help`
  - Acceptance: all available checks pass or documented blockers are recorded in `Docs/dev/progress.md`.

## Deferred Items

- `[>] V2V3-DEF-001` Stable `insert-before`.
  - Reason: exact insertion before first sibling depends on Notion positioning support and configured `Notion-Version`.
  - Reopen condition: official docs confirm supported exact placement and compatibility tests are added.

- `[>] V2V3-DEF-002` Full cache/index support under `.notion_mcp/cache/`.
  - Reason: ADR-003 reserves the directory but does not require it for the minimum attach workflow.
  - Reopen condition: page/database tree caching becomes a performance requirement.

- `[>] V2V3-DEF-003` Local logs/audit under `.notion_mcp/logs/`.
  - Reason: reserved for future local runtime observability.
  - Reopen condition: CLI audit or troubleshooting workflow requires persisted project-local logs.

- `[>] V2V3-DEF-004` OAuth.
  - Reason: current project targets local Notion integration token flow.
  - Reopen condition: product requirements include OAuth user authorization.

- `[>] V2V3-DEF-005` GUI.
  - Reason: explicitly outside ADR-003 scope.
  - Reopen condition: separate GUI design is accepted.
