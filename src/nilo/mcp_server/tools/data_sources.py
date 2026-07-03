# File: src/nilo/mcp_server/tools/data_sources.py
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

from nilo.core.errors import CoreError
from nilo.core.models import dry_run_result

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
        description="Create a Notion data source from a raw SDK payload or under a database container.",
    )
    def data_source_create(
        payload: dict[str, Any],
        database_id: str | None = None,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        dry_run_payload = dict(payload)
        if database_id is not None:
            dry_run_payload = {"database_id": database_id, "payload": payload}
        if dry_run:
            return dry_run_result("data_sources.create", dry_run_payload).__dict__
        try:
            if database_id is not None:
                return get_data_sources_service().create_for_database(database_id, payload)
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

    @server.tool(
        name="data_source_templates",
        description="List page templates available for a Notion data source.",
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    def data_source_templates(data_source_id: str) -> dict[str, Any]:
        try:
            return get_data_sources_service().templates(data_source_id)
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(
        name="data_source_property_rename",
        description="Rename a Notion data source property by id or current name.",
    )
    def data_source_property_rename(
        data_source_id: str,
        property_id_or_name: str,
        new_name: str,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        payload = {
            "data_source_id": data_source_id,
            "property_id_or_name": property_id_or_name,
            "new_name": new_name,
        }
        if dry_run:
            return dry_run_result("data_sources.property.rename", payload).__dict__
        try:
            return get_data_sources_service().rename_property(data_source_id, property_id_or_name, new_name)
        except CoreError as exc:
            return core_error_payload(exc)
