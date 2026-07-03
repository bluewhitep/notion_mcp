# File: src/nilo/mcp_server/tools/comments.py
# Format: UTF-8
# =============================
# File Description:
# MCP tools for Notion comment operations.
# TAG: mcp, tools, comments
# =============================

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from nilo.core.errors import CoreError
from nilo.core.models import dry_run_result

from .shared import core_error_payload, get_comments_service as _get_comments_service


def get_comments_service():
    return _get_comments_service()


def register(server: FastMCP) -> None:
    @server.tool(
        name="comment_list",
        description="List Notion comments using raw Notion comment query parameters.",
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    def comment_list(params: dict[str, Any]) -> dict[str, Any]:
        try:
            return get_comments_service().list(**params)
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(
        name="comment_create",
        description="Create a Notion comment from a raw SDK payload.",
    )
    def comment_create(payload: dict[str, Any], dry_run: bool = False) -> dict[str, Any]:
        if dry_run:
            return dry_run_result("comments.create", payload).__dict__
        try:
            return get_comments_service().create(payload)
        except CoreError as exc:
            return core_error_payload(exc)

    @server.tool(name="comment_reply", description="Reply to a Notion discussion.")
    def comment_reply(
        discussion_id: str,
        rich_text: list[dict[str, Any]],
        dry_run: bool = False,
    ) -> dict[str, Any]:
        payload = {"discussion_id": discussion_id, "rich_text": rich_text}
        if dry_run:
            return dry_run_result("comments.reply", payload).__dict__
        try:
            return get_comments_service().reply(discussion_id, rich_text)
        except CoreError as exc:
            return core_error_payload(exc)
