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

`fastapi` 当前只用于内部 REST 原型兼容代码。`uvicorn` 仍用于 HTTP server runtime。

## Runtime Stack

当前项目继续使用 Python，`pyproject.toml` 声明 `requires-python = ">=3.10"`。继续使用 Python 的原因是：

- 现有代码和测试都是 Python。
- Notion Python SDK 可复用。
- MCP Python SDK 可直接实现本地 MCP server。
- pytest、Typer、FastAPI 和 Pydantic 工具链已经存在。

Notion SDK 由 Core client factory 统一创建，并集中注入：

- bearer token
- Notion API version
- timeout
- retry policy
- fake client test double

CLI 和 MCP Tool 不应直接创建 Notion SDK client。

Notion API version 是全局配置项。当前默认目标版本为 `2026-03-11`，升级该版本时必须同步兼容性测试。

MCP Python SDK 用于创建真正的 MCP server、注册 tools、暴露 tool schema 并处理 stdio / Streamable HTTP transport。

Typer 是 CLI 框架；CLI 只调用 Core，支持普通文本输出、`--json` 输出和 `--dry-run`。

Pydantic 用于配置模型和结构化输入输出。当前代码使用 Pydantic v2 API。

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
uv run --no-project --with . notion-mcp config --global --show --json
uv run --no-project --with . notion-mcp server run --help
```

## Release Checks

发布前验收命令：

```bash
uv run pytest -q -p no:cacheprovider
uv run ruff check .
uv run mypy src
uv build --out-dir /tmp/notion-mcp-dist-check
```

`ruff` 和 `mypy` 的缓存目录配置到 `/tmp`，避免在仓库中留下 `.ruff_cache/`
或 `.mypy_cache/`。

## PyPI Publication

PyPI 发布使用 GitHub Actions Trusted Publishing，不在仓库或 GitHub secrets 中保存
PyPI API token。

仓库侧准备：

- `.github/workflows/publish.yml` 在 GitHub Release `published` 事件上构建并上传包。
- 同一个 workflow 支持 `workflow_dispatch`，但手动触发只构建分发包，不上传 PyPI。
- `publish` job 只授予 `contents: read` 和 `id-token: write`，用于 GitHub OIDC。
- GitHub environment 名称为 `pypi`。

PyPI 侧发布前必须完成：

1. 在 PyPI 创建或保留 `notion-mcp` 项目名。
2. 为 GitHub 仓库配置 Trusted Publisher。
3. Trusted Publisher 的 workflow 文件名必须匹配 `publish.yml`。
4. Trusted Publisher 的 environment 必须匹配 `pypi`。
5. 确认 GitHub Release tag 对应的版本已写入 `pyproject.toml`。

发布流程：

1. 确认 CI 通过。
2. 确认本地 release checks 通过。
3. 创建 GitHub Release。
4. GitHub Release 发布后，由 `publish.yml` 上传 sdist 和 wheel 到 PyPI。

## Generated Files

发布前必须清理：

- Python bytecode cache。
- build output。
- package egg-info。
- pytest cache。
- ruff cache。
- mypy cache。

这些文件不属于仓库源码。
