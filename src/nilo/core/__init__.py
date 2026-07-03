# File: src/nilo/core/__init__.py
# Format: UTF-8
# =============================
# File Description:
# Core package exports the shared business layer used by CLI and MCP entrypoints.
# TAG: core, package
# =============================

from .config import CoreConfig, DEFAULT_NOTION_VERSION
from .errors import CoreError

__all__ = ["CoreConfig", "CoreError", "DEFAULT_NOTION_VERSION"]
