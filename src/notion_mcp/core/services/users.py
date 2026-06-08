# File: src/notion_mcp/core/services/users.py
# Format: UTF-8
# =============================
# File Description:
# Core service for Notion user operations.
# TAG: core, services, users
# =============================

from __future__ import annotations

from typing import Any

from .base import BaseNotionService


class UsersService(BaseNotionService):
    # --------------------------------
    # Function Description:
    # Lists Notion users available to the integration.
    # Inputs/Outputs:
    # Input optional paging params; returns Notion list response.
    # Usage:
    # UsersService(client).list(page_size=10)
    # --------------------------------
    def list(self, **params: Any) -> dict[str, Any]:
        return self._call("users.list", self.client.users.list, **params)

    # --------------------------------
    # Function Description:
    # Retrieves a Notion user.
    # Inputs/Outputs:
    # Input user_id; returns Notion user response.
    # Usage:
    # UsersService(client).retrieve("user-id")
    # --------------------------------
    def retrieve(self, user_id: str) -> dict[str, Any]:
        return self._call("users.retrieve", self.client.users.retrieve, user_id=user_id)

    # --------------------------------
    # Function Description:
    # Retrieves the bot/user attached to the active token.
    # Inputs/Outputs:
    # No input; returns Notion users.me response.
    # Usage:
    # UsersService(client).me()
    # --------------------------------
    def me(self) -> dict[str, Any]:
        return self._call("users.me", self.client.users.me)
