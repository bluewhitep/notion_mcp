# File: src/nilo/core/services/raw_api.py
# Format: UTF-8
# =============================
# File Description:
# Registered raw Notion SDK operation invoker for broad API coverage.
# TAG: core, services, raw-api, notion-sdk
# =============================

from __future__ import annotations

from typing import Any

from .base import BaseNotionService
from ..errors import NotionOperationError

OPERATION_REGISTRY: dict[str, tuple[str, ...]] = {
    "blocks.retrieve": ("blocks", "retrieve"),
    "blocks.update": ("blocks", "update"),
    "blocks.delete": ("blocks", "delete"),
    "blocks.children.list": ("blocks", "children", "list"),
    "blocks.children.append": ("blocks", "children", "append"),
    "pages.retrieve": ("pages", "retrieve"),
    "pages.create": ("pages", "create"),
    "pages.update": ("pages", "update"),
    "pages.properties.retrieve": ("pages", "properties", "retrieve"),
    "databases.retrieve": ("databases", "retrieve"),
    "databases.create": ("databases", "create"),
    "databases.update": ("databases", "update"),
    "databases.query": ("databases", "query"),
    "data_sources.retrieve": ("data_sources", "retrieve"),
    "data_sources.create": ("data_sources", "create"),
    "data_sources.update": ("data_sources", "update"),
    "data_sources.query": ("data_sources", "query"),
    "users.list": ("users", "list"),
    "users.retrieve": ("users", "retrieve"),
    "users.me": ("users", "me"),
    "comments.list": ("comments", "list"),
    "comments.create": ("comments", "create"),
    "views.list": ("views", "list"),
    "views.retrieve": ("views", "retrieve"),
    "views.create": ("views", "create"),
    "views.update": ("views", "update"),
    "views.query": ("views", "query"),
    "file_uploads.list": ("file_uploads", "list"),
    "file_uploads.create": ("file_uploads", "create"),
    "file_uploads.retrieve": ("file_uploads", "retrieve"),
    "file_uploads.send": ("file_uploads", "send"),
    "file_uploads.complete": ("file_uploads", "complete"),
    "search": ("search",),
    "custom_emojis.list": ("custom_emojis", "list"),
    "custom_emojis.retrieve": ("custom_emojis", "retrieve"),
}


# --------------------------------
# Function Description:
# Lists registered raw Notion SDK operations.
# Inputs/Outputs:
# No input; returns a sorted tuple of operation names.
# Usage:
# registered_operations()
# --------------------------------
def registered_operations() -> tuple[str, ...]:
    return tuple(sorted(OPERATION_REGISTRY))


class RawNotionService(BaseNotionService):
    # --------------------------------
    # Function Description:
    # Invokes a registered Notion SDK operation with raw keyword arguments.
    # Inputs/Outputs:
    # Input operation name and argument dict; returns SDK response or raises Core error.
    # Usage:
    # RawNotionService(client).invoke("pages.retrieve", {"page_id": "id"})
    # --------------------------------
    def invoke(self, operation: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        if operation not in OPERATION_REGISTRY:
            raise NotionOperationError(operation, "Operation is not registered")
        arguments = arguments or {}
        if operation == "custom_emojis.retrieve":
            from .custom_emojis import CustomEmojisService

            custom_emoji_id = arguments.get("custom_emoji_id")
            if not isinstance(custom_emoji_id, str) or not custom_emoji_id:
                raise NotionOperationError(operation, "custom_emoji_id is required")
            return CustomEmojisService(self.client).retrieve(custom_emoji_id)
        if operation == "views.query":
            from .views import ViewsService

            view_id = arguments.get("view_id")
            if not isinstance(view_id, str) or not view_id:
                raise NotionOperationError(operation, "view_id is required")
            payload = {key: value for key, value in arguments.items() if key != "view_id"}
            return ViewsService(self.client).query(view_id, payload)
        path = OPERATION_REGISTRY[operation]
        if any(part.startswith("_") for part in path):
            raise NotionOperationError(operation, "Private SDK attributes are not allowed")
        target = self._resolve_path(operation, path)
        if not callable(target):
            raise NotionOperationError(operation, "Registered operation is not callable")
        return self._call(operation, target, **arguments)

    # --------------------------------
    # Function Description:
    # Resolves a registered SDK attribute path.
    # Inputs/Outputs:
    # Input operation label and path parts; returns the resolved object.
    # Usage:
    # self._resolve_path("pages.retrieve", ("pages", "retrieve"))
    # --------------------------------
    def _resolve_path(self, operation: str, path: tuple[str, ...]) -> Any:
        target: Any = self.client
        try:
            for part in path:
                target = getattr(target, part)
        except AttributeError as exc:
            raise NotionOperationError(
                operation,
                "Registered operation is unavailable on the current SDK client",
            ) from exc
        return target
