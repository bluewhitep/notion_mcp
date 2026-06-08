# File: src/notion_mcp/core/services/blocks.py
# Format: UTF-8
# =============================
# File Description:
# Core service for Notion block operations.
# TAG: core, services, blocks
# =============================

from __future__ import annotations

from typing import Any

from .base import BaseNotionService


class BlocksService(BaseNotionService):
    # --------------------------------
    # Function Description:
    # Retrieves a Notion block.
    # Inputs/Outputs:
    # Input block_id; returns Notion block response.
    # Usage:
    # BlocksService(client).retrieve("block-id")
    # --------------------------------
    def retrieve(self, block_id: str) -> dict[str, Any]:
        return self._call("blocks.retrieve", self.client.blocks.retrieve, block_id=block_id)

    # --------------------------------
    # Function Description:
    # Lists children for a Notion block.
    # Inputs/Outputs:
    # Input block_id plus optional paging params; returns Notion list response.
    # Usage:
    # BlocksService(client).list_children("block-id", page_size=10)
    # --------------------------------
    def list_children(self, block_id: str, **params: Any) -> dict[str, Any]:
        return self._call(
            "blocks.children.list",
            self.client.blocks.children.list,
            block_id=block_id,
            **params,
        )

    # --------------------------------
    # Function Description:
    # Appends children to a block using the 2026 position contract.
    # Inputs/Outputs:
    # Input block_id, children, optional position and params; returns Notion append response.
    # Usage:
    # BlocksService(client).append_children("block-id", children=[], position={"type": "end"})
    # --------------------------------
    def append_children(
        self,
        block_id: str,
        *,
        children: list[dict[str, Any]],
        position: dict[str, Any] | None = None,
        **params: Any,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"block_id": block_id, "children": children}
        if position is not None:
            payload["position"] = position
        payload.update(params)
        return self._call(
            "blocks.children.append",
            self.client.blocks.children.append,
            **payload,
        )

    # --------------------------------
    # Function Description:
    # Updates a Notion block.
    # Inputs/Outputs:
    # Input block_id and payload; returns Notion update response.
    # Usage:
    # BlocksService(client).update("block-id", {"paragraph": {}})
    # --------------------------------
    def update(self, block_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self._call("blocks.update", self.client.blocks.update, block_id=block_id, **payload)

    # --------------------------------
    # Function Description:
    # Moves a Notion block to trash.
    # Inputs/Outputs:
    # Input block_id; returns Notion delete response when available.
    # Usage:
    # BlocksService(client).trash("block-id")
    # --------------------------------
    def trash(self, block_id: str) -> dict[str, Any]:
        return self._call("blocks.delete", self.client.blocks.delete, block_id=block_id)
