"""
FastAPI dependency definitions.

This module keeps configuration loading and Notion client initialization
separate to avoid circular imports.
"""

from __future__ import annotations

from fastapi import Depends, HTTPException
from typing import Any

from .config import load_config
from .models import Config

try:
    from notion_client import Client as NotionClient  # type: ignore
except ImportError:
    NotionClient = Any  # type: ignore


def get_config() -> Config:
    """Load and return the current configuration.

    Raises HTTP 500 when the configuration file or Notion token is missing.
    """
    try:
        config = load_config()
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Global configuration file does not exist. Run: notion-mcp config --global user.token <token>",
        )
    if not config.notion_token:
        raise HTTPException(
            status_code=500,
            detail="Notion token is not set. Run: notion-mcp config --global user.token <token>",
        )
    return config


def get_notion_client(config: Config = Depends(get_config)) -> NotionClient:
    """Initialize and return a Notion client from configuration."""
    return NotionClient(auth=config.notion_token)  # type: ignore
