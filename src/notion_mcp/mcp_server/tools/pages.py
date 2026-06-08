# File: src/notion_mcp/mcp_server/tools/pages.py
# Format: UTF-8
# =============================
# File Description:
# MCP tools for Notion page operations.
# TAG: mcp, tools, pages
# =============================

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from notion_mcp.core.errors import CoreError
from notion_mcp.core.models import dry_run_result

from .shared import core_error_payload, get_pages_service as _get_pages_service


# --------------------------------
# Function Description:
# Returns the Core pages service.
# Inputs/Outputs:
# No input; returns PagesService.
# Usage:
# get_pages_service().retrieve("page-id")
# --------------------------------
def get_pages_service():
    return _get_pages_service()


# --------------------------------
# Function Description:
# Registers page MCP tools.
# Inputs/Outputs:
# Input FastMCP server; output is server with page tools.
# Usage:
# register(server)
# --------------------------------
def register(server: FastMCP) -> None:
    @server.tool(
        name="page_retrieve",
        description="Retrieve a Notion page by id.",
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    def page_retrieve(page_id: str) -> dict[str, Any]:
        try:
            return get_pages_service().retrieve(page_id)
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(
        name="page_property_retrieve",
        description="Retrieve a Notion page property item with optional pagination.",
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    def page_property_retrieve(
        page_id: str,
        property_id: str,
        page_size: int | None = None,
        start_cursor: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if page_size is not None:
            params["page_size"] = page_size
        if start_cursor is not None:
            params["start_cursor"] = start_cursor
        try:
            return get_pages_service().retrieve_property_item(page_id, property_id, **params)
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(
        name="page_create",
        description="Create a Notion page from a raw Notion SDK payload.",
    )
    def page_create(payload: dict[str, Any], dry_run: bool = False) -> dict[str, Any]:
        if dry_run:
            return dry_run_result("pages.create", payload).__dict__
        try:
            return get_pages_service().create(payload)
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(
        name="page_update",
        description="Update a Notion page from a raw Notion SDK payload.",
    )
    def page_update(page_id: str, payload: dict[str, Any], dry_run: bool = False) -> dict[str, Any]:
        if dry_run:
            return dry_run_result("pages.update", {"page_id": page_id, **payload}).__dict__
        try:
            return get_pages_service().update(page_id, payload)
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(
        name="page_trash",
        description="Move a Notion page to trash. Requires confirm=true.",
        annotations=ToolAnnotations(destructiveHint=True),
    )
    def page_trash(page_id: str, confirm: bool = False, dry_run: bool = False) -> dict[str, Any]:
        if not confirm:
            return {
                "ok": False,
                "error": {
                    "code": "confirmation_required",
                    "message": "confirm=true is required for page_trash",
                },
            }
        if dry_run:
            return dry_run_result("pages.trash", {"page_id": page_id}).__dict__
        try:
            return get_pages_service().trash(page_id)
        except CoreError as exc:
            return core_error_payload(exc)
