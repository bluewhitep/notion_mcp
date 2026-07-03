# Core API

この文書は `src/nilo/core/` の現在の Core capability を記録します。Core は唯一の business logic layer です。CLI と MCP tools は Notion SDK を直接呼ばず、Core を呼び出します。

## Configuration

Module: `src/nilo/core/config.py`

- `CoreConfig`
  - `notion_token`、`user_name`、`user_id`、`notion_version`、`timeout_ms`、`retry`、`default_transport`、`audit_enabled` を保存します。
  - `user_id` が設定される場合は UUID である必要があります。
  - `notion_version` の default は `2026-03-11` です。
- `init_core_config(...)`
  - configuration を初期化し、local configuration file に書き込みます。
  - file permission は `0600` です。
- `load_core_config(...)`
  - configuration file を読み取り、validated `CoreConfig` を返します。
- `update_core_config(...)`
  - 渡された field だけを更新し、省略された field は消しません。
- `redacted_config(...)`
  - token を表示しない status-safe configuration を返します。

## Error model

Module: `src/nilo/core/errors.py`

- `CoreError`
  - Core errors の base class。
  - `to_dict()` は `type`、`code`、`message`、`details` を返します。
- `ConfigNotFoundError`
- `ConfigValidationError`
- `NotionAuthError`
- `NotionOperationError`

CLI JSON output と MCP tool responses は、この error structure を再利用します。

## Notion SDK client

Module: `src/nilo/core/client.py`

- `NotionClientFactory`
  - `CoreConfig` から Notion SDK client を作成します。
  - `auth`、`notion_version`、`timeout_ms`、`retry` を注入します。
  - tests と MCP scenarios 向けに `client_cls` と `fake_client` をサポートします。
- `create_notion_client(...)`
  - default client factory entrypoint。

## Authentication

Module: `src/nilo/core/auth.py`

- `AuthService.validate(...)`
  - `client.users.me()` を呼び出して token を検証します。
  - `expected_user_id` を渡すと、configured user identity と current token identity を比較します。
  - `AuthValidationResult` を返します。

## Audit

Module: `src/nilo/core/audit.py`

- `AuditRecorder.record(...)`
  - JSONL audit records を書き込みます。
  - `timestamp`、`configured_user_id`、`operation`、`target`、`dry_run`、`metadata` を記録します。
  - `notion_token`、`token`、`auth`、`authorization`、`bearer` などの sensitive fields を除去します。

## Notion domain services

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

これらの services は Core と Notion SDK-compatible client だけに依存します。CLI または MCP layer は import しません。

## Raw API

Module: `src/nilo/core/services/raw_api.py`

- `registered_operations()`
  - 許可された pass-through Notion SDK operation names を返します。
- `RawNotionService.invoke(operation, arguments)`
  - 登録済み operation だけを許可します。
  - 未登録 operation と private attributes を拒否します。
  - Supported public Notion SDK/API capabilities の controlled fallback を提供します。
