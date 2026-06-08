# File: src/notion_mcp/mcp_server/tools/raw_api.py
# Format: UTF-8
# =============================
# File Description:
# MCP tool for registered raw Notion SDK/API operations.
# TAG: mcp, tools, raw-api
# =============================

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from notion_mcp.core.errors import CoreError
from notion_mcp.core.services.raw_api import registered_operations

from .shared import core_error_payload, get_raw_api_service as _get_raw_api_service


def get_raw_api_service():
    return _get_raw_api_service()


def register(server: FastMCP) -> None:
    @server.tool(
        name="raw_api_invoke",
        description="Invoke a registered Notion SDK/API operation with raw arguments.",
    )
    def raw_api_invoke(operation: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        try:
            return get_raw_api_service().invoke(operation, arguments or {})
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(
        name="raw_api_registered_operations",
        description="List registered raw Notion SDK/API operations.",
    )
    def raw_api_registered_operations() -> dict[str, Any]:
        return {"operations": list(registered_operations())}
