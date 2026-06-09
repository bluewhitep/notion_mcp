"""
notion_mcp
===============

This package implements the local Notion MCP service, including configuration
management, FastAPI service setup, CLI commands, and route modules.

Module overview:

- `config`: Reads and saves global configuration.
- `models`: Contains Pydantic models for validation.
- `routes`: Provides domain-specific FastAPI routes.
- `server`: Builds the FastAPI application and registers routes.
- `cli`: Provides the command-line entry point.

"""

from importlib import metadata

try:
    __version__ = metadata.version(__name__)
except metadata.PackageNotFoundError:
    # Package is not installed; fallback for local development
    __version__ = "0.0.0"

__all__ = ["__version__"]
