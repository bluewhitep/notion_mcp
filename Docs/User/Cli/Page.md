# Page CLI

本文说明 page 相关命令。

`page attach` 的含义是“绑定当前项目默认 page”，不是上传文件附件。以后如果要处理文件附件，应使用单独的文件命令。

所有公开 `<page_id>` 输入都可以直接传 Notion page id、Notion 分享 URL，或包含 Notion URL 的 Markdown 链接。CLI 会从 URL 中提取 32 位 page id，并规范成带连字符的 UUID。

## 命令

| 命令 | 作用 |
| --- | --- |
| `notion-mcp page attach <page_id>` | 把一个 Notion page 绑定为当前项目的默认 page。 |
| `notion-mcp page status` | 查看当前项目绑定的 page。 |
| `notion-mcp page refresh` | 重新从 Notion 拉取已绑定 page 的标题、URL 和状态，只刷新本地状态，不修改 Notion 远端 page。 |
| `notion-mcp page detach` | 取消本地 page 绑定，不修改 Notion 远端 page。 |
| `notion-mcp page retrieve` | 读取当前绑定 page 的页面元信息，例如属性、标题、URL 和状态。 |
| `notion-mcp page retrieve <page_id>` | 读取指定 page 的页面元信息，显式 id 覆盖当前绑定 page。 |
| `notion-mcp page blocks` | 读取当前绑定 page 下的内容块摘要。 |
| `notion-mcp page blocks <page_id>` | 读取指定 page 下的内容块摘要。 |
| `notion-mcp page create` | 创建 child page；如果当前项目已绑定 page，默认创建到该 page 下。 |
| `notion-mcp page create --parent-page <page_id>` | 在指定 parent page 下创建 child page。 |
| `notion-mcp page update <page_id>` | 更新普通 page 或 data source entry page 的 properties。 |
| `notion-mcp page trash <page_id>` | 将 page 移入 trash。 |

## 示例

```bash
notion-mcp page attach <page_id>
notion-mcp page attach "https://www.notion.so/Notion-MCP-3799a1afb97a80489bb0e7384f334958?source=copy_link"
notion-mcp page status
notion-mcp page retrieve --json
notion-mcp page retrieve "https://www.notion.so/Notion-MCP-3799a1afb97a80489bb0e7384f334958?source=copy_link" --json
notion-mcp page blocks --tree
notion-mcp page create --payload '{"properties": {"title": [{"text": {"content": "Child"}}]}}'
notion-mcp page update <page_id> --payload '{"properties": {}}'
```

页面内编辑仍然必须传具体 `block_id`。绑定 page 只能确定页面范围，不能确定编辑位置。
