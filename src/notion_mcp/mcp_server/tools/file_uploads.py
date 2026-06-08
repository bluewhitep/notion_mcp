# File: src/notion_mcp/mcp_server/tools/file_uploads.py
# Format: UTF-8
# =============================
# File Description:
# MCP tools for Notion file upload lifecycle operations.
# TAG: mcp, tools, file-uploads
# =============================

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from notion_mcp.core.errors import CoreError
from notion_mcp.core.models import dry_run_result

from .shared import core_error_payload, get_file_uploads_service as _get_file_uploads_service


def get_file_uploads_service():
    return _get_file_uploads_service()


def register(server: FastMCP) -> None:
    @server.tool(
        name="file_upload_list",
        description="List Notion file upload objects when supported by the SDK.",
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    def file_upload_list(
        page_size: int | None = None,
        start_cursor: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if page_size is not None:
            params["page_size"] = page_size
        if start_cursor is not None:
            params["start_cursor"] = start_cursor
        try:
            return get_file_uploads_service().list(**params)
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(name="file_upload_create", description="Create a Notion file upload object.")
    def file_upload_create(payload: dict[str, Any], dry_run: bool = False) -> dict[str, Any]:
        if dry_run:
            return dry_run_result("file_uploads.create", payload).__dict__
        try:
            return get_file_uploads_service().create(payload)
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(
        name="file_upload_retrieve",
        description="Retrieve a Notion file upload object by id.",
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    def file_upload_retrieve(file_upload_id: str) -> dict[str, Any]:
        try:
            return get_file_uploads_service().retrieve(file_upload_id)
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(name="file_upload_send", description="Send a Notion file upload payload.")
    def file_upload_send(
        file_upload_id: str,
        payload: dict[str, Any],
        dry_run: bool = False,
    ) -> dict[str, Any]:
        if dry_run:
            return dry_run_result(
                "file_uploads.send",
                {"file_upload_id": file_upload_id, **payload},
            ).__dict__
        try:
            return get_file_uploads_service().send(file_upload_id, payload)
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(name="file_upload_complete", description="Complete a Notion file upload.")
    def file_upload_complete(
        file_upload_id: str,
        payload: dict[str, Any] | None = None,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        if dry_run:
            return dry_run_result(
                "file_uploads.complete",
                {"file_upload_id": file_upload_id, **(payload or {})},
            ).__dict__
        try:
            return get_file_uploads_service().complete(file_upload_id, payload or {})
        except CoreError as exc:
            return core_error_payload(exc)
