# Page CLI

Page commands bind project defaults and operate on Notion pages.

`page attach` means "bind this page as the default page for the current project." It does not upload file attachments.

Public `<page_id>` inputs can be a Notion page ID, a Notion share URL, or a Markdown link that contains a Notion URL. The CLI extracts the 32-character ID and normalizes it to a hyphenated UUID.

## Commands

| Command | Purpose |
| --- | --- |
| `nilo page attach <page_id>` | Bind a Notion page as the default page for the current project. |
| `nilo page status` | Show the attached page. |
| `nilo page refresh` | Refresh local title, URL, and status without changing the remote page. |
| `nilo page detach` | Remove the local page binding without changing the remote page. |
| `nilo page retrieve` | Read metadata for the attached page. |
| `nilo page retrieve <page_id>` | Read metadata for a specific page. |
| `nilo page blocks` | Read a summary of content blocks under the attached page. |
| `nilo page blocks <page_id>` | Read a summary of content blocks under a specific page. |
| `nilo page create` | Create a child page. If a page is attached, it is used as the default parent. |
| `nilo page create --parent-page <page_id>` | Create a child page under a specific parent page. |
| `nilo page update <page_id>` | Update properties for a normal page or data source entry page. |
| `nilo page trash <page_id>` | Move a page to trash. |

## Examples

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

Editing content inside a page still requires a concrete `block_id`. A page binding only sets the page scope; it does not identify an edit location.
