"""
路由包。按功能拆分的 API 路由在此集中导入，供主应用注册。
"""

from . import databases, pages, blocks  # noqa: F401

__all__ = ["databases", "pages", "blocks"]