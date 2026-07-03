# File: tests/live/test_live_content_consistency_e2e.py
# Format: UTF-8
# =============================
# File Description:
# Live Notion create/read/update/delete consistency tests for page, block, and data source entry workflows.
# TAG: tests, live, e2e, notion, content-consistency
# =============================

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any, Callable
from uuid import uuid4

import pytest

from nilo.core.attachments import DatabaseAttachmentStore, PageAttachmentStore
from nilo.core.client import create_notion_client
from nilo.core.config import CoreConfig, load_core_config
from nilo.core.errors import CoreError
from nilo.core.project import ProjectResolver
from nilo.core.services.blocks import BlocksService
from nilo.core.services.data_sources import DataSourcesService
from nilo.core.services.pages import PagesService
from nilo.core.services.pages import extract_block_text


pytestmark = pytest.mark.live


# --------------------------------
# Function Description:
# Skips unless destructive live E2E checks were explicitly requested.
# Inputs/Outputs:
# No input; skips test process unless NOTION_MCP_LIVE_E2E=1.
# Usage:
# _require_live_e2e()
# --------------------------------
def _require_live_e2e() -> None:
    if os.getenv("NOTION_MCP_LIVE_E2E") != "1":
        pytest.skip("Set NOTION_MCP_LIVE_E2E=1 to run live create/update/trash content consistency tests")


# --------------------------------
# Function Description:
# Loads configured Notion credentials from global config or explicit environment variables.
# Inputs/Outputs:
# No input; returns CoreConfig or skips when no token is available.
# Usage:
# config = _load_live_config()
# --------------------------------
def _load_live_config() -> CoreConfig:
    try:
        return load_core_config()
    except CoreError:
        token = os.getenv("NOTION_MCP_TOKEN")
        if not token:
            pytest.skip("No global Notion MCP config or NOTION_MCP_TOKEN available for live E2E")
        return CoreConfig(
            notion_token=token,
            user_id=os.getenv("NOTION_MCP_USER_ID") or None,
        )


# --------------------------------
# Function Description:
# Resolves the dedicated live parent page from env or project page attachment state.
# Inputs/Outputs:
# No input; returns page id or skips when unavailable.
# Usage:
# parent_page_id = _resolve_parent_page_id()
# --------------------------------
def _resolve_parent_page_id() -> str:
    explicit = os.getenv("NOTION_MCP_LIVE_PARENT_PAGE_ID")
    if explicit:
        return explicit
    try:
        project_root = ProjectResolver.find_project_root(Path.cwd())
        return PageAttachmentStore.load(project_root).page.id
    except CoreError:
        pytest.skip("Set NOTION_MCP_LIVE_PARENT_PAGE_ID or attach a project page before running live E2E")


# --------------------------------
# Function Description:
# Resolves the live data source id from env or project database attachment state.
# Inputs/Outputs:
# No input; returns data source id or skips when unavailable.
# Usage:
# data_source_id = _resolve_data_source_id()
# --------------------------------
def _resolve_data_source_id() -> str:
    explicit = os.getenv("NOTION_MCP_LIVE_DATA_SOURCE_ID")
    if explicit:
        return explicit
    try:
        project_root = ProjectResolver.find_project_root(Path.cwd())
        attachment = DatabaseAttachmentStore.load(project_root)
    except CoreError:
        pytest.skip("Set NOTION_MCP_LIVE_DATA_SOURCE_ID or attach a project database before running live E2E")
    if attachment.active_data_source is None:
        pytest.skip("Attached database has no active data source for live E2E")
    return attachment.active_data_source.id


# --------------------------------
# Function Description:
# Creates Core services backed by the configured live Notion SDK client.
# Inputs/Outputs:
# No input; returns page, block, and data source services.
# Usage:
# pages, blocks, data_sources = _live_services()
# --------------------------------
def _live_services() -> tuple[PagesService, BlocksService, DataSourcesService]:
    client = create_notion_client(_load_live_config())
    return PagesService(client), BlocksService(client), DataSourcesService(client)


# --------------------------------
# Function Description:
# Builds a plain-text rich text payload.
# Inputs/Outputs:
# Input text; returns Notion rich_text list.
# Usage:
# _rich_text("hello")
# --------------------------------
def _rich_text(text: str) -> list[dict[str, Any]]:
    return [{"type": "text", "text": {"content": text}}]


# --------------------------------
# Function Description:
# Builds a paragraph block payload.
# Inputs/Outputs:
# Input text; returns Notion paragraph block payload.
# Usage:
# _paragraph("body")
# --------------------------------
def _paragraph(text: str) -> dict[str, Any]:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": _rich_text(text)},
    }


# --------------------------------
# Function Description:
# Extracts readable title text from a page property object.
# Inputs/Outputs:
# Input page response and title property name; returns plain text.
# Usage:
# _page_title_text(page, "Name")
# --------------------------------
def _page_title_text(page: dict[str, Any], property_name: str) -> str:
    properties = page.get("properties", {})
    if not isinstance(properties, dict):
        return ""
    prop = properties.get(property_name, {})
    if not isinstance(prop, dict):
        return ""
    title_items = prop.get("title", [])
    if not isinstance(title_items, list):
        return ""
    return "".join(_plain_text(item) for item in title_items if isinstance(item, dict))


# --------------------------------
# Function Description:
# Finds the title property name on a page response.
# Inputs/Outputs:
# Input page response; returns property name or skips when missing.
# Usage:
# title_property = _title_property_name(page)
# --------------------------------
def _title_property_name(page: dict[str, Any]) -> str:
    properties = page.get("properties", {})
    if not isinstance(properties, dict):
        pytest.fail("page response has no properties object")
    for name, prop in properties.items():
        if isinstance(name, str) and isinstance(prop, dict) and prop.get("type") == "title":
            return name
    pytest.fail("page response has no title property")


# --------------------------------
# Function Description:
# Finds the title property name on a data source schema response.
# Inputs/Outputs:
# Input data source response; returns title property name or skips when missing.
# Usage:
# title_property = _data_source_title_property_name(data_source)
# --------------------------------
def _data_source_title_property_name(data_source: dict[str, Any]) -> str:
    properties = data_source.get("properties", {})
    if not isinstance(properties, dict):
        pytest.fail("data source response has no properties object")
    for name, prop in properties.items():
        if isinstance(name, str) and isinstance(prop, dict) and prop.get("type") == "title":
            return name
    pytest.fail("data source schema has no title property")


# --------------------------------
# Function Description:
# Extracts plain text from a rich text object.
# Inputs/Outputs:
# Input rich text object; returns plain text content.
# Usage:
# _plain_text({"plain_text": "hello"})
# --------------------------------
def _plain_text(item: dict[str, Any]) -> str:
    plain_text = item.get("plain_text")
    if isinstance(plain_text, str):
        return plain_text
    text = item.get("text")
    if isinstance(text, dict) and isinstance(text.get("content"), str):
        return text["content"]
    return ""


# --------------------------------
# Function Description:
# Returns the text summaries from page content blocks.
# Inputs/Outputs:
# Input PagesService.content response; returns block text list.
# Usage:
# _content_block_texts(content)
# --------------------------------
def _content_block_texts(content: dict[str, Any]) -> list[str]:
    blocks = content.get("blocks", [])
    if not isinstance(blocks, list):
        return []
    return [str(block.get("text", "")) for block in blocks if isinstance(block, dict)]


# --------------------------------
# Function Description:
# Finds a block id in a page content response by exact text.
# Inputs/Outputs:
# Input content response and text; returns block id or fails.
# Usage:
# block_id = _block_id_with_text(content, "body")
# --------------------------------
def _block_id_with_text(content: dict[str, Any], text: str) -> str:
    blocks = content.get("blocks", [])
    if isinstance(blocks, list):
        for block in blocks:
            if isinstance(block, dict) and block.get("text") == text and isinstance(block.get("id"), str):
                return block["id"]
    pytest.fail(f"Could not find block with text: {text}")


# --------------------------------
# Function Description:
# Checks if a listed block response contains a specific block id.
# Inputs/Outputs:
# Input block children response and block id; returns boolean.
# Usage:
# _children_contain_block(children, block_id)
# --------------------------------
def _children_contain_block(children: dict[str, Any], block_id: str) -> bool:
    results = children.get("results", [])
    return isinstance(results, list) and any(isinstance(item, dict) and item.get("id") == block_id for item in results)


# --------------------------------
# Function Description:
# Retries a condition until it becomes true or times out.
# Inputs/Outputs:
# Input predicate and timeout settings; fails when condition stays false.
# Usage:
# _eventually(lambda: condition)
# --------------------------------
def _eventually(predicate: Callable[[], bool], *, timeout_seconds: float = 10.0, interval_seconds: float = 1.0) -> None:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if predicate():
            return
        time.sleep(interval_seconds)
    assert predicate()


# --------------------------------
# Function Description:
# Safely trashes a page during live test cleanup.
# Inputs/Outputs:
# Input PagesService and optional page id; output is None.
# Usage:
# _safe_trash_page(pages, page_id)
# --------------------------------
def _safe_trash_page(pages: PagesService, page_id: str | None) -> None:
    if not page_id:
        return
    try:
        pages.trash(page_id)
    except CoreError:
        return


# --------------------------------
# Function Description:
# Safely trashes a block during live test cleanup.
# Inputs/Outputs:
# Input BlocksService and optional block id; output is None.
# Usage:
# _safe_trash_block(blocks, block_id)
# --------------------------------
def _safe_trash_block(blocks: BlocksService, block_id: str | None) -> None:
    if not block_id:
        return
    try:
        blocks.trash(block_id)
    except CoreError:
        return


# --------------------------------
# Function Description:
# Verifies page creation, child content readback, update readback, and trash state.
# Inputs/Outputs:
# No input; performs live Notion mutations on the configured dedicated test page.
# Usage:
# pytest tests/live/test_live_content_consistency_e2e.py -m live
# --------------------------------
def test_live_page_and_child_content_create_read_update_trash_consistency() -> None:
    _require_live_e2e()
    parent_page_id = _resolve_parent_page_id()
    pages, blocks, _ = _live_services()
    suffix = uuid4().hex[:8]
    original_title = f"Live E2E page {suffix}"
    updated_title = f"Live E2E page updated {suffix}"
    original_body = f"Live E2E page body {suffix}"
    updated_body = f"Live E2E page body updated {suffix}"
    created_page_id: str | None = None

    try:
        created = pages.create(
            {
                "parent": {"type": "page_id", "page_id": parent_page_id},
                "properties": {"title": {"title": _rich_text(original_title)}},
                "children": [_paragraph(original_body)],
            }
        )
        created_page_id = str(created["id"])

        content = pages.content(created_page_id)
        assert content["page"]["title"] == original_title
        assert original_body in _content_block_texts(content)

        retrieved_page = pages.retrieve(created_page_id)
        title_property = _title_property_name(retrieved_page)
        block_id = _block_id_with_text(content, original_body)
        pages.update(created_page_id, {"properties": {title_property: {"title": _rich_text(updated_title)}}})
        blocks.update(block_id, {"paragraph": {"rich_text": _rich_text(updated_body)}})

        updated_content = pages.content(created_page_id)
        assert updated_content["page"]["title"] == updated_title
        assert updated_body in _content_block_texts(updated_content)
        assert original_body not in _content_block_texts(updated_content)

        trashed = pages.trash(created_page_id)
        assert trashed.get("in_trash") is True
        assert pages.retrieve(created_page_id).get("in_trash") is True
        created_page_id = None
    finally:
        _safe_trash_page(pages, created_page_id)


# --------------------------------
# Function Description:
# Verifies block append/list/retrieve/update/list/trash consistency.
# Inputs/Outputs:
# No input; performs live Notion block mutations on the configured dedicated test page.
# Usage:
# pytest tests/live/test_live_content_consistency_e2e.py -m live
# --------------------------------
def test_live_block_create_read_update_trash_consistency() -> None:
    _require_live_e2e()
    parent_page_id = _resolve_parent_page_id()
    _, blocks, _ = _live_services()
    suffix = uuid4().hex[:8]
    original_text = f"Live E2E block {suffix}"
    updated_text = f"Live E2E block updated {suffix}"
    created_block_id: str | None = None

    try:
        created = blocks.append_children(parent_page_id, children=[_paragraph(original_text)])
        results = created.get("results", [])
        assert isinstance(results, list) and results
        created_block = results[0]
        assert isinstance(created_block, dict)
        created_block_id = str(created_block["id"])
        assert extract_block_text(created_block, "paragraph") == original_text

        children = blocks.list_children(parent_page_id, page_size=100)
        assert _children_contain_block(children, created_block_id)

        blocks.update(created_block_id, {"paragraph": {"rich_text": _rich_text(updated_text)}})
        retrieved = blocks.retrieve(created_block_id)
        assert extract_block_text(retrieved, "paragraph") == updated_text

        blocks.trash(created_block_id)
        _eventually(lambda: not _children_contain_block(blocks.list_children(parent_page_id, page_size=100), created_block_id))
        created_block_id = None
    finally:
        _safe_trash_block(blocks, created_block_id)


# --------------------------------
# Function Description:
# Verifies data source entry create/query/retrieve/update/query/trash consistency.
# Inputs/Outputs:
# No input; performs live Notion data source entry mutations on the configured data source.
# Usage:
# pytest tests/live/test_live_content_consistency_e2e.py -m live
# --------------------------------
def test_live_data_source_entry_create_read_update_trash_consistency() -> None:
    _require_live_e2e()
    data_source_id = _resolve_data_source_id()
    pages, _, data_sources = _live_services()
    data_source = data_sources.retrieve(data_source_id)
    title_property = _data_source_title_property_name(data_source)
    suffix = uuid4().hex[:8]
    original_title = f"Live E2E entry {suffix}"
    updated_title = f"Live E2E entry updated {suffix}"
    created_page_id: str | None = None

    try:
        created = pages.create(
            {
                "parent": {"type": "data_source_id", "data_source_id": data_source_id},
                "properties": {title_property: {"title": _rich_text(original_title)}},
            }
        )
        created_page_id = str(created["id"])

        retrieved = pages.retrieve(created_page_id)
        assert _page_title_text(retrieved, title_property) == original_title
        original_query = data_sources.query(
            data_source_id,
            {"filter": {"property": title_property, "title": {"equals": original_title}}, "page_size": 10},
        )
        assert _query_contains_page(original_query, created_page_id)

        pages.update(created_page_id, {"properties": {title_property: {"title": _rich_text(updated_title)}}})
        updated = pages.retrieve(created_page_id)
        assert _page_title_text(updated, title_property) == updated_title
        updated_query = data_sources.query(
            data_source_id,
            {"filter": {"property": title_property, "title": {"equals": updated_title}}, "page_size": 10},
        )
        assert _query_contains_page(updated_query, created_page_id)

        trashed = pages.trash(created_page_id)
        assert trashed.get("in_trash") is True
        assert pages.retrieve(created_page_id).get("in_trash") is True
        created_page_id = None
    finally:
        _safe_trash_page(pages, created_page_id)


# --------------------------------
# Function Description:
# Checks whether a data source query result includes a page id.
# Inputs/Outputs:
# Input query response and page id; returns boolean.
# Usage:
# _query_contains_page(query, page_id)
# --------------------------------
def _query_contains_page(query: dict[str, Any], page_id: str) -> bool:
    results = query.get("results", [])
    return isinstance(results, list) and any(isinstance(item, dict) and item.get("id") == page_id for item in results)
