# File Uploads CLI

File upload commands manage the Notion file upload lifecycle.

## Commands

| Command | Purpose |
| --- | --- |
| `nilo file-upload retrieve <file_upload_id>` | Read file upload status. |
| `nilo file-upload list` | List file uploads. |
| `nilo file-upload create` | Create a file upload. |
| `nilo file-upload send <file_upload_id>` | Send file contents. |
| `nilo file-upload complete <file_upload_id>` | Complete a file upload. |

## Examples

```bash
nilo file-upload list --json
nilo file-upload retrieve <file_upload_id> --json
nilo file-upload create --payload '{}'
nilo file-upload send <file_upload_id> --path ./example.pdf
nilo file-upload complete <file_upload_id>
```
