# File: src/notion_mcp/mcp_server/tools/databases.py
# Format: UTF-8
# =============================
# File Description:
# MCP tools for legacy Notion database operations.
# TAG: mcp, tools, databases
# =============================

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from notion_mcp.core.errors import CoreError
from notion_mcp.core.models import dry_run_result

from .shared import core_error_payload, get_databases_service as _get_databases_service


def get_databases_service():
    return _get_databases_service()


def register(server: FastMCP) -> None:
    @server.tool(
        name="database_retrieve",
        description="Retrieve a legacy Notion database by id.",
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    def database_retrieve(database_id: str) -> dict[str, Any]:
        try:
            return get_databases_service().retrieve(database_id)
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(
        name="database_query",
        description="Query a legacy Notion database.",
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    def database_query(database_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        try:
            return get_databases_service().query(database_id, payload or {})
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(
        name="database_create",
        description="Create a legacy Notion database from a raw SDK payload.",
    )
    def database_create(payload: dict[str, Any], dry_run: bool = False) -> dict[str, Any]:
        if dry_run:
            return dry_run_result("databases.create", payload).__dict__
        try:
            return get_databases_service().create(payload)
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(
        name="database_update",
        description="Update a legacy Notion database from a raw SDK payload.",
    )
    def database_update(
        database_id: str,
        payload: dict[str, Any],
        dry_run: bool = False,
    ) -> dict[str, Any]:
        if dry_run:
            return dry_run_result("databases.update", {"database_id": database_id, **payload}).__dict__
        try:
            return get_databases_service().update(database_id, payload)
        except CoreError as exc:
            return core_error_payload(exc)
