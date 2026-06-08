# File: src/notion_mcp/mcp_server/tools/shared.py
# Format: UTF-8
# =============================
# File Description:
# Shared Core service helpers for MCP tool modules.
# TAG: mcp, tools, shared
# =============================

from __future__ import annotations

from typing import Any

from notion_mcp.core.client import create_notion_client
from notion_mcp.core.config import load_core_config
from notion_mcp.core.errors import CoreError
from notion_mcp.core.services.blocks import BlocksService
from notion_mcp.core.services.comments import CommentsService
from notion_mcp.core.services.custom_emojis import CustomEmojisService
from notion_mcp.core.services.data_sources import DataSourcesService
from notion_mcp.core.services.databases import DatabasesService
from notion_mcp.core.services.file_uploads import FileUploadsService
from notion_mcp.core.services.pages import PagesService
from notion_mcp.core.services.raw_api import RawNotionService
from notion_mcp.core.services.search import SearchService
from notion_mcp.core.services.users import UsersService
from notion_mcp.core.services.views import ViewsService


# --------------------------------
# Function Description:
# Creates a Core Notion client from local configuration.
# Inputs/Outputs:
# No input; returns SDK-compatible client.
# Usage:
# get_core_client()
# --------------------------------
def get_core_client() -> Any:
    return create_notion_client(load_core_config())


# --------------------------------
# Function Description:
# Converts a CoreError to a structured MCP tool payload.
# Inputs/Outputs:
# Input CoreError; returns dictionary error payload.
# Usage:
# core_error_payload(exc)
# --------------------------------
def core_error_payload(error: CoreError) -> dict[str, Any]:
    return {"ok": False, "error": error.to_dict()}


# --------------------------------
# Function Description:
# Creates the Core pages service.
# Inputs/Outputs:
# No input; returns PagesService.
# Usage:
# get_pages_service()
# --------------------------------
def get_pages_service() -> PagesService:
    return PagesService(get_core_client())


# --------------------------------
# Function Description:
# Creates the Core blocks service.
# Inputs/Outputs:
# No input; returns BlocksService.
# Usage:
# get_blocks_service()
# --------------------------------
def get_blocks_service() -> BlocksService:
    return BlocksService(get_core_client())


# --------------------------------
# Function Description:
# Creates the Core databases service.
# Inputs/Outputs:
# No input; returns DatabasesService.
# Usage:
# get_databases_service()
# --------------------------------
def get_databases_service() -> DatabasesService:
    return DatabasesService(get_core_client())


# --------------------------------
# Function Description:
# Creates the Core data sources service.
# Inputs/Outputs:
# No input; returns DataSourcesService.
# Usage:
# get_data_sources_service()
# --------------------------------
def get_data_sources_service() -> DataSourcesService:
    return DataSourcesService(get_core_client())


# --------------------------------
# Function Description:
# Creates the Core users service.
# Inputs/Outputs:
# No input; returns UsersService.
# Usage:
# get_users_service()
# --------------------------------
def get_users_service() -> UsersService:
    return UsersService(get_core_client())


# --------------------------------
# Function Description:
# Creates the Core comments service.
# Inputs/Outputs:
# No input; returns CommentsService.
# Usage:
# get_comments_service()
# --------------------------------
def get_comments_service() -> CommentsService:
    return CommentsService(get_core_client())


# --------------------------------
# Function Description:
# Creates the Core views service.
# Inputs/Outputs:
# No input; returns ViewsService.
# Usage:
# get_views_service()
# --------------------------------
def get_views_service() -> ViewsService:
    return ViewsService(get_core_client())


# --------------------------------
# Function Description:
# Creates the Core file uploads service.
# Inputs/Outputs:
# No input; returns FileUploadsService.
# Usage:
# get_file_uploads_service()
# --------------------------------
def get_file_uploads_service() -> FileUploadsService:
    return FileUploadsService(get_core_client())


# --------------------------------
# Function Description:
# Creates the Core search service.
# Inputs/Outputs:
# No input; returns SearchService.
# Usage:
# get_search_service()
# --------------------------------
def get_search_service() -> SearchService:
    return SearchService(get_core_client())


# --------------------------------
# Function Description:
# Creates the Core custom emojis service.
# Inputs/Outputs:
# No input; returns CustomEmojisService.
# Usage:
# get_custom_emojis_service()
# --------------------------------
def get_custom_emojis_service() -> CustomEmojisService:
    return CustomEmojisService(get_core_client())


# --------------------------------
# Function Description:
# Creates the Core raw API service.
# Inputs/Outputs:
# No input; returns RawNotionService.
# Usage:
# get_raw_api_service()
# --------------------------------
def get_raw_api_service() -> RawNotionService:
    return RawNotionService(get_core_client())
