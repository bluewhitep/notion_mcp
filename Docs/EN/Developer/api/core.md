# Core API

This document records the current Core capabilities under `src/nilo/core/`. Core is the only business logic layer. CLI and MCP tools call Core instead of calling the Notion SDK directly.

## Configuration

Module: `src/nilo/core/config.py`

- `CoreConfig`
  - Stores `notion_token`, `user_name`, `user_id`, `notion_version`, `timeout_ms`, `retry`, `default_transport`, and `audit_enabled`.
  - Requires `user_id` to be a UUID when it is set.
  - Defaults `notion_version` to `2026-03-11`.
- `init_core_config(...)`
  - Initializes configuration and writes the local configuration file.
  - Writes configuration files with `0600` permissions.
- `load_core_config(...)`
  - Reads a configuration file and returns a validated `CoreConfig`.
- `update_core_config(...)`
  - Updates only provided fields and does not clear omitted fields.
- `redacted_config(...)`
  - Returns status-safe configuration without exposing the token.

## Error Model

Module: `src/nilo/core/errors.py`

- `CoreError`
  - Base class for Core errors.
  - `to_dict()` returns `type`, `code`, `message`, and `details`.
- `ConfigNotFoundError`
- `ConfigValidationError`
- `NotionAuthError`
- `NotionOperationError`

CLI JSON output and MCP tool responses should reuse these structures.

## Notion SDK Client

Module: `src/nilo/core/client.py`

- `NotionClientFactory`
  - Creates a Notion SDK client from `CoreConfig`.
  - Injects `auth`, `notion_version`, `timeout_ms`, and `retry`.
  - Supports `client_cls` and `fake_client` for tests and MCP scenarios.
- `create_notion_client(...)`
  - Default client factory entrypoint.

## Authentication

Module: `src/nilo/core/auth.py`

- `AuthService.validate(...)`
  - Calls `client.users.me()` to validate the token.
  - Accepts `expected_user_id` to compare configured user identity with the current token identity.
  - Returns `AuthValidationResult`.

## Audit

Module: `src/nilo/core/audit.py`

- `AuditRecorder.record(...)`
  - Writes JSONL audit records.
  - Records include `timestamp`, `configured_user_id`, `operation`, `target`, `dry_run`, and `metadata`.
  - Removes sensitive fields such as `notion_token`, `token`, `auth`, `authorization`, and `bearer`.

## Notion Domain Services

Directory: `src/nilo/core/services/`

Current service modules:

- `blocks.py`
- `pages.py`
- `databases.py`
- `data_sources.py`
- `users.py`
- `comments.py`
- `views.py`
- `file_uploads.py`
- `search.py`
- `custom_emojis.py`
- `raw_api.py`

These services depend only on Core and a Notion SDK-compatible client. They do not import CLI or MCP layers.

## Raw API

Module: `src/nilo/core/services/raw_api.py`

- `registered_operations()`
  - Returns the allowed pass-through Notion SDK operation names.
- `RawNotionService.invoke(operation, arguments)`
  - Allows only registered operations.
  - Rejects unregistered operations and private attributes.
  - Provides a controlled fallback for supported public Notion SDK/API capabilities.
