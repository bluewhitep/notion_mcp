# Core Tests

This document describes Core-layer test coverage and common verification commands.

## Coverage Goals

- Configuration model: initialization, load, update, path override, file permissions, token redaction, UUID validation, and default Notion API version.
- Error model: Core error code, message, details, and CLI/MCP-consumable structure.
- Client factory: token, version, timeout, retry injection, and fake client support.
- Auth: `users.me()` token validation, configured user ID matching, and error wrapping.
- Services: pages, blocks, databases, data sources, users, comments, views, file uploads, search, custom emojis, and Raw API behavior.
- Audit: JSONL audit records and sensitive-field cleanup.
- Boundary: Core does not depend on CLI, MCP server, or internal REST prototype routes.

## Common Commands

Core-focused verification:

```bash
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/nilo_uv_core uv run pytest -q -p no:cacheprovider
```

Full local verification:

```bash
env PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/private/tmp/nilo_uv_full uv run pytest -q -p no:cacheprovider
```

## Notes

- Core is the shared business layer for CLI and MCP tools.
- Add Core tests before exposing new Notion API capability through CLI or MCP.
- Real Notion live tests are skipped by default and must not be faked.
