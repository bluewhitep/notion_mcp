"""
FastAPI service application.

Defines the FastAPI application instance and registers functional routes. The
dependency layer reads configuration and initializes the Notion client.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Dependency functions exposed for external imports.
from .dependencies import get_config, get_notion_client  # noqa: F401

# Route modules grouped by domain.
from .routes import databases, pages, blocks


# Initialize FastAPI application.
app = FastAPI(
    title="Local Notion MCP Server",
    description="Local Notion MCP service providing database, page, and block APIs.",
    version="0.2.0",
)


@app.get("/")
async def root() -> JSONResponse:
    """Root route used for health checks."""
    return JSONResponse({"message": "Notion MCP server is running"})


# Register functional routes.
app.include_router(databases.router)
app.include_router(pages.router)
app.include_router(blocks.router)
