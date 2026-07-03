"""
Configuration management module.

Provides functions for reading and writing the global configuration file,
including Notion integration token and user UUID fields. The default file is
``~/.notion_mcp/config.json`` and can be overridden with ``NOTION_MCP_CONFIG``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from .models import Config


# Default configuration directory and file name.
DEFAULT_CONFIG_DIR = Path.home() / ".notion_mcp"
DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / "config.json"


def get_config_path() -> Path:
    """Return the configuration file path.

    Uses ``NOTION_MCP_CONFIG`` when set; otherwise uses the default path.
    """
    from os import getenv

    env_path = getenv("NOTION_MCP_CONFIG")
    if env_path:
        return Path(env_path).expanduser()
    return DEFAULT_CONFIG_FILE


def load_config(path: Optional[Path] = None) -> Config:
    """Load the configuration file and return a ``Config`` instance.

    Args:
        path: Configuration file path, defaulting to ``get_config_path()``.

    Returns:
        ``Config``: Parsed configuration object.

    Raises:
        FileNotFoundError: Raised when the configuration file does not exist.
        json.JSONDecodeError: Raised when the configuration file is not valid JSON.
    """
    cfg_path = path or get_config_path()
    if not cfg_path.exists():
        raise FileNotFoundError(f"Configuration file does not exist: {cfg_path}")
    with cfg_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return Config.model_validate(data)


def save_config(config: Config, path: Optional[Path] = None) -> None:
    """Serialize a ``Config`` object to the target path.

    Creates the parent directory when needed.

    Args:
        config: Configuration object to save.
        path: Destination path, defaulting to ``get_config_path()``.
    """
    cfg_path = path or get_config_path()
    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    data = config.model_dump(exclude_none=True)
    with cfg_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def set_token(token: str, path: Optional[Path] = None) -> None:
    """Update the Notion token in configuration.

    Creates a new configuration object when the file does not exist.
    """
    try:
        cfg = load_config(path)
    except FileNotFoundError:
        cfg = Config()
    cfg.notion_token = token
    save_config(cfg, path)


def set_user(user_id: str, path: Optional[Path] = None) -> None:
    """Update the current user UUID in configuration.

    Creates a new configuration object when the file does not exist.
    """
    try:
        cfg = load_config(path)
    except FileNotFoundError:
        cfg = Config()
    cfg.user_id = user_id
    save_config(cfg, path)
