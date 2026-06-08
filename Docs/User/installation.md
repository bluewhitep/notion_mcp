# Installation

本文面向使用者，说明如何安装本地 Notion MCP 工具。

## 使用 uv 临时运行

在仓库根目录外也可以使用：

```bash
uv run --no-project --with /path/to/notion_mcp_project notion-mcp --help
```

## 使用 uvx 风格运行

如果已经发布到包索引，可使用：

```bash
uvx notion-mcp --help
```

当前本地开发仓库建议使用本地路径安装。

## 使用 pip 安装

```bash
pip install /path/to/notion_mcp_project
notion-mcp --help
```

## 卸载

```bash
pip uninstall notion-mcp
```

如果使用 `uv run --with /path/to/project` 临时运行，不需要单独卸载。
