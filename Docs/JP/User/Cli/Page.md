# Page CLI

Page commands は project default の binding と Notion pages の操作を行います。

`page attach` は「この page を現在の project の default page として bind する」という意味です。file attachment の upload ではありません。

公開 `<page_id>` input には、Notion page ID、Notion share URL、または Notion URL を含む Markdown link を渡せます。CLI は 32 文字 ID を抽出し、ハイフン付き UUID に正規化します。

## コマンド

| Command | Purpose |
| --- | --- |
| `nilo page attach <page_id>` | Notion page を現在の project の default page として bind します。 |
| `nilo page status` | attached page を表示します。 |
| `nilo page refresh` | remote page を変更せず、ローカルの title、URL、status を更新します。 |
| `nilo page detach` | remote page を変更せず、ローカル page binding を削除します。 |
| `nilo page retrieve` | attached page の metadata を読み取ります。 |
| `nilo page retrieve <page_id>` | 指定 page の metadata を読み取ります。 |
| `nilo page blocks` | attached page 配下の content blocks summary を読み取ります。 |
| `nilo page blocks <page_id>` | 指定 page 配下の content blocks summary を読み取ります。 |
| `nilo page create` | child page を作成します。attached page があれば default parent として使います。 |
| `nilo page create --parent-page <page_id>` | 指定 parent page 配下に child page を作成します。 |
| `nilo page update <page_id>` | 通常 page または data source entry page の properties を更新します。 |
| `nilo page trash <page_id>` | page を trash に移動します。 |

## 例

```bash
nilo page attach <page_id>
nilo page attach "https://www.notion.so/Example-3799a1afb97a80489bb0e7384f334958?source=copy_link"
nilo page status
nilo page retrieve --json
nilo page retrieve "https://www.notion.so/Example-3799a1afb97a80489bb0e7384f334958?source=copy_link" --json
nilo page blocks --tree
nilo page create --payload '{"properties": {"title": [{"text": {"content": "Child"}}]}}'
nilo page update <page_id> --payload '{"properties": {}}'
```

page 内の content を編集するには具体的な `block_id` が必要です。page binding は page scope を決めるだけで、編集位置は決めません。
