# File: src/notion_mcp/core/attachments/database_attachment.py
# Format: UTF-8
# =============================
# File Description:
# Database attachment state models and Notion database response conversion helpers.
# TAG: core, attachments, databases, data-sources
# =============================

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator

from notion_mcp.core.errors import DatabaseDataSourceSelectionError
from notion_mcp.core.project.project_config import timestamp_utc

from .page_attachment import AttachmentSource


class AttachedDatabase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str | None = None
    url: str | None = None
    is_inline: bool | None = None
    archived: bool | None = None
    in_trash: bool | None = None


class AttachedDataSource(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str | None = None
    parent_database_id: str


class DatabaseAttachment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = 1
    kind: str = "database_attach"
    status: str = "attached"
    database: AttachedDatabase
    active_data_source: AttachedDataSource | None = None
    available_data_sources: list[AttachedDataSource] = []
    attached_at: str
    updated_at: str
    verified_at: str | None = None
    source: AttachmentSource

    # --------------------------------
    # Function Description:
    # Validates database attachment schema version.
    # Inputs/Outputs:
    # Input integer; returns supported value or raises ValueError.
    # Usage:
    # DatabaseAttachment(..., schema_version=1)
    # --------------------------------
    @field_validator("schema_version")
    @classmethod
    def validate_schema_version(cls, value: int) -> int:
        if value != 1:
            raise ValueError("database attachment schema_version must be 1")
        return value

    # --------------------------------
    # Function Description:
    # Builds verified attachment state from a Notion database response.
    # Inputs/Outputs:
    # Input database response and optional data source selector; returns DatabaseAttachment.
    # Usage:
    # DatabaseAttachment.from_database_response(database, data_source_selector="Tasks", command="...")
    # --------------------------------
    @classmethod
    def from_database_response(
        cls,
        database_response: dict[str, Any],
        *,
        command: str,
        data_source_selector: str | None = None,
        attached_at: str | None = None,
    ) -> "DatabaseAttachment":
        now = timestamp_utc()
        attached = attached_at or now
        database_id = str(database_response.get("id") or "")
        available_data_sources = extract_data_sources(database_response, database_id)
        active = select_active_data_source(
            database_id,
            available_data_sources,
            data_source_selector=data_source_selector,
        )
        archived = database_response.get("archived")
        in_trash = database_response.get("in_trash")
        if in_trash is None and isinstance(archived, bool):
            in_trash = archived
        return cls(
            database=AttachedDatabase(
                id=database_id,
                title=extract_database_title(database_response),
                url=_optional_str(database_response.get("url")),
                is_inline=_optional_bool(database_response.get("is_inline")),
                archived=archived if isinstance(archived, bool) else None,
                in_trash=in_trash if isinstance(in_trash, bool) else None,
            ),
            active_data_source=active,
            available_data_sources=available_data_sources,
            attached_at=attached,
            updated_at=now,
            verified_at=now,
            source=AttachmentSource(command=command),
        )

    # --------------------------------
    # Function Description:
    # Builds unverified database attachment state from manual metadata.
    # Inputs/Outputs:
    # Input database id/title and command; returns DatabaseAttachment.
    # Usage:
    # DatabaseAttachment.from_manual(database_id="db", title="Manual", command="...")
    # --------------------------------
    @classmethod
    def from_manual(
        cls,
        *,
        database_id: str,
        title: str | None = None,
        command: str,
    ) -> "DatabaseAttachment":
        now = timestamp_utc()
        return cls(
            database=AttachedDatabase(id=database_id, title=title),
            active_data_source=None,
            available_data_sources=[],
            attached_at=now,
            updated_at=now,
            verified_at=None,
            source=AttachmentSource(command=command),
        )

    # --------------------------------
    # Function Description:
    # Returns a refreshed copy while preserving original attachment time.
    # Inputs/Outputs:
    # Input Notion database response; returns refreshed attachment.
    # Usage:
    # attachment.refreshed(database_response, command="notion-mcp database refresh")
    # --------------------------------
    def refreshed(self, database_response: dict[str, Any], *, command: str) -> "DatabaseAttachment":
        selector = self.active_data_source.id if self.active_data_source else None
        return DatabaseAttachment.from_database_response(
            database_response,
            command=command,
            data_source_selector=selector,
            attached_at=self.attached_at,
        )


# --------------------------------
# Function Description:
# Extracts data source attachment records from a Notion database response.
# Inputs/Outputs:
# Input database response and parent database id; returns data source records.
# Usage:
# extract_data_sources(database_response, "database-id")
# --------------------------------
def extract_data_sources(database_response: dict[str, Any], database_id: str) -> list[AttachedDataSource]:
    raw_sources = database_response.get("data_sources", [])
    if not isinstance(raw_sources, list):
        return []
    sources: list[AttachedDataSource] = []
    for raw_source in raw_sources:
        if not isinstance(raw_source, dict):
            continue
        source_id = raw_source.get("id")
        if not isinstance(source_id, str):
            continue
        sources.append(
            AttachedDataSource(
                id=source_id,
                name=_optional_str(raw_source.get("name")) or _optional_str(raw_source.get("title")),
                parent_database_id=database_id,
            )
        )
    return sources


# --------------------------------
# Function Description:
# Selects the active data source for a database attachment.
# Inputs/Outputs:
# Input database id, available sources, optional selector; returns active source or raises CoreError.
# Usage:
# select_active_data_source("db", sources, data_source_selector="Tasks")
# --------------------------------
def select_active_data_source(
    database_id: str,
    sources: list[AttachedDataSource],
    *,
    data_source_selector: str | None = None,
) -> AttachedDataSource | None:
    if data_source_selector:
        for source in sources:
            if source.id == data_source_selector or source.name == data_source_selector:
                return source
        raise DatabaseDataSourceSelectionError(
            database_id,
            sources=[source.model_dump(mode="json", exclude_none=False) for source in sources],
            selector=data_source_selector,
        )
    if len(sources) == 1:
        return sources[0]
    if len(sources) > 1:
        raise DatabaseDataSourceSelectionError(
            database_id,
            sources=[source.model_dump(mode="json", exclude_none=False) for source in sources],
            selector=None,
        )
    return None


# --------------------------------
# Function Description:
# Extracts a readable title from a Notion database response.
# Inputs/Outputs:
# Input database response; returns plain title text or None.
# Usage:
# extract_database_title(database_response)
# --------------------------------
def extract_database_title(database_response: dict[str, Any]) -> str | None:
    title = database_response.get("title")
    if isinstance(title, str):
        return title
    if not isinstance(title, list):
        return None
    parts: list[str] = []
    for item in title:
        if not isinstance(item, dict):
            continue
        plain_text = item.get("plain_text")
        if isinstance(plain_text, str):
            parts.append(plain_text)
            continue
        text = item.get("text")
        if isinstance(text, dict) and isinstance(text.get("content"), str):
            parts.append(text["content"])
    value = "".join(parts).strip()
    return value or None


# --------------------------------
# Function Description:
# Returns a value only when it is a string.
# Inputs/Outputs:
# Input arbitrary value; returns string or None.
# Usage:
# _optional_str(database.get("url"))
# --------------------------------
def _optional_str(value: Any) -> str | None:
    return value if isinstance(value, str) else None


# --------------------------------
# Function Description:
# Returns a value only when it is a bool.
# Inputs/Outputs:
# Input arbitrary value; returns bool or None.
# Usage:
# _optional_bool(database.get("is_inline"))
# --------------------------------
def _optional_bool(value: Any) -> bool | None:
    return value if isinstance(value, bool) else None
