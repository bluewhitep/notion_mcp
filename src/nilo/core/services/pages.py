# File: src/nilo/core/services/pages.py
# Format: UTF-8
# =============================
# File Description:
# Core service for Notion page operations.
# TAG: core, services, pages
# =============================

from __future__ import annotations

from typing import Any

from nilo.core.attachments import extract_page_title
from nilo.core.identifiers import parse_notion_page_id

from .base import BaseNotionService
from .blocks import BlocksService


class PagesService(BaseNotionService):
    # --------------------------------
    # Function Description:
    # Retrieves a Notion page.
    # Inputs/Outputs:
    # Input page_id; returns Notion page response.
    # Usage:
    # PagesService(client).retrieve("page-id")
    # --------------------------------
    def retrieve(self, page_id: str) -> dict[str, Any]:
        resolved_page_id = parse_notion_page_id(page_id)
        return self._call("pages.retrieve", self.client.pages.retrieve, page_id=resolved_page_id)

    # --------------------------------
    # Function Description:
    # Retrieves page metadata and summarizes child blocks.
    # Inputs/Outputs:
    # Input page_id and tree flag; returns stable page/content dictionary.
    # Usage:
    # PagesService(client).content("page-id", tree=True)
    # --------------------------------
    def content(self, page_id: str, *, tree: bool = False) -> dict[str, Any]:
        resolved_page_id = parse_notion_page_id(page_id)
        page = self.retrieve(resolved_page_id)
        blocks = self._summarize_children(resolved_page_id, tree=tree)
        return {
            "page": {
                "id": page.get("id", resolved_page_id),
                "title": extract_page_title(page),
                "properties": page.get("properties", {}),
            },
            "blocks": blocks,
        }

    # --------------------------------
    # Function Description:
    # Retrieves a Notion page property item with optional pagination.
    # Inputs/Outputs:
    # Input page_id, property_id, and paging params; returns property item response.
    # Usage:
    # PagesService(client).retrieve_property_item("page-id", "property-id", page_size=25)
    # --------------------------------
    def retrieve_property_item(
        self,
        page_id: str,
        property_id: str,
        **params: Any,
    ) -> dict[str, Any]:
        resolved_page_id = parse_notion_page_id(page_id)
        return self._call(
            "pages.properties.retrieve",
            self.client.pages.properties.retrieve,
            page_id=resolved_page_id,
            property_id=property_id,
            **params,
        )

    # --------------------------------
    # Function Description:
    # Creates a Notion page from a raw SDK payload.
    # Inputs/Outputs:
    # Input payload dictionary; returns Notion create response.
    # Usage:
    # PagesService(client).create({"parent": {"page_id": "root"}})
    # --------------------------------
    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._call("pages.create", self.client.pages.create, **payload)

    # --------------------------------
    # Function Description:
    # Updates a Notion page from a raw SDK payload.
    # Inputs/Outputs:
    # Input page_id and payload; returns Notion update response.
    # Usage:
    # PagesService(client).update("page-id", {"properties": {}})
    # --------------------------------
    def update(self, page_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        resolved_page_id = parse_notion_page_id(page_id)
        return self._call("pages.update", self.client.pages.update, page_id=resolved_page_id, **payload)

    # --------------------------------
    # Function Description:
    # Moves a Notion page to trash using the 2026 in_trash field.
    # Inputs/Outputs:
    # Input page_id; returns Notion update response.
    # Usage:
    # PagesService(client).trash("page-id")
    # --------------------------------
    def trash(self, page_id: str) -> dict[str, Any]:
        return self.update(page_id, {"in_trash": True})

    # --------------------------------
    # Function Description:
    # Summarizes direct child blocks and optionally recurses into nested children.
    # Inputs/Outputs:
    # Input parent block/page id and tree flag; returns block summary list.
    # Usage:
    # self._summarize_children("page-id", tree=True)
    # --------------------------------
    def _summarize_children(self, block_id: str, *, tree: bool) -> list[dict[str, Any]]:
        children_response = BlocksService(self.client).list_children(block_id)
        results = children_response.get("results", [])
        blocks = results if isinstance(results, list) else []
        summaries: list[dict[str, Any]] = []
        for block in blocks:
            if not isinstance(block, dict):
                continue
            summary = summarize_block(block)
            if tree and summary["has_children"]:
                summary["children"] = self._summarize_children(str(summary["id"]), tree=True)
            summaries.append(summary)
        return summaries


# --------------------------------
# Function Description:
# Converts a Notion block response to a stable page content summary.
# Inputs/Outputs:
# Input block dictionary; returns id/type/text/parent-child summary.
# Usage:
# summarize_block(block)
# --------------------------------
def summarize_block(block: dict[str, Any]) -> dict[str, Any]:
    block_type = block.get("type")
    block_type_text = block_type if isinstance(block_type, str) else "unsupported"
    return {
        "id": str(block.get("id", "")),
        "type": block_type_text,
        "text": extract_block_text(block, block_type_text),
        "parent_id": extract_parent_id(block.get("parent")),
        "has_children": bool(block.get("has_children")),
        "children": [],
    }


# --------------------------------
# Function Description:
# Extracts a readable parent id from a Notion parent object.
# Inputs/Outputs:
# Input parent object; returns id string or None.
# Usage:
# extract_parent_id(block.get("parent"))
# --------------------------------
def extract_parent_id(parent: Any) -> str | None:
    if not isinstance(parent, dict):
        return None
    parent_type = parent.get("type")
    if isinstance(parent_type, str):
        value = parent.get(parent_type)
        if isinstance(value, str):
            return value
    for key in ("page_id", "block_id", "data_source_id", "database_id"):
        value = parent.get(key)
        if isinstance(value, str):
            return value
    return None


# --------------------------------
# Function Description:
# Extracts readable text from supported rich-text-bearing block types.
# Inputs/Outputs:
# Input block dictionary and block type; returns plain text summary.
# Usage:
# extract_block_text(block, "paragraph")
# --------------------------------
def extract_block_text(block: dict[str, Any], block_type: str) -> str:
    value = block.get(block_type)
    if isinstance(value, dict):
        if isinstance(value.get("title"), str):
            return value["title"]
        rich_text = value.get("rich_text")
        if isinstance(rich_text, list):
            return "".join(_rich_text_plain_text(item) for item in rich_text if isinstance(item, dict)).strip()
        text = value.get("text")
        if isinstance(text, list):
            return "".join(_rich_text_plain_text(item) for item in text if isinstance(item, dict)).strip()
    return ""


# --------------------------------
# Function Description:
# Extracts plain text from a Notion rich text item.
# Inputs/Outputs:
# Input rich text object; returns plain text fallback.
# Usage:
# _rich_text_plain_text(item)
# --------------------------------
def _rich_text_plain_text(item: dict[str, Any]) -> str:
    plain_text = item.get("plain_text")
    if isinstance(plain_text, str):
        return plain_text
    text = item.get("text")
    if isinstance(text, dict) and isinstance(text.get("content"), str):
        return text["content"]
    return ""
