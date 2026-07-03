# Database DataSource CLI

このページでは database container commands、data source commands、database shortcuts を説明します。

現在の Notion API model では、database は container、data source はその中の具体的な table です。

- Container-level operation には `database` を使います。
- 明示的な data source 操作には `data-source` を使います。
- Database shortcuts は、現在の project に attached database の active data source を対象にするときだけ使います。

## Database container commands

| Command | Purpose |
| --- | --- |
| `nilo database attach <database_id>` | 現在の project の default database を attach します。data source が 1 つなら自動選択できます。 |
| `nilo database attach <database_id> --data-source <id_or_name>` | database を attach し、active data source を明示的に選択します。 |
| `nilo database status` | attached database と active data source を表示します。 |
| `nilo database refresh` | remote database を変更せず、ローカル title、URL、data source list、status を更新します。 |
| `nilo database detach` | remote database を変更せず、ローカル database binding を削除します。 |
| `nilo database retrieve` | attached database container を読み取ります。 |
| `nilo database retrieve <database_id>` | 指定 database container を読み取ります。 |
| `nilo database sources` | attached database 配下の data sources を一覧します。 |
| `nilo database sources <database_id>` | 指定 database 配下の data sources を一覧します。 |
| `nilo database create` | database container と initial data source を作成します。 |
| `nilo database create --parent-page <page_id>` | 指定 parent page 配下に database container を作成します。 |
| `nilo database update <database_id>` | title、description、icon、cover など container-level fields を更新します。 |
| `nilo database rename <database_id> <new_name>` | database container を rename します。 |

例:

```bash
nilo database attach <database_id> --data-source Tasks
nilo database status
nilo database sources
nilo database create --parent-page <page_id> --payload '{"title": []}'
nilo database update <database_id> --payload '{"title": []}'
```

## Database shortcuts

これらの command は attached database の active data source に作用します。

| Command | Purpose |
| --- | --- |
| `nilo database query --payload '<json>'` | active data source を query します。 |
| `nilo database page create` | active data source に page/entry を作成します。 |
| `nilo database property rename <property> <new_name>` | active data source の property を rename します。 |

例:

```bash
nilo database query --payload '{"page_size": 10}'
nilo database page create --properties '{"Name": {"title": []}}'
nilo database property rename Status State
```

## DataSource commands

| Command | Purpose |
| --- | --- |
| `nilo data-source retrieve <data_source_id>` | table-level data source information と schema を読み取ります。 |
| `nilo data-source query <data_source_id>` | 指定 data source の entries/pages を query します。 |
| `nilo data-source create` | attached database 配下に data source を作成します。 |
| `nilo data-source create <database_id>` | 指定 database container 配下に data source を作成します。 |
| `nilo data-source update <data_source_id>` | table-level properties または schema を更新します。 |
| `nilo data-source templates <data_source_id>` | data source で利用可能な page templates を一覧します。 |
| `nilo data-source property rename <data_source_id> <property> <new_name>` | 指定 data source の property を rename します。 |
| `nilo data-source page create <data_source_id>` | 指定 data source に page/entry を作成します。 |

例:

```bash
nilo data-source query <data_source_id> --payload '{"page_size": 10}'
nilo data-source create <database_id> --payload '{"name": "Tasks", "properties": {}}'
nilo data-source property rename <data_source_id> Status State
nilo data-source page create <data_source_id> --properties '{"Name": {"title": []}}'
```
