# File: src/notion_mcp/mcp_server/__init__.py
# Format: UTF-8
# =============================
# File Description:
# MCP server package for Agent/LLM structured tool access.
# TAG: mcp, server, package
# =============================

from .server import create_mcp_server, serve, supported_transports

__all__ = ["create_mcp_server", "serve", "supported_transports"]
