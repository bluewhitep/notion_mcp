# File: src/notion_mcp/core/services/views.py
# Format: UTF-8
# =============================
# File Description:
# Core service for Notion view operations when exposed by the SDK/API.
# TAG: core, services, views
# =============================

from __future__ import annotations

from typing import Any

from .base import BaseNotionService


class ViewsService(BaseNotionService):
    # --------------------------------
    # Function Description:
    # Creates a Notion view using the SDK views object.
    # Inputs/Outputs:
    # Input raw payload; returns Notion view create response.
    # Usage:
    # ViewsService(client).create({"data_source_id": "id"})
    # --------------------------------
    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._call("views.create", self.client.views.create, **payload)

    # --------------------------------
    # Function Description:
    # Lists views using the SDK views object.
    # Inputs/Outputs:
    # Input raw params; returns Notion views list response.
    # Usage:
    # ViewsService(client).list(data_source_id="data-source-id")
    # --------------------------------
    def list(self, **params: Any) -> dict[str, Any]:
        return self._call("views.list", self.client.views.list, **params)

    # --------------------------------
    # Function Description:
    # Retrieves a Notion view.
    # Inputs/Outputs:
    # Input view_id; returns Notion view response.
    # Usage:
    # ViewsService(client).retrieve("view-id")
    # --------------------------------
    def retrieve(self, view_id: str) -> dict[str, Any]:
        return self._call("views.retrieve", self.client.views.retrieve, view_id=view_id)

    # --------------------------------
    # Function Description:
    # Updates a Notion view using the SDK views object.
    # Inputs/Outputs:
    # Input view_id and payload; returns Notion view update response.
    # Usage:
    # ViewsService(client).update("view-id", {"name": "Roadmap"})
    # --------------------------------
    def update(self, view_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self._call("views.update", self.client.views.update, view_id=view_id, **payload)

    # --------------------------------
    # Function Description:
    # Queries a Notion view using the SDK views object.
    # Inputs/Outputs:
    # Input view_id and query payload; returns Notion view query response.
    # Usage:
    # ViewsService(client).query("view-id", {"page_size": 10})
    # --------------------------------
    def query(self, view_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._call(
            "views.query",
            self.client.views.query,
            view_id=view_id,
            **(payload or {}),
        )
