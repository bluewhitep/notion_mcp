# Core Tests

この文書は Core layer の test coverage とよく使う verification commands を説明します。

## Coverage goals

- Configuration model: initialization、load、update、path override、file permissions、token redaction、UUID validation、default Notion API version。
- Error model: Core error code、message、details、CLI/MCP で消費できる structure。
- Client factory: token、version、timeout、retry injection、fake client support。
- Auth: `users.me()` token validation、configured user ID matching、error wrapping。
- Services: pages、blocks、databases、data sources、users、comments、views、file uploads、search、custom emojis、Raw API behavior。
- Audit: JSONL audit records と sensitive-field cleanup。
- Boundary: Core は CLI、MCP server、internal REST prototype routes に依存しません。

## Common commands

Core-focused verification:

```bash
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/nilo_uv_core uv run pytest -q -p no:cacheprovider
```

Full local verification:

```bash
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/nilo_uv_full uv run pytest -q -p no:cacheprovider
```

## Notes

- Core は CLI と MCP tools の shared business layer です。
- 新しい Notion API capability は、CLI/MCP に出す前に Core tests を追加します。
- Real Notion live tests は default skip であり、成功を偽装してはいけません。
