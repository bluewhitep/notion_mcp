# File: src/nilo/core/services/comments.py
# Format: UTF-8
# =============================
# File Description:
# Core service for Notion comment operations.
# TAG: core, services, comments
# =============================

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from .base import BaseNotionService


class CommentsService(BaseNotionService):
    # --------------------------------
    # Function Description:
    # Lists comments for a page or block discussion.
    # Inputs/Outputs:
    # Input raw query params; returns Notion comments list response.
    # Usage:
    # CommentsService(client).list(block_id="block-id")
    # --------------------------------
    def list(self, **params: Any) -> dict[str, Any]:
        return self._call("comments.list", self.client.comments.list, **params)

    # --------------------------------
    # Function Description:
    # Creates a Notion comment.
    # Inputs/Outputs:
    # Input raw payload; returns Notion create response.
    # Usage:
    # CommentsService(client).create({"parent": {}})
    # --------------------------------
    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._call("comments.create", self.client.comments.create, **payload)

    # --------------------------------
    # Function Description:
    # Replies to an existing Notion discussion.
    # Inputs/Outputs:
    # Input discussion id and rich_text list; returns Notion comment create response.
    # Usage:
    # CommentsService(client).reply("discussion-id", [{"type": "text"}])
    # --------------------------------
    def reply(self, discussion_id: str, rich_text: Sequence[dict[str, Any]]) -> dict[str, Any]:
        return self._call(
            "comments.create",
            self.client.comments.create,
            discussion_id=discussion_id,
            rich_text=rich_text,
        )
