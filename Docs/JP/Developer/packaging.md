# Packaging

この文書は repository の packaging、local installation、PyPI release strategy を説明します。

## Package layout

Project は `src` layout を使います。

```text
src/
  nilo/
```

Console script:

```text
nilo = nilo.cli:app
```

Build backend:

```text
hatchling.build
```

`hatchling` を使う理由は、isolated install checks が local path から wheel を build しても、`build/` や `*.egg-info` を working tree に書き戻さないためです。

## Dependencies

Runtime dependencies:

- `notion-client`
- `mcp`
- `typer`
- `pydantic`
- `fastapi`
- `uvicorn`

`fastapi` は現在 internal REST prototype compatibility code に使われます。`uvicorn` は HTTP server runtime で使います。

## Runtime stack

Project は Python を継続して使います。`pyproject.toml` は `requires-python = ">=3.10"` を宣言しています。

- 既存の source と tests は Python です。
- Notion Python SDK を再利用できます。
- MCP Python SDK で local MCP server を直接実装できます。
- pytest、Typer、FastAPI、Pydantic の toolchain が既にあります。

Core は Notion SDK client を作成し、bearer token、Notion API version、timeout、retry policy、fake client test doubles を注入します。

CLI と MCP tools は Notion SDK client を直接作成してはいけません。

Notion API version は global configuration field です。現在の default は `2026-03-11` です。変更する場合は compatibility tests が必要です。

## Isolated install

Developer acceptance commands:

```bash
uv run --no-project --with . nilo --help
uv run --no-project --with . nilo config --global --show --json
uv run --no-project --with . nilo server run --help
```

## Release checks

Publish 前に実行します。

```bash
uv run pytest -q -p no:cacheprovider
uv run ruff check .
uv run mypy src
uv build --out-dir /tmp/notion-nilo-dist-check
```

`ruff` と `mypy` の cache は `/tmp` 配下に設定し、repository に `.ruff_cache/` や `.mypy_cache/` を残さないようにします。

## PyPI publication

PyPI publication は GitHub Actions Trusted Publishing を使います。repository や GitHub secrets に PyPI API token は保存しません。

Repository-side setup:

- `.github/workflows/publish.yml` は GitHub Release `published` event で build/upload します。
- `workflow_dispatch` は distribution build のみで、PyPI には upload しません。
- `publish` job は GitHub OIDC のために `contents: read` と `id-token: write` を使います。
- GitHub environment name は `pypi` です。

PyPI-side requirements:

1. Project name は `notion-nilo`。
2. GitHub repository に Trusted Publisher を設定します。
3. Workflow file は `publish.yml`。
4. Environment は `pypi`。
5. GitHub Release tag は `pyproject.toml` の version と一致します。

以前公開された `notion-mcp` PyPI project は別 project で、PyPI により自動 rename されません。旧ユーザー向け案内が必要な場合は、旧 project に migration notice release を出します。
