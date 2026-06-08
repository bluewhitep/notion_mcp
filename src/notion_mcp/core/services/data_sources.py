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
