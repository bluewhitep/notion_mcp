"""
FastAPI 服务应用。

该模块定义了 FastAPI 应用实例并注册各功能路由。通过依赖注入机制从配置文件读取
Notion 集成 token，初始化 Notion 客户端，并在路由处理函数中使用。
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse

# 依赖函数供外部引用
from .dependencies import get_config, get_notion_client  # noqa: F401

# 路由模块按功能导入
from .routes import databases, pages, blocks


# 初始化 FastAPI 应用
app = FastAPI(
    title="Local Notion MCP Server",
    description="本地 Notion MCP 服务，提供数据库、页面和区块操作的 API。",
    version="0.2.0",
)


@app.get("/")
async def root() -> JSONResponse:
    """根路由，用于健康检查。"""
    return JSONResponse({"message": "Notion MCP server is running"})


# 注册各功能路由
app.include_router(databases.router)
app.include_router(pages.router)
app.include_router(blocks.router)
