# File Uploads CLI

File upload commands は Notion file upload lifecycle を管理します。

## コマンド

| Command | Purpose |
| --- | --- |
| `nilo file-upload retrieve <file_upload_id>` | file upload status を読み取ります。 |
| `nilo file-upload list` | file uploads を一覧します。 |
| `nilo file-upload create` | file upload を作成します。 |
| `nilo file-upload send <file_upload_id>` | file contents を送信します。 |
| `nilo file-upload complete <file_upload_id>` | file upload を完了します。 |

## 例

```bash
nilo file-upload list --json
nilo file-upload retrieve <file_upload_id> --json
nilo file-upload create --payload '{}'
nilo file-upload send <file_upload_id> --path ./example.pdf
nilo file-upload complete <file_upload_id>
```
