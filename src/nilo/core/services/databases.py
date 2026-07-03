# File: src/nilo/core/services/databases.py
# Format: UTF-8
# =============================
# File Description:
# Core service for Notion database container operations.
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
    # Lists child data sources from a Notion database container response.
    # Inputs/Outputs:
    # Input database_id; returns the database response data_sources list.
    # Usage:
    # DatabasesService(client).list_data_sources("database-id")
    # --------------------------------
    def list_data_sources(self, database_id: str) -> list[dict[str, Any]]:
        database = self.retrieve(database_id)
        data_sources = database.get("data_sources", [])
        if not isinstance(data_sources, list):
            return []
        return [item for item in data_sources if isinstance(item, dict)]

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
    # Renames a Notion database container.
    # Inputs/Outputs:
    # Input database_id and new display name; returns Notion update response.
    # Usage:
    # DatabasesService(client).rename("database-id", "Project Database")
    # --------------------------------
    def rename(self, database_id: str, new_name: str) -> dict[str, Any]:
        return self.update(database_id, {"title": rich_text_title(new_name)})


# --------------------------------
# Function Description:
# Builds a Notion rich text title payload from plain text.
# Inputs/Outputs:
# Input display text; returns title rich text list.
# Usage:
# rich_text_title("Project Database")
# --------------------------------
def rich_text_title(text: str) -> list[dict[str, Any]]:
    return [{"type": "text", "text": {"content": text}}]
