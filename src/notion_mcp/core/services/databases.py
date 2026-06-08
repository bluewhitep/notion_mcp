# File: src/notion_mcp/core/services/databases.py
# Format: UTF-8
# =============================
# File Description:
# Core service for legacy Notion database operations.
# TAG: core, services, databases
# =============================

from __future__ import annotations

from typing import Any

from .base import BaseNotionService


class DatabasesService(BaseNotionService):
    # --------------------------------
    # Function Description:
    # Retrieves a legacy Notion database.
    # Inputs/Outputs:
    # Input database_id; returns Notion database response.
    # Usage:
    # DatabasesService(client).retrieve("database-id")
    # --------------------------------
    def retrieve(self, database_id: str) -> dict[str, Any]:
        return self._call(
            "databases.retrieve",
            self.client.databases.retrieve,
            database_id=database_id,
        )

    # --------------------------------
    # Function Description:
    # Creates a legacy Notion database.
    # Inputs/Outputs:
    # Input raw payload; returns Notion create response.
    # Usage:
    # DatabasesService(client).create({"parent": {}})
    # --------------------------------
    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._call("databases.create", self.client.databases.create, **payload)

    # --------------------------------
    # Function Description:
    # Updates a legacy Notion database.
    # Inputs/Outputs:
    # Input database_id and raw payload; returns Notion update response.
    # Usage:
    # DatabasesService(client).update("database-id", {"title": []})
    # --------------------------------
    def update(self, database_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self._call(
            "databases.update",
            self.client.databases.update,
            database_id=database_id,
            **payload,
        )

    # --------------------------------
    # Function Description:
    # Queries a legacy Notion database.
    # Inputs/Outputs:
    # Input database_id and query payload; returns Notion query response.
    # Usage:
    # DatabasesService(client).query("database-id", {"page_size": 10})
    # --------------------------------
    def query(self, database_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._call(
            "databases.query",
            self.client.databases.query,
            database_id=database_id,
            **(payload or {}),
        )
