# File: src/notion_mcp/cli/core_services.py
# Format: UTF-8
# =============================
# File Description:
# CLI helpers that connect commands to Core services.
# TAG: cli, core-services
# =============================

from __future__ import annotations

from typing import Any

from notion_mcp.core.client import create_notion_client
from notion_mcp.core.config import load_core_config
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
# Creates a Notion SDK-compatible client through Core.
# Inputs/Outputs:
# No input; returns client created from local Core config.
# Usage:
# get_core_client()
# --------------------------------
def get_core_client() -> Any:
    return create_notion_client(load_core_config())


# --------------------------------
# Function Description:
# Creates the Core pages service for CLI commands.
# Inputs/Outputs:
# No input; returns PagesService.
# Usage:
# get_pages_service().retrieve("page-id")
# --------------------------------
def get_pages_service() -> PagesService:
    return PagesService(get_core_client())


# --------------------------------
# Function Description:
# Creates the Core blocks service for CLI commands.
# Inputs/Outputs:
# No input; returns BlocksService.
# Usage:
# get_blocks_service().list_children("block-id")
# --------------------------------
def get_blocks_service() -> BlocksService:
    return BlocksService(get_core_client())


# --------------------------------
# Function Description:
# Creates the Core databases service for CLI commands.
# Inputs/Outputs:
# No input; returns DatabasesService.
# Usage:
# get_databases_service().retrieve("database-id")
# --------------------------------
def get_databases_service() -> DatabasesService:
    return DatabasesService(get_core_client())


# --------------------------------
# Function Description:
# Creates the Core data sources service for CLI commands.
# Inputs/Outputs:
# No input; returns DataSourcesService.
# Usage:
# get_data_sources_service().retrieve("data-source-id")
# --------------------------------
def get_data_sources_service() -> DataSourcesService:
    return DataSourcesService(get_core_client())


# --------------------------------
# Function Description:
# Creates the Core users service for CLI commands.
# Inputs/Outputs:
# No input; returns UsersService.
# Usage:
# get_users_service().me()
# --------------------------------
def get_users_service() -> UsersService:
    return UsersService(get_core_client())


# --------------------------------
# Function Description:
# Creates the Core comments service for CLI commands.
# Inputs/Outputs:
# No input; returns CommentsService.
# Usage:
# get_comments_service().list(block_id="block-id")
# --------------------------------
def get_comments_service() -> CommentsService:
    return CommentsService(get_core_client())


# --------------------------------
# Function Description:
# Creates the Core views service for CLI commands.
# Inputs/Outputs:
# No input; returns ViewsService.
# Usage:
# get_views_service().retrieve("view-id")
# --------------------------------
def get_views_service() -> ViewsService:
    return ViewsService(get_core_client())


# --------------------------------
# Function Description:
# Creates the Core file uploads service for CLI commands.
# Inputs/Outputs:
# No input; returns FileUploadsService.
# Usage:
# get_file_uploads_service().retrieve("file-upload-id")
# --------------------------------
def get_file_uploads_service() -> FileUploadsService:
    return FileUploadsService(get_core_client())


# --------------------------------
# Function Description:
# Creates the Core search service for CLI commands.
# Inputs/Outputs:
# No input; returns SearchService.
# Usage:
# get_search_service().search({"query": "Roadmap"})
# --------------------------------
def get_search_service() -> SearchService:
    return SearchService(get_core_client())


# --------------------------------
# Function Description:
# Creates the Core custom emojis service for CLI commands.
# Inputs/Outputs:
# No input; returns CustomEmojisService.
# Usage:
# get_custom_emojis_service().list()
# --------------------------------
def get_custom_emojis_service() -> CustomEmojisService:
    return CustomEmojisService(get_core_client())


# --------------------------------
# Function Description:
# Creates the Core raw API service for CLI commands.
# Inputs/Outputs:
# No input; returns RawNotionService.
# Usage:
# get_raw_api_service().invoke("pages.retrieve", {"page_id": "id"})
# --------------------------------
def get_raw_api_service() -> RawNotionService:
    return RawNotionService(get_core_client())
