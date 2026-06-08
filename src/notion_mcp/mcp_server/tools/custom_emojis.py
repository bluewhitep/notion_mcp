# File: src/notion_mcp/mcp_server/tools/custom_emojis.py
# Format: UTF-8
# =============================
# File Description:
# MCP tool for Notion custom emoji operations.
# TAG: mcp, tools, custom-emojis
# =============================

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from notion_mcp.core.errors import CoreError

from .shared import core_error_payload, get_custom_emojis_service as _get_custom_emojis_service


def get_custom_emojis_service():
    return _get_custom_emojis_service()


def register(server: FastMCP) -> None:
    @server.tool(
        name="custom_emoji_list",
        description="List Notion custom emojis available to the integration.",
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    def custom_emoji_list(page_size: int | None = None, start_cursor: str | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if page_size is not None:
            params["page_size"] = page_size
        if start_cursor is not None:
            params["start_cursor"] = start_cursor
        try:
            return get_custom_emojis_service().list(**params)
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(
        name="custom_emoji_retrieve",
        description="Retrieve a Notion custom emoji when supported by the SDK.",
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    def custom_emoji_retrieve(custom_emoji_id: str) -> dict[str, Any]:
        try:
            return get_custom_emojis_service().retrieve(custom_emoji_id)
        except CoreError as exc:
            return core_error_payload(exc)
