# File: src/notion_mcp/mcp_server/tools/search.py
# Format: UTF-8
# =============================
# File Description:
# MCP tool for Notion workspace search.
# TAG: mcp, tools, search
# =============================

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from notion_mcp.core.errors import CoreError

from .shared import core_error_payload, get_search_service as _get_search_service


def get_search_service():
    return _get_search_service()


def register(server: FastMCP) -> None:
    @server.tool(
        name="search",
        description="Search Notion workspace using the raw Notion search payload.",
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    def search(payload: dict[str, Any] | None = None) -> dict[str, Any]:
        try:
            return get_search_service().search(payload or {})
        except CoreError as exc:
            return core_error_payload(exc)
