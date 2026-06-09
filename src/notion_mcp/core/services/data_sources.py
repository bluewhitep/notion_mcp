# File: src/notion_mcp/core/services/data_sources.py
# Format: UTF-8
# =============================
# File Description:
# Core service for Notion data source operations.
# TAG: core, services, data-sources
# =============================

from __future__ import annotations

from typing import Any

from .base import BaseNotionService


class DataSourcesService(BaseNotionService):
    # --------------------------------
    # Function Description:
    # Retrieves a Notion data source.
    # Inputs/Outputs:
    # Input data_source_id; returns Notion data source response.
    # Usage:
    # DataSourcesService(client).retrieve("data-source-id")
    # --------------------------------
    def retrieve(self, data_source_id: str) -> dict[str, Any]:
        return self._call(
            "data_sources.retrieve",
            self.client.data_sources.retrieve,
            data_source_id=data_source_id,
        )

    # --------------------------------
    # Function Description:
    # Creates a Notion data source.
    # Inputs/Outputs:
    # Input raw payload; returns Notion create response.
    # Usage:
    # DataSourcesService(client).create({"parent": {}})
    # --------------------------------
    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._call("data_sources.create", self.client.data_sources.create, **payload)

    # --------------------------------
    # Function Description:
    # Creates a Notion data source under an existing database container.
    # Inputs/Outputs:
    # Input database_id and payload; returns Notion create response.
    # Usage:
    # DataSourcesService(client).create_for_database("database-id", {"properties": {}})
    # --------------------------------
    def create_for_database(self, database_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        data = dict(payload)
        data.setdefault("parent", {"type": "database_id", "database_id": database_id})
        return self.create(data)

    # --------------------------------
    # Function Description:
    # Updates a Notion data source.
    # Inputs/Outputs:
    # Input data_source_id and raw payload; returns Notion update response.
    # Usage:
    # DataSourcesService(client).update("data-source-id", {"properties": {}})
    # --------------------------------
    def update(self, data_source_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self._call(
            "data_sources.update",
            self.client.data_sources.update,
            data_source_id=data_source_id,
            **payload,
        )

    # --------------------------------
    # Function Description:
    # Queries a Notion data source.
    # Inputs/Outputs:
    # Input data_source_id and query payload; returns Notion query response.
    # Usage:
    # DataSourcesService(client).query("data-source-id", {"page_size": 10})
    # --------------------------------
    def query(self, data_source_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._call(
            "data_sources.query",
            self.client.data_sources.query,
            data_source_id=data_source_id,
            **(payload or {}),
        )

    # --------------------------------
    # Function Description:
    # Lists page templates available for a Notion data source.
    # Inputs/Outputs:
    # Input data_source_id; returns Notion template listing response.
    # Usage:
    # DataSourcesService(client).templates("data-source-id")
    # --------------------------------
    def templates(self, data_source_id: str) -> dict[str, Any]:
        return self._call(
            "data_sources.list_templates",
            self.client.data_sources.list_templates,
            data_source_id=data_source_id,
        )

    # --------------------------------
    # Function Description:
    # Renames a data source property by property id or current property name.
    # Inputs/Outputs:
    # Input data_source_id, property id/name, and new name; returns update response.
    # Usage:
    # DataSourcesService(client).rename_property("data-source-id", "Status", "State")
    # --------------------------------
    def rename_property(self, data_source_id: str, property_id_or_name: str, new_name: str) -> dict[str, Any]:
        return self.update(
            data_source_id,
            {"properties": {property_id_or_name: {"name": new_name}}},
        )
