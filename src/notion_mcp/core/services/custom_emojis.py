# File: src/notion_mcp/core/services/custom_emojis.py
# Format: UTF-8
# =============================
# File Description:
# Core service for Notion custom emoji operations.
# TAG: core, services, custom-emojis
# =============================

from __future__ import annotations

from typing import Any

from .base import BaseNotionService


class CustomEmojisService(BaseNotionService):
    # --------------------------------
    # Function Description:
    # Lists custom emojis available to the integration.
    # Inputs/Outputs:
    # Input optional paging params; returns Notion custom emoji list response.
    # Usage:
    # CustomEmojisService(client).list(page_size=10)
    # --------------------------------
    def list(self, **params: Any) -> dict[str, Any]:
        return self._call("custom_emojis.list", self.client.custom_emojis.list, **params)

    # --------------------------------
    # Function Description:
    # Retrieves a custom emoji when supported by the SDK.
    # Inputs/Outputs:
    # Input custom_emoji_id; returns Notion custom emoji response.
    # Usage:
    # CustomEmojisService(client).retrieve("emoji-id")
    # --------------------------------
    def retrieve(self, custom_emoji_id: str) -> dict[str, Any]:
        return self._call(
            "custom_emojis.retrieve",
            self.client.custom_emojis.retrieve,
            custom_emoji_id=custom_emoji_id,
        )
