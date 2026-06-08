# 技术栈选型

本文档面向开发者，描述补全本地 Notion MCP 服务器时使用的技术栈和版本策略。

## Python

当前项目继续使用 Python。

原因：

- 已有代码是 Python。
- Notion Python SDK `notion-client` 可复用。
- MCP Python SDK 可直接实现本地 MCP server。
- pytest、Typer、FastAPI 等工具链已经存在。

当前 `pyproject.toml` 声明 `requires-python = ">=3.10"`，与 `mcp>=1.27` 的运行时下限一致。后续如要提升到 Python 3.12，需要新增兼容性测试和文档。

## uv

uv 是首选本地隔离安装和验证工具。

阶段 0 已使用以下模式验证隔离安装：

```bash
uv run --no-project --with /Users/mbp-14/Desktop/notion_mcp_project notion-mcp --help
```

后续开发应优先使用：

```bash
uv run pytest -q
uv run --with . notion-mcp --help
```

如果保留 `requirements.txt`，它只作为兼容安装文件；依赖事实以 `pyproject.toml` 为准。

## Notion SDK

Notion SDK 依赖是 `notion-client`。

Core 层必须集中创建 client，并统一注入：

- bearer token
- Notion API version
- timeout
- retry 策略
- fake client 测试替身

CLI、MCP Tool 和 legacy REST routes 不应直接创建 Notion SDK client。

## Notion API version

Notion API version 是项目级配置。

默认目标版本：`2026-03-11`。

设计要求：

- Core client 工厂统一管理 `Notion-Version`。
- 配置文件允许覆盖 version。
- 测试覆盖默认值和覆盖值。
- 文档记录 version 变更风险。

## MCP Python SDK

MCP Python SDK 是实现真正 MCP server 的目标依赖。

用途：

- 创建 MCP server。
- 注册 tools/resources/prompts。
- 支持 stdio 和 Streamable HTTP 等 transport。
- 生成和暴露 tool schema。
- 处理 MCP lifecycle 和 tool call 结果。

阶段 4 才引入 MCP server 实现；阶段 1 仅更新文档和测试边界。

## Typer

Typer 继续用于 CLI。

要求：

- CLI 只调用 Core。
- 普通输出给人读。
- `--json` 输出给程序使用。
- 写操作支持 `--dry-run`。
- `notion-mcp mcp serve` 负责启动 MCP server。

当前依赖使用 `typer>=0.9`，不使用不存在的 `typer[all]` extra。

## FastAPI

FastAPI 当前只作为 legacy REST 原型和兼容层。

要求：

- 不再把 FastAPI REST 路由描述为最终 MCP server。
- 迁移后 REST routes 应改为调用 Core。
- MCP Tool 不能通过 REST route 间接调用业务逻辑。

## Pydantic

Pydantic 用于配置模型、Core 输入输出模型和 MCP tool schema 支撑。

当前依赖为 `pydantic>=2.0`。代码应使用 Pydantic v2 API，例如 `model_validate` 和 `model_dump`。

## pytest

pytest 是默认测试框架。

测试目录目标：

- `tests/test_*.py`：legacy tests，不修改。
- `tests/v2/core/`
- `tests/v2/cli/`
- `tests/v2/mcp_server/`
- `tests/v2/scenarios/`
- `tests/live/`

## 质量工具

发布前验收工具：

- ruff
- mypy

`pytest`、`pytest-asyncio`、`httpx`、`ruff` 和 `mypy` 同时声明在
`dependency-groups.dev` 与 `project.optional-dependencies.dev` 中。仓库内开发和发布验收使用
`uv run pytest`、`uv run ruff check .`、`uv run mypy src`；隔离安装场景可继续使用
`notion-mcp[dev]`。
