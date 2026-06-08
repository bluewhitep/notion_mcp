# File: src/notion_mcp/core/client.py
# Format: UTF-8
# =============================
# File Description:
# Notion SDK client factory for the Core layer.
# TAG: core, client, notion-sdk
# =============================

from __future__ import annotations

from typing import Any, Callable

try:
    from notion_client import Client as _SDKNotionClient
except ImportError:  # pragma: no cover - package dependency should provide this.
    NotionClient: Callable[..., Any] | None = None
else:
    NotionClient = _SDKNotionClient

from .config import CoreConfig
from .errors import ConfigValidationError


class NotionClientFactory:
    # --------------------------------
    # Function Description:
    # Initializes a client factory with optional test doubles.
    # Inputs/Outputs:
    # Input client class or fake client; output is a reusable factory.
    # Usage:
    # NotionClientFactory(client_cls=FakeClient)
    # --------------------------------
    def __init__(
        self,
        *,
        client_cls: Callable[..., Any] | None = None,
        fake_client: Any | None = None,
    ) -> None:
        self.client_cls = client_cls
        self.fake_client = fake_client

    # --------------------------------
    # Function Description:
    # Creates a Notion SDK client from CoreConfig.
    # Inputs/Outputs:
    # Input CoreConfig; returns SDK client or injected fake client.
    # Usage:
    # factory.create(config)
    # --------------------------------
    def create(self, config: CoreConfig) -> Any:
        if self.fake_client is not None:
            return self.fake_client
        if not config.notion_token:
            raise ConfigValidationError("notion_token is required to create a Notion client")
        client_cls = self.client_cls or NotionClient
        if client_cls is None:
            raise ConfigValidationError("notion-client is not installed")
        return client_cls(
            auth=config.notion_token,
            notion_version=config.notion_version,
            timeout_ms=config.timeout_ms,
            retry=config.retry,
        )


# --------------------------------
# Function Description:
# Creates a Notion client using the default factory.
# Inputs/Outputs:
# Input CoreConfig; returns SDK client.
# Usage:
# create_notion_client(config)
# --------------------------------
def create_notion_client(config: CoreConfig) -> Any:
    return NotionClientFactory().create(config)
