# File: src/notion_mcp/mcp_server/tools/data_sources.py
# Format: UTF-8
# =============================
# File Description:
# MCP tools for Notion data source operations.
# TAG: mcp, tools, data-sources
# =============================

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from notion_mcp.core.errors import CoreError
from notion_mcp.core.models import dry_run_result

from .shared import core_error_payload, get_data_sources_service as _get_data_sources_service


def get_data_sources_service():
    return _get_data_sources_service()


def register(server: FastMCP) -> None:
    @server.tool(
        name="data_source_retrieve",
        description="Retrieve a Notion data source by id.",
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    def data_source_retrieve(data_source_id: str) -> dict[str, Any]:
        try:
            return get_data_sources_service().retrieve(data_source_id)
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(
        name="data_source_query",
        description="Query a Notion data source.",
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    def data_source_query(
        data_source_id: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        try:
            return get_data_sources_service().query(data_source_id, payload or {})
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(
        name="data_source_create",
        description="Create a Notion data source from a raw SDK payload.",
    )
    def data_source_create(payload: dict[str, Any], dry_run: bool = False) -> dict[str, Any]:
        if dry_run:
            return dry_run_result("data_sources.create", payload).__dict__
        try:
            return get_data_sources_service().create(payload)
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(
        name="data_source_update",
        description="Update a Notion data source from a raw SDK payload.",
    )
    def data_source_update(
        data_source_id: str,
        payload: dict[str, Any],
        dry_run: bool = False,
    ) -> dict[str, Any]:
        if dry_run:
            return dry_run_result(
                "data_sources.update",
                {"data_source_id": data_source_id, **payload},
            ).__dict__
        try:
            return get_data_sources_service().update(data_source_id, payload)
        except CoreError as exc:
            return core_error_payload(exc)
