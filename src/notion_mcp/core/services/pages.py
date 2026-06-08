# File: src/notion_mcp/core/services/pages.py
# Format: UTF-8
# =============================
# File Description:
# Core service for Notion page operations.
# TAG: core, services, pages
# =============================

from __future__ import annotations

from typing import Any

from .base import BaseNotionService


class PagesService(BaseNotionService):
    # --------------------------------
    # Function Description:
    # Retrieves a Notion page.
    # Inputs/Outputs:
    # Input page_id; returns Notion page response.
    # Usage:
    # PagesService(client).retrieve("page-id")
    # --------------------------------
    def retrieve(self, page_id: str) -> dict[str, Any]:
        return self._call("pages.retrieve", self.client.pages.retrieve, page_id=page_id)

    # --------------------------------
    # Function Description:
    # Retrieves a Notion page property item with optional pagination.
    # Inputs/Outputs:
    # Input page_id, property_id, and paging params; returns property item response.
    # Usage:
    # PagesService(client).retrieve_property_item("page-id", "property-id", page_size=25)
    # --------------------------------
    def retrieve_property_item(
        self,
        page_id: str,
        property_id: str,
        **params: Any,
    ) -> dict[str, Any]:
        return self._call(
            "pages.properties.retrieve",
            self.client.pages.properties.retrieve,
            page_id=page_id,
            property_id=property_id,
            **params,
        )

    # --------------------------------
    # Function Description:
    # Creates a Notion page from a raw SDK payload.
    # Inputs/Outputs:
    # Input payload dictionary; returns Notion create response.
    # Usage:
    # PagesService(client).create({"parent": {"page_id": "root"}})
    # --------------------------------
    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._call("pages.create", self.client.pages.create, **payload)

    # --------------------------------
    # Function Description:
    # Updates a Notion page from a raw SDK payload.
    # Inputs/Outputs:
    # Input page_id and payload; returns Notion update response.
    # Usage:
    # PagesService(client).update("page-id", {"properties": {}})
    # --------------------------------
    def update(self, page_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self._call("pages.update", self.client.pages.update, page_id=page_id, **payload)

    # --------------------------------
    # Function Description:
    # Moves a Notion page to trash using the 2026 in_trash field.
    # Inputs/Outputs:
    # Input page_id; returns Notion update response.
    # Usage:
    # PagesService(client).trash("page-id")
    # --------------------------------
    def trash(self, page_id: str) -> dict[str, Any]:
        return self.update(page_id, {"in_trash": True})
