# File: src/nilo/mcp_server/tools/blocks.py
# Format: UTF-8
# =============================
# File Description:
# MCP tools for Notion block operations.
# TAG: mcp, tools, blocks
# =============================

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from nilo.core.errors import CoreError
from nilo.core.models import dry_run_result

from .shared import core_error_payload, get_blocks_service as _get_blocks_service


# --------------------------------
# Function Description:
# Returns the Core blocks service.
# Inputs/Outputs:
# No input; returns BlocksService.
# Usage:
# get_blocks_service().list_children("block-id")
# --------------------------------
def get_blocks_service():
    return _get_blocks_service()


# --------------------------------
# Function Description:
# Registers block MCP tools.
# Inputs/Outputs:
# Input FastMCP server; output is server with block tools.
# Usage:
# register(server)
# --------------------------------
def register(server: FastMCP) -> None:
    @server.tool(
        name="block_children_list",
        description="List Notion child blocks for a block id.",
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    def block_children_list(
        block_id: str,
        page_size: int | None = None,
        start_cursor: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if page_size is not None:
            params["page_size"] = page_size
        if start_cursor is not None:
            params["start_cursor"] = start_cursor
        try:
            return get_blocks_service().list_children(block_id, **params)
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(
        name="block_append",
        description="Append child blocks using the Notion 2026 position contract.",
    )
    def block_append(
        block_id: str,
        children: list[dict[str, Any]],
        position: dict[str, Any] | None = None,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"block_id": block_id, "children": children}
        if position is not None:
            payload["position"] = position
        if dry_run:
            return dry_run_result("blocks.children.append", payload).__dict__
        try:
            return get_blocks_service().append_children(
                block_id,
                children=children,
                position=position,
            )
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(
        name="block_update",
        description="Update a Notion block from a raw Notion SDK payload.",
    )
    def block_update(block_id: str, payload: dict[str, Any], dry_run: bool = False) -> dict[str, Any]:
        if dry_run:
            return dry_run_result("blocks.update", {"block_id": block_id, **payload}).__dict__
        try:
            return get_blocks_service().update(block_id, payload)
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(
        name="block_trash",
        description="Delete or trash a Notion block. Requires confirm=true.",
        annotations=ToolAnnotations(destructiveHint=True),
    )
    def block_trash(block_id: str, confirm: bool = False, dry_run: bool = False) -> dict[str, Any]:
        if not confirm:
            return {
                "ok": False,
                "error": {
                    "code": "confirmation_required",
                    "message": "confirm=true is required for block_trash",
                },
            }
        if dry_run:
            return dry_run_result("blocks.trash", {"block_id": block_id}).__dict__
        try:
            return get_blocks_service().trash(block_id)
        except CoreError as exc:
            return core_error_payload(exc)
