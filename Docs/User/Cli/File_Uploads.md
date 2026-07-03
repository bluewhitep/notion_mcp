# File Uploads CLI

本文说明 file upload 相关命令。

## 命令

| 命令 | 作用 |
| --- | --- |
| `nilo file-upload retrieve <file_upload_id>` | 读取 file upload 状态。 |
| `nilo file-upload list` | 列出 file uploads。 |
| `nilo file-upload create` | 创建 file upload。 |
| `nilo file-upload send <file_upload_id>` | 发送文件内容。 |
| `nilo file-upload complete <file_upload_id>` | 完成 file upload。 |

## 示例

```bash
nilo file-upload list --json
nilo file-upload retrieve <file_upload_id> --json
nilo file-upload create --payload '{}'
nilo file-upload send <file_upload_id> --path ./example.pdf
nilo file-upload complete <file_upload_id>
```
