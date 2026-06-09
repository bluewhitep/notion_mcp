# File: src/notion_mcp/core/attachments/__init__.py
# Format: UTF-8
# =============================
# File Description:
# Public exports for project-local page/database attachment state.
# TAG: core, attachments
# =============================

from .attachment_store import DatabaseAttachmentStore, PageAttachmentStore
from .context_resolver import ContextResolver
from .database_attachment import AttachedDatabase, AttachedDataSource, DatabaseAttachment, extract_database_title
from .page_attachment import AttachedPage, PageAttachment, build_page_attachment_from_response, extract_page_title

__all__ = [
    "AttachedDatabase",
    "AttachedDataSource",
    "AttachedPage",
    "ContextResolver",
    "DatabaseAttachment",
    "DatabaseAttachmentStore",
    "PageAttachment",
    "PageAttachmentStore",
    "build_page_attachment_from_response",
    "extract_database_title",
    "extract_page_title",
]
