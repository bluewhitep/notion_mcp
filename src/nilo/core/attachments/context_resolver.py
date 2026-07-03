# File: src/nilo/core/attachments/context_resolver.py
# Format: UTF-8
# =============================
# File Description:
# Context resolution helpers for explicit ids and project attachment state.
# TAG: core, attachments, context
# =============================

from __future__ import annotations

from pathlib import Path

from nilo.core.errors import ActiveDataSourceNotFoundError
from nilo.core.identifiers import parse_notion_page_id

from .attachment_store import DatabaseAttachmentStore, PageAttachmentStore


class ContextResolver:
    def __init__(self, project_root: Path) -> None:
        self.project_root = Path(project_root).expanduser().resolve()

    # --------------------------------
    # Function Description:
    # Resolves a page id from explicit input or attached page state.
    # Inputs/Outputs:
    # Input optional explicit page id; returns page id or raises PageAttachmentNotFoundError.
    # Usage:
    # ContextResolver(root).resolve_page_id(explicit_page_id)
    # --------------------------------
    def resolve_page_id(self, explicit_page_id: str | None = None) -> str:
        if explicit_page_id:
            return parse_notion_page_id(explicit_page_id)
        return PageAttachmentStore.load(self.project_root).page.id

    # --------------------------------
    # Function Description:
    # Resolves a database id from explicit input or attached database state.
    # Inputs/Outputs:
    # Input optional explicit database id; returns database id or raises DatabaseAttachmentNotFoundError.
    # Usage:
    # ContextResolver(root).resolve_database_id(explicit_database_id)
    # --------------------------------
    def resolve_database_id(self, explicit_database_id: str | None = None) -> str:
        if explicit_database_id:
            return explicit_database_id
        return DatabaseAttachmentStore.load(self.project_root).database.id

    # --------------------------------
    # Function Description:
    # Resolves a data source id from explicit input or attached active data source.
    # Inputs/Outputs:
    # Input optional explicit data source id; returns data source id or raises CoreError.
    # Usage:
    # ContextResolver(root).resolve_data_source_id(explicit_data_source_id)
    # --------------------------------
    def resolve_data_source_id(self, explicit_data_source_id: str | None = None) -> str:
        if explicit_data_source_id:
            return explicit_data_source_id
        attachment = DatabaseAttachmentStore.load(self.project_root)
        if attachment.active_data_source is None:
            raise ActiveDataSourceNotFoundError(str(self.project_root), attachment.database.id)
        return attachment.active_data_source.id
