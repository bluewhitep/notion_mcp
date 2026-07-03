# CLI API

この文書は、現在の public `nilo` CLI surface、hidden compatibility entries、Core call boundaries を記録します。CLI は terminal user experience を担当し、business behavior は Core services から取得します。

## Entrypoint

- Package: `nilo.cli`
- Console script: `nilo = nilo.cli:app`
- Root app: `src/nilo/cli/app.py`
- Help options: `--help` and `-h`

## Core boundary

```text
CLI -> Core -> Notion SDK/API
MCP Tool -> Core -> Notion SDK/API
```

CLI は Notion SDK を直接呼びません。新しい command を追加する場合は、まず対応する Core service capability を確認します。Core にない capability は、CLI wiring の前に Core に追加します。

## Public root commands

- `nilo init`: project-local `.notion_mcp/` context を初期化します。token は保存せず、user ID も要求しません。
- `nilo pwd`: 現在の directory から上位へ探索して project root を解決します。
- `nilo version`: package version と configured Notion API version を表示します。
- `nilo config --global --show`: redacted global configuration summary を表示します。
- `nilo config --global user.token <token>`: global token を更新します。
- `nilo config --global user.name <name>`: global display name を更新します。
- `nilo config --local --show`: current project-local configuration summary を表示します。

`project`、`local`、root `status`、`config global/local`、`config set/get/unset/list` は hidden compatibility entries です。public command surface ではありません。

## Project context

Core が project context を提供します。

```text
ProjectResolver
ProjectConfigStore
AttachmentStore
ContextResolver
```

Resolution order:

```text
explicit id > attached state > error
```

Project-local configuration:

```text
.notion_mcp/config.json
```

Attachment state:

```text
.notion_mcp/state/page.attach.json
.notion_mcp/state/database.attach.json
```

Project-local configuration と attachment state は token を保存してはいけません。

## Page CLI

Page ID inputs は `src/nilo/core/identifiers.py` で normalize されます。Public `<page_id>` arguments は raw IDs、Notion URLs、Notion URL を含む Markdown links を受け取れます。

Public commands:

- `nilo page attach <page_id>`: current project の default page を bind します。file attachment ではありません。
- `nilo page status`: attached page を表示します。
- `nilo page refresh`: remote page を変更せず、local title、URL、status を refresh します。
- `nilo page detach`: remote page を変更せず、local page attachment state を削除します。
- `nilo page retrieve [page_id]`: page metadata を読み取ります。ID がない場合は attached page を使います。
- `nilo page blocks [page_id]`: block summary を読み取ります。ID がない場合は attached page を使います。
- `nilo page create`: page を作成します。payload に parent がなく attached page がある場合、attached page を parent に使います。
- `nilo page create --parent-page <page_id>`: 指定 parent の下に child page を作成します。
- `nilo page update <page_id>`: normal page または data source entry page properties を更新します。
- `nilo page trash <page_id>`: page を trash に移動します。

Hidden compatibility entries は旧 aliases 用に残しますが、public user commands として文書化しません。

## Block CLI

Public commands:

- `nilo block children <block_id>`
- `nilo block append <block_id>`
- `nilo block insert-after <block_id>`
- `nilo block update <block_id>`
- `nilo block trash <block_id>`

`insert-before` は stable public command ではありません。`block remove` は trash behavior の hidden compatibility alias です。

## Database and DataSource

Semantic model:

```text
database = container
data_source = table under database
page = page or data source entry
block = page content node
```

Container-level operations には `database` を使います。Table-level schema、query、templates、entry creation には `data-source` を使います。Database shortcuts は attached database の active data source に対してのみ使います。

### Database container commands

- `nilo database attach <database_id>`
- `nilo database attach <database_id> --data-source <id_or_name>`
- `nilo database status`
- `nilo database refresh`
- `nilo database detach`
- `nilo database retrieve [database_id]`
- `nilo database sources [database_id]`
- `nilo database create`
- `nilo database create --parent-page <page_id>`
- `nilo database update <database_id>`
- `nilo database rename <database_id> <new_name>`

`database create` は database container と initial data source を作成します。`database update` は container-level fields だけを更新し、data source schema は変更しません。

### Database shortcut commands

Attached database の active data source にだけ作用します。

- `nilo database query --payload <json>`
- `nilo database page create --properties <json>`
- `nilo database property rename <property> <new_name>`

Explicit data source operations は `data-source` を使います。Page property updates は `page update` を使います。

### DataSource commands

- `nilo data-source retrieve <data_source_id>`
- `nilo data-source query <data_source_id>`
- `nilo data-source create`
- `nilo data-source create <database_id>`
- `nilo data-source update <data_source_id>`
- `nilo data-source templates <data_source_id>`
- `nilo data-source property rename <data_source_id> <property> <new_name>`
- `nilo data-source page create <data_source_id>`

## Other object domains

- `nilo auth validate`
- `nilo auth whoami`
- `nilo user me/list/retrieve`
- `nilo comment list/create/reply`
- `nilo view retrieve/list/query/create/update`
- `nilo file-upload retrieve/list/create/send/complete`
- `nilo search query`
- `nilo custom-emoji list/retrieve`
- `nilo raw-api operations`
- `nilo raw-api invoke <operation>`
- `nilo server run`
- `nilo server status`
- `nilo server stop`
- `nilo server logs`
- `nilo server remove`
- `nilo server stdio`

Raw API は advanced fallback entrypoint であり、通常の page/database editing path ではありません。

## Removed legacy entrypoints

次の old root commands は public CLI entries ではありません。

- `nilo set-token`
- `nilo set-user`
- `nilo show`
- `nilo run`
- `nilo mcp serve`

Configuration には `nilo config --global ...` を使い、MCP server lifecycle には `nilo server ...` を使います。
