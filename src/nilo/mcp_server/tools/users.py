# File: src/nilo/mcp_server/tools/users.py
# Format: UTF-8
# =============================
# File Description:
# MCP tools for Notion user operations.
# TAG: mcp, tools, users
# =============================

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from nilo.core.errors import CoreError

from .shared import core_error_payload, get_users_service as _get_users_service


def get_users_service():
    return _get_users_service()


def register(server: FastMCP) -> None:
    @server.tool(
        name="user_list",
        description="List Notion users available to the integration.",
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    def user_list(page_size: int | None = None, start_cursor: str | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if page_size is not None:
            params["page_size"] = page_size
        if start_cursor is not None:
            params["start_cursor"] = start_cursor
        try:
            return get_users_service().list(**params)
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(
        name="user_retrieve",
        description="Retrieve a Notion user by id.",
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    def user_retrieve(user_id: str) -> dict[str, Any]:
        try:
            return get_users_service().retrieve(user_id)
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(
        name="user_me",
        description="Retrieve the bot/user attached to the active token.",
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    def user_me() -> dict[str, Any]:
        try:
            return get_users_service().me()
        except CoreError as exc:
            return core_error_payload(exc)
