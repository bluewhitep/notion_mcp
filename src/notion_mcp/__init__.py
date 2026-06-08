"""
notion_mcp
===============

本包包含本地 Notion MCP 服务的实现，包括配置管理、FastAPI 服务、CLI 工具以及路由模块。
使用者可通过 `notion-mcp` 命令行来初始化配置并启动服务。

模块结构概览：

- `config`：负责读取和保存全局配置（集成 token 与用户 ID）。
- `models`：包含 Pydantic 数据模型，用于校验配置和请求/响应体。
- `routes`：按功能划分的 FastAPI 路由（数据库、页面、区块等）。
- `server`：构建 FastAPI 应用并注册路由。
- `cli`：命令行入口，提供初始化配置和启动服务等功能。

"""

from importlib import metadata

try:
    __version__ = metadata.version(__name__)
except metadata.PackageNotFoundError:
    # Package is not installed; fallback for local development
    __version__ = "0.0.0"

__all__ = ["__version__"]
