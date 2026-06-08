# File: src/notion_mcp/core/services/base.py
# Format: UTF-8
# =============================
# File Description:
# Shared service base helpers for Notion SDK operation wrappers.
# TAG: core, services, base
# =============================

from __future__ import annotations

from typing import Any, Callable

from ..errors import NotionOperationError


class BaseNotionService:
    # --------------------------------
    # Function Description:
    # Initializes a Core service with a Notion SDK-compatible client.
    # Inputs/Outputs:
    # Input client; output is a service instance.
    # Usage:
    # BaseNotionService(client)
    # --------------------------------
    def __init__(self, client: Any) -> None:
        self.client = client

    # --------------------------------
    # Function Description:
    # Calls a Notion SDK function and normalizes failures.
    # Inputs/Outputs:
    # Input operation label, callable, and keyword arguments; returns SDK response.
    # Usage:
    # self._call("pages.retrieve", self.client.pages.retrieve, page_id="id")
    # --------------------------------
    def _call(
        self,
        operation: str,
        func: Callable[..., dict[str, Any]],
        **kwargs: Any,
    ) -> dict[str, Any]:
        try:
            return func(**kwargs)
        except NotionOperationError:
            raise
        except Exception as exc:
            raise NotionOperationError(operation, str(exc)) from exc
