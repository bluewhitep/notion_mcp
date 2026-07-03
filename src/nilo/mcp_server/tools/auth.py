# File: src/nilo/mcp_server/tools/auth.py
# Format: UTF-8
# =============================
# File Description:
# MCP tools for validating configured Notion authentication.
# TAG: mcp, tools, auth
# =============================

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from nilo.core.auth import AuthService
from nilo.core.client import create_notion_client
from nilo.core.config import load_core_config
from nilo.core.errors import CoreError

from .shared import core_error_payload


# --------------------------------
# Function Description:
# Registers auth MCP tools.
# Inputs/Outputs:
# Input FastMCP server; output is server with auth tools.
# Usage:
# register(server)
# --------------------------------
def register(server: FastMCP) -> None:
    @server.tool(
        name="auth_validate",
        description="Validate the configured Notion token and optional configured user id.",
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    def auth_validate() -> dict[str, Any]:
        try:
            config = load_core_config()
            result = AuthService(create_notion_client(config)).validate(
                expected_user_id=config.user_id
            )
        except CoreError as exc:
            return core_error_payload(exc)
        return {
            "valid": result.valid,
            "user_id": result.user_id,
            "name": result.name,
            "raw": result.raw,
        }

    @server.tool(
        name="auth_whoami",
        description="Return the Notion user associated with the configured token.",
        annotations=ToolAnnotations(readOnlyHint=True),
    )
    def auth_whoami() -> dict[str, Any]:
        return auth_validate()
