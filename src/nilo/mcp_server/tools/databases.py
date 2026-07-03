# File: src/nilo/mcp_server/tools/databases.py
# Format: UTF-8
# =============================
# File Description:
# MCP tools for Notion database container operations.
# TAG: mcp, tools, databases
# =============================

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from nilo.core.errors import CoreError, DatabaseDataSourceSelectionError, NotionOperationError
from nilo.core.models import dry_run_result

from .shared import core_error_payload, get_databases_service as _get_databases_service
from .shared import get_data_sources_service as _get_data_sources_service
from .shared import get_raw_api_service as _get_raw_api_service


def get_databases_service():
    return _get_databases_service()


def get_data_sources_service():
    return _get_data_sources_service()


def get_raw_api_service():
    return _get_raw_api_service()


# --------------------------------
# Function Description:
# Resolves the single data source for a database shortcut query.
# Inputs/Outputs:
# Input database id and data source dictionaries; returns data source id or raises CoreError.
# Usage:
# resolve_single_data_source_id("database-id", [{"id": "data-source-id"}])
# --------------------------------
def resolve_single_data_source_id(database_id: str, data_sources: list[dict[str, Any]]) -> str:
    if not data_sources:
        raise NotionOperationError(
            "database.query",
            "Database has no data sources.",
            details={"database_id": database_id},
        )
    if len(data_sources) > 1:
        raise DatabaseDataSourceSelectionError(database_id, sources=data_sources, selector=None)
    data_source_id = data_sources[0].get("id")
    if not isinstance(data_source_id, str) or not data_source_id:
        raise NotionOperationError(
            "database.query",
            "Database data source response did not include an id.",
            details={"database_id": database_id, "data_source": data_sources[0]},
        )
    return data_source_id


def register(server: FastMCP) -> None:
    @server.tool(
        name="database_retrieve",
        description="Retrieve a Notion database container by id.",
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    def database_retrieve(database_id: str) -> dict[str, Any]:
        try:
            return get_databases_service().retrieve(database_id)
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(
        name="database_sources",
        description="List data sources contained by a Notion database container.",
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    def database_sources(database_id: str) -> dict[str, Any]:
        try:
            return {
                "database_id": database_id,
                "data_sources": get_databases_service().list_data_sources(database_id),
            }
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(
        name="database_query",
        description="Query a legacy Notion database. Prefer data_source_query for table-level queries.",
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    def database_query(database_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        try:
            database_service = get_databases_service()
            legacy_query = getattr(database_service, "query", None)
            if callable(legacy_query):
                return legacy_query(database_id, payload or {})
            list_data_sources = getattr(database_service, "list_data_sources", None)
            if callable(list_data_sources):
                data_source_id = resolve_single_data_source_id(database_id, list_data_sources(database_id))
                return get_data_sources_service().query(data_source_id, payload or {})
            return get_raw_api_service().invoke("databases.query", {"database_id": database_id, **(payload or {})})
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(
        name="database_create",
        description="Create a Notion database container from a raw SDK payload.",
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
        description="Update a Notion database container from a raw SDK payload.",
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

    @server.tool(
        name="database_rename",
        description="Rename a Notion database container.",
    )
    def database_rename(database_id: str, new_name: str, dry_run: bool = False) -> dict[str, Any]:
        payload = {"database_id": database_id, "new_name": new_name}
        if dry_run:
            return dry_run_result("databases.rename", payload).__dict__
        try:
            return get_databases_service().rename(database_id, new_name)
        except CoreError as exc:
            return core_error_payload(exc)
