# 設定

この文書では、Notion internal connection の準備、グローバル token の保存、プロジェクトローカル `.notion_mcp/` context の作成方法を説明します。

## Notion access を準備する

`nilo` を設定する前に、Notion internal connection を作成し、操作したい page または database にアクセス権を付与します。

1. Notion internal connection を作成します。
   - Notion Developer portal を開きます。
   - Build / Internal connections で新しい connection を作成します。
   - `Connection name` には `nilo-local` など分かりやすい名前を設定します。
   - `Authentication method` は `Access token` を選択します。現在の N.I.L.O. ユーザーフローでは OAuth は使いません。
   - workspace を選択します。
   - connection 設定ページから installation access token をコピーします。
   - token は通常 `ntn_` または `secret_` で始まります。

2. connection capabilities を設定します。
   - Content capabilities:
     - `Read content`: page、block、database、data source の読み取りに必要です。
     - `Update content`: page properties、block 更新、page/block trash に必要です。
     - `Insert content`: page、database entry、child page、child database、block 追加に必要です。
   - Comment capabilities:
     - `Read comments`: comments の一覧取得に必要です。
     - `Insert comments`: comment 作成や reply に必要です。
   - User capabilities:
     - 通常は `Read user information without email addresses` で十分です。
     - email が本当に必要な場合だけ email access を有効化してください。

3. connection を対象 content に共有します。
   - Developer portal の Content access ページで許可する pages/databases を選択します。
   - または Notion page の `...` メニューから Connections / Add connection を選び、作成した connection を追加します。
   - parent page を共有すると、その child pages にもアクセスできることが多いです。
   - API が 403 や not found を返す場合は、まず対象 page/database が connection に共有されているか確認します。

4. page ID を取得します。
   - Notion で対象 page を開きます。
   - Share / Copy link を使います。
   - 32 文字 UUID、またはハイフン付き UUID が page ID です。
   - CLI は Notion URL や Markdown link も直接解析できます。

```bash
nilo page attach "https://www.notion.so/Example-3799a1afb97a80489bb0e7384f334958?source=copy_link"
nilo page retrieve "[Example](https://www.notion.so/Example-3799a1afb97a80489bb0e7384f334958?source=copy_link)"
```

5. database ID を取得します。
   - database を full page として開きます。
   - Share / Copy link を使います。
   - workspace path の後、`?v=` などの query parameter の前にある UUID が database ID です。
   - linked database は元の database ではありません。元の database を connection に共有してください。

6. data source ID を取得します。
   - 現在の Notion API では、database は container、data source はその container 内の具体的な table です。
   - token 設定と database 共有が終わったら、次を実行します。

```bash
nilo database sources <database_id>
```

   - database に data source が 1 つだけなら、`database attach` は自動選択できます。
   - 複数ある場合は `--data-source <data_source_id_or_name>` を指定します。

7. token identity を確認します。
   - 通常の利用では `user_id` を設定する必要はありません。
   - グローバル token を保存し、identity を確認します。

```bash
nilo config --global user.token ntn_xxx
nilo auth whoami --json
```

   - internal connection は通常 bot user として識別されます。
   - `nilo auth validate` は token が使えるか確認します。

## グローバル設定

グローバル設定は、Notion token、表示名、Notion API version、timeout、retry などのユーザー単位の runtime 設定を保存します。

デフォルトパス:

```text
~/.notion_mcp/config.json
```

別ファイルを使う場合:

```bash
NOTION_MCP_CONFIG=/path/to/config.json nilo config --global --show
```

よく使うコマンド:

```bash
nilo config --global user.token ntn_xxx
nilo config --global user.name "Ada"
nilo config --global --show
nilo config --global --show --json
```

`nilo config --global --show` は token の有無を表示しますが、生の token は表示しません。

## プロジェクトローカル設定

プロジェクトローカル設定は、Git のように現在の directory から上位へ context を探索します。プロジェクト内で作業するとき、page ID、database ID、data source ID を毎回指定しなくて済みます。

保存場所:

```text
.notion_mcp/config.json
```

ここには token は保存されません。token はグローバル設定に保存されます。

初期化:

```bash
nilo init --project-name "Demo"
nilo init --workspace-hint "Team Workspace" --json
```

確認:

```bash
nilo config --local --show
nilo config --local --show --json
nilo pwd
```

設定例:

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

## Page attachment

`page attach` は現在のプロジェクトの default page を binding します。ファイル添付ではありません。

```bash
nilo page attach <page_id>
nilo page status
nilo page retrieve
nilo page blocks
```

解除:

```bash
nilo page detach
```

ローカル状態の更新:

```bash
nilo page refresh
```

`page refresh` は Notion から title、URL、status を取得してローカル状態だけを更新します。リモート page は変更しません。

## Database attachment

database は container、data source はその中の table です。database attachment は bound database と active data source を保存します。

```bash
nilo database attach <database_id>
nilo database attach <database_id> --data-source <data_source_id_or_name>
nilo database status
nilo database query --payload '{"page_size": 10}'
```

解除:

```bash
nilo database detach
```

ローカル状態の更新:

```bash
nilo database refresh
```

`database refresh` は Notion から database title、URL、data sources、status を取得してローカル状態だけを更新します。リモート database は変更しません。

## よく使う workflow

グローバル token を設定して現在の repository を初期化します。

```bash
nilo config --global user.token ntn_xxx
nilo config --global user.name "Ada"
nilo config --global --show
nilo init --project-name "Demo"
nilo config --local --show
```

page を attach して読む:

```bash
nilo page attach <page_id>
nilo page retrieve
nilo page blocks --tree
```

database を attach して active data source を query する:

```bash
nilo database attach <database_id> --data-source Tasks
nilo database sources
nilo database query --payload '{"page_size": 10}'
```

data source を明示的に操作する:

```bash
nilo data-source query <data_source_id> --payload '{"page_size": 10}'
nilo data-source property rename <data_source_id> Status State
```
