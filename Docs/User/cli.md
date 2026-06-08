# CLI 使用说明

本文面向使用者，说明如何使用 `notion-mcp` 命令行工具。

## 初始化

```bash
notion-mcp init \
  --token ntn_xxx \
  --user-name "Ada" \
  --user-id 01234567-89ab-cdef-0123-456789abcdef
```

查看状态：

```bash
notion-mcp status
notion-mcp status --json
```

## 配置

```bash
notion-mcp config list
notion-mcp config get user_name
notion-mcp config set user_name "Ada Lovelace"
notion-mcp config unset user_name
```

token 默认不会明文显示。

## 页面

```bash
notion-mcp page retrieve <page_id> --json
notion-mcp page create --payload '{"parent": {"page_id": "<parent_id>"}}' --dry-run --json
```

## 区块

```bash
notion-mcp block children <block_id> --json
notion-mcp block append <block_id> --payload '{"children": []}' --dry-run --json
```

## 数据库

```bash
notion-mcp database retrieve <database_id> --json
notion-mcp database query <database_id> --payload '{"page_size": 10}' --json
```

## 数据源

```bash
notion-mcp data-source retrieve <data_source_id> --json
notion-mcp data-source query <data_source_id> --payload '{"page_size": 10}' --json
```

## 用户

```bash
notion-mcp user me --json
notion-mcp user list --page-size 10 --json
notion-mcp user retrieve <user_id> --json
```

## 评论

```bash
notion-mcp comment list --block-id <block_id> --json
notion-mcp comment create --payload '{"parent": {"page_id": "<page_id>"}, "rich_text": []}' --dry-run --json
```

## 视图

```bash
notion-mcp view retrieve <view_id> --json
notion-mcp view query <view_id> --payload '{"page_size": 10}' --json
```

## 文件上传

```bash
notion-mcp file-upload retrieve <file_upload_id> --json
notion-mcp file-upload create --payload '{"mode": "single_part"}' --dry-run --json
```

## 搜索和自定义表情

```bash
notion-mcp search query --payload '{"query": "Roadmap"}' --json
notion-mcp custom-emoji list --json
```

## 受控 Raw API

```bash
notion-mcp raw-api operations --json
notion-mcp raw-api invoke pages.retrieve --arguments '{"page_id": "<page_id>"}' --json
```

## MCP

```bash
notion-mcp mcp serve --help
notion-mcp mcp serve --transport stdio
```

`mcp serve` 会启动本地 MCP server，供支持 MCP 的客户端通过 stdio 调用。
