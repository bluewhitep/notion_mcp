# Packaging

This document describes the repository's packaging, local installation, and PyPI release strategy.

## Package Layout

The project uses a `src` layout:

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

`hatchling` is used because isolated install checks build a wheel from the local path without writing `build/` or `*.egg-info` back into the working tree.

## Dependencies

Runtime dependencies:

- `notion-client`
- `mcp`
- `typer`
- `pydantic`
- `fastapi`
- `uvicorn`

`fastapi` currently supports internal REST prototype compatibility code. `uvicorn` is still used by the HTTP server runtime.

## Runtime Stack

The project remains Python-based. `pyproject.toml` declares `requires-python = ">=3.10"` because:

- Existing source and tests are Python.
- The Notion Python SDK is reusable.
- The MCP Python SDK can implement the local MCP server directly.
- The existing pytest, Typer, FastAPI, and Pydantic toolchain is already in place.

Core creates the Notion SDK client and injects:

- bearer token
- Notion API version
- timeout
- retry policy
- fake client test doubles

CLI and MCP tools must not create Notion SDK clients directly.

The Notion API version is a global configuration field. The current default is `2026-03-11`; changing it requires compatibility tests.

The MCP Python SDK registers tools, exposes schemas, and handles stdio / streamable HTTP transport.

Typer powers the CLI. The CLI calls Core and supports human-readable output, `--json`, and `--dry-run`.

Pydantic is used for configuration models and structured input/output. The codebase uses Pydantic v2 APIs.

Development dependencies:

- `pytest`
- `pytest-asyncio`
- `httpx`
- `ruff`
- `mypy`

They are declared in both `dependency-groups.dev` and `project.optional-dependencies.dev`. The dependency group supports repository-local commands such as `uv run pytest`; the optional extra keeps `notion-nilo[dev]` compatibility.

## Isolated Install

Developer acceptance commands:

```bash
uv run --no-project --with . nilo --help
uv run --no-project --with . nilo config --global --show --json
uv run --no-project --with . nilo server run --help
```

## Release Checks

Run before publishing:

```bash
uv run pytest -q -p no:cacheprovider
uv run ruff check .
uv run mypy src
uv build --out-dir /tmp/notion-nilo-dist-check
```

`ruff` and `mypy` caches are configured under `/tmp` so `.ruff_cache/` and `.mypy_cache/` are not left in the repository.

## PyPI Publication

PyPI publication uses GitHub Actions Trusted Publishing. The repository and GitHub secrets do not store a PyPI API token.

Repository-side setup:

- `.github/workflows/publish.yml` builds and uploads on GitHub Release `published` events.
- The same workflow supports `workflow_dispatch`, but manual runs only build distributions and do not publish to PyPI.
- The `publish` job uses `contents: read` and `id-token: write` for GitHub OIDC.
- The GitHub environment name is `pypi`.

PyPI-side requirements:

1. The project name is `notion-nilo`.
2. A Trusted Publisher is configured for the GitHub repository.
3. The Trusted Publisher workflow file is `publish.yml`.
4. The Trusted Publisher environment is `pypi`.
5. The GitHub Release tag matches the version in `pyproject.toml`.

The previously published `notion-mcp` PyPI project is separate and is not renamed by PyPI. If old users need migration guidance, publish a separate notice release under that old project.

Release flow:

1. Confirm CI is green.
2. Confirm local release checks pass.
3. Create a GitHub Release.
4. Let `publish.yml` upload the sdist and wheel to PyPI after the release is published.

## Generated Files

Clean these before release:

- Python bytecode cache.
- Build output.
- Package egg-info.
- pytest cache.
- ruff cache.
- mypy cache.

These files are not repository source.
