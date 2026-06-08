# File: src/notion_mcp/core/services/search.py
# Format: UTF-8
# =============================
# File Description:
# Core service for Notion workspace search.
# TAG: core, services, search
# =============================

from __future__ import annotations

from typing import Any

from .base import BaseNotionService


class SearchService(BaseNotionService):
    # --------------------------------
    # Function Description:
    # Searches the Notion workspace through the SDK search operation.
    # Inputs/Outputs:
    # Input raw search payload; returns Notion search response.
    # Usage:
    # SearchService(client).search({"query": "Project"})
    # --------------------------------
    def search(self, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._call("search", self.client.search, **(payload or {}))
