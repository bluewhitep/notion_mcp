# File Uploads CLI

本文说明 file upload 相关命令。

## 命令

| 命令 | 作用 |
| --- | --- |
| `notion-mcp file-upload retrieve <file_upload_id>` | 读取 file upload 状态。 |
| `notion-mcp file-upload list` | 列出 file uploads。 |
| `notion-mcp file-upload create` | 创建 file upload。 |
| `notion-mcp file-upload send <file_upload_id>` | 发送文件内容。 |
| `notion-mcp file-upload complete <file_upload_id>` | 完成 file upload。 |

## 示例

```bash
notion-mcp file-upload list --json
notion-mcp file-upload retrieve <file_upload_id> --json
notion-mcp file-upload create --payload '{}'
notion-mcp file-upload send <file_upload_id> --path ./example.pdf
notion-mcp file-upload complete <file_upload_id>
```
