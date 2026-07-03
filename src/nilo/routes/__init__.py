"""
Route package. Domain-specific API routes are imported here for registration by
the main application.
"""

from . import databases, pages, blocks  # noqa: F401

__all__ = ["databases", "pages", "blocks"]
