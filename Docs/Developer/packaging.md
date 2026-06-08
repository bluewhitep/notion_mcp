# Packaging

本文档面向开发者，说明本仓库的打包和本地安装策略。

## Package Layout

当前项目使用 `src` layout。

```text
src/
  notion_mcp/
```

console script：

```text
notion-mcp = notion_mcp.cli:app
```

构建后端：

```text
hatchling.build
```

选择 `hatchling` 的原因是隔离安装验证会从本地路径构建 wheel；该后端不会把 `build/`
或 `*.egg-info` 写回仓库工作树。

## Dependencies

核心依赖：

- `notion-client`
- `mcp`
- `typer`
- `pydantic`
- `fastapi`
- `uvicorn`

`fastapi` 和 `uvicorn` 当前用于 legacy REST 兼容入口。

开发验收依赖：

- `pytest`
- `pytest-asyncio`
- `httpx`
- `ruff`
- `mypy`

这些工具同时声明在 `dependency-groups.dev` 和 `project.optional-dependencies.dev`
中。前者支持仓库内 `uv run pytest`、`uv run ruff check .`、`uv run mypy src`
直接同步开发环境；后者保留 `notion-mcp[dev]` 形式的额外安装兼容性。

## Isolated Install

开发者验收命令：

```bash
uv run --no-project --with . notion-mcp --help
uv run --no-project --with . notion-mcp status --json
uv run --no-project --with . notion-mcp mcp serve --help
```

## Release Checks

发布前验收命令：

```bash
uv run pytest -q -p no:cacheprovider
uv run ruff check .
uv run mypy src
```

`ruff` 和 `mypy` 的缓存目录配置到 `/tmp`，避免在仓库中留下 `.ruff_cache/`
或 `.mypy_cache/`。

## Generated Files

发布前必须清理：

- Python bytecode cache。
- build output。
- package egg-info。
- pytest cache。
- ruff cache。
- mypy cache。

这些文件不属于仓库源码。
