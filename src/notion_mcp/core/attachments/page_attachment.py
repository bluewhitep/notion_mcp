# File: src/notion_mcp/core/attachments/page_attachment.py
# Format: UTF-8
# =============================
# File Description:
# Page attachment state models and Notion page response conversion helpers.
# TAG: core, attachments, pages
# =============================

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator

from notion_mcp.core.project.project_config import timestamp_utc


class AttachedPage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str | None = None
    url: str | None = None
    parent: dict[str, Any] | None = None
    archived: bool | None = None
    in_trash: bool | None = None


class AttachmentSource(BaseModel):
    model_config = ConfigDict(extra="forbid")

    created_by: str = "cli"
    command: str


class PageAttachment(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = 1
    kind: str = "page_attach"
    status: str = "attached"
    page: AttachedPage
    attached_at: str
    updated_at: str
    verified_at: str | None = None
    source: AttachmentSource

    # --------------------------------
    # Function Description:
    # Validates page attachment schema version.
    # Inputs/Outputs:
    # Input integer; returns supported value or raises ValueError.
    # Usage:
    # PageAttachment(..., schema_version=1)
    # --------------------------------
    @field_validator("schema_version")
    @classmethod
    def validate_schema_version(cls, value: int) -> int:
        if value != 1:
            raise ValueError("page attachment schema_version must be 1")
        return value

    # --------------------------------
    # Function Description:
    # Builds verified attachment state from a Notion page response.
    # Inputs/Outputs:
    # Input page response and source command; returns PageAttachment.
    # Usage:
    # PageAttachment.from_page_response(page, command="notion-mcp page attach")
    # --------------------------------
    @classmethod
    def from_page_response(
        cls,
        page_response: dict[str, Any],
        *,
        command: str,
        attached_at: str | None = None,
    ) -> "PageAttachment":
        now = timestamp_utc()
        attached = attached_at or now
        page_id = str(page_response.get("id") or "")
        archived = page_response.get("archived")
        in_trash = page_response.get("in_trash")
        if in_trash is None and isinstance(archived, bool):
            in_trash = archived
        return cls(
            page=AttachedPage(
                id=page_id,
                title=extract_page_title(page_response),
                url=_optional_str(page_response.get("url")),
                parent=_optional_dict(page_response.get("parent")),
                archived=archived if isinstance(archived, bool) else None,
                in_trash=in_trash if isinstance(in_trash, bool) else None,
            ),
            attached_at=attached,
            updated_at=now,
            verified_at=now,
            source=AttachmentSource(command=command),
        )

    # --------------------------------
    # Function Description:
    # Builds unverified attachment state from manual page metadata.
    # Inputs/Outputs:
    # Input page id/title and source command; returns PageAttachment.
    # Usage:
    # PageAttachment.from_manual(page_id="page", title="Manual", command="...")
    # --------------------------------
    @classmethod
    def from_manual(
        cls,
        *,
        page_id: str,
        title: str | None = None,
        command: str,
    ) -> "PageAttachment":
        now = timestamp_utc()
        return cls(
            page=AttachedPage(id=page_id, title=title),
            attached_at=now,
            updated_at=now,
            verified_at=None,
            source=AttachmentSource(command=command),
        )

    # --------------------------------
    # Function Description:
    # Returns a refreshed copy while preserving original attachment time.
    # Inputs/Outputs:
    # Input Notion page response and command; returns updated PageAttachment.
    # Usage:
    # attachment.refreshed(page_response, command="notion-mcp page refresh")
    # --------------------------------
    def refreshed(self, page_response: dict[str, Any], *, command: str) -> "PageAttachment":
        return PageAttachment.from_page_response(
            page_response,
            command=command,
            attached_at=self.attached_at,
        )


# --------------------------------
# Function Description:
# Builds verified page attachment state from a Notion page response.
# Inputs/Outputs:
# Input page response and command; returns PageAttachment.
# Usage:
# build_page_attachment_from_response(page, command="notion-mcp page attach")
# --------------------------------
def build_page_attachment_from_response(page_response: dict[str, Any], *, command: str) -> PageAttachment:
    return PageAttachment.from_page_response(page_response, command=command)


# --------------------------------
# Function Description:
# Extracts a readable title from a Notion page response properties object.
# Inputs/Outputs:
# Input page response; returns title text or None.
# Usage:
# extract_page_title(page_response)
# --------------------------------
def extract_page_title(page_response: dict[str, Any]) -> str | None:
    properties = page_response.get("properties")
    if not isinstance(properties, dict):
        return None
    title_values: list[dict[str, Any]] | None = None
    for property_name, property_value in properties.items():
        if not isinstance(property_value, dict):
            continue
        if property_value.get("type") == "title" or property_name == "title":
            raw_title = property_value.get("title")
            if isinstance(raw_title, list):
                title_values = [item for item in raw_title if isinstance(item, dict)]
                break
    if not title_values:
        return None
    parts: list[str] = []
    for item in title_values:
        plain_text = item.get("plain_text")
        if isinstance(plain_text, str):
            parts.append(plain_text)
            continue
        text = item.get("text")
        if isinstance(text, dict) and isinstance(text.get("content"), str):
            parts.append(text["content"])
    title = "".join(parts).strip()
    return title or None


# --------------------------------
# Function Description:
# Returns a value only when it is a string.
# Inputs/Outputs:
# Input arbitrary value; returns string or None.
# Usage:
# _optional_str(page.get("url"))
# --------------------------------
def _optional_str(value: Any) -> str | None:
    return value if isinstance(value, str) else None


# --------------------------------
# Function Description:
# Returns a value only when it is a dictionary.
# Inputs/Outputs:
# Input arbitrary value; returns dict or None.
# Usage:
# _optional_dict(page.get("parent"))
# --------------------------------
def _optional_dict(value: Any) -> dict[str, Any] | None:
    return value if isinstance(value, dict) else None
