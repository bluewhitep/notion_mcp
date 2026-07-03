# File: src/nilo/mcp_server/tools/views.py
# Format: UTF-8
# =============================
# File Description:
# MCP tools for Notion view operations.
# TAG: mcp, tools, views
# =============================

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from nilo.core.errors import CoreError

from .shared import core_error_payload, get_views_service as _get_views_service


def get_views_service():
    return _get_views_service()


def register(server: FastMCP) -> None:
    @server.tool(name="view_create", description="Create a Notion view from a raw SDK payload.")
    def view_create(payload: dict[str, Any], dry_run: bool = False) -> dict[str, Any]:
        if dry_run:
            from nilo.core.models import dry_run_result

            return dry_run_result("views.create", payload).__dict__
        try:
            return get_views_service().create(payload)
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(
        name="view_list",
        description="List Notion views using raw view query parameters.",
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    def view_list(params: dict[str, Any]) -> dict[str, Any]:
        try:
            return get_views_service().list(**params)
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(
        name="view_retrieve",
        description="Retrieve a Notion view by id.",
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    def view_retrieve(view_id: str) -> dict[str, Any]:
        try:
            return get_views_service().retrieve(view_id)
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(name="view_update", description="Update a Notion view from a raw SDK payload.")
    def view_update(
        view_id: str,
        payload: dict[str, Any],
        dry_run: bool = False,
    ) -> dict[str, Any]:
        if dry_run:
            from nilo.core.models import dry_run_result

            return dry_run_result("views.update", {"view_id": view_id, **payload}).__dict__
        try:
            return get_views_service().update(view_id, payload)
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(
        name="view_query",
        description="Query a Notion view using raw query payload.",
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    def view_query(view_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        try:
            return get_views_service().query(view_id, payload or {})
        except CoreError as exc:
            return core_error_payload(exc)
