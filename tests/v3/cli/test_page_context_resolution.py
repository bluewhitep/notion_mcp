from pathlib import Path

import pytest

from notion_mcp.core.attachments import ContextResolver, PageAttachment, PageAttachmentStore
from notion_mcp.core.errors import PageAttachmentNotFoundError
from notion_mcp.core.project import ProjectConfigStore


def test_page_context_resolver_prefers_explicit_page_id(tmp_path: Path) -> None:
    ProjectConfigStore.init_project(tmp_path)
    attachment = PageAttachment.from_manual(
        page_id="attached-page",
        title="Attached",
        command="test",
    )
    PageAttachmentStore.save(tmp_path, attachment)

    resolved = ContextResolver(project_root=tmp_path).resolve_page_id("explicit-page")

    assert resolved == "explicit-page"


def test_page_context_resolver_uses_attached_page_when_explicit_id_is_missing(tmp_path: Path) -> None:
    ProjectConfigStore.init_project(tmp_path)
    attachment = PageAttachment.from_manual(
        page_id="attached-page",
        title="Attached",
        command="test",
    )
    PageAttachmentStore.save(tmp_path, attachment)

    resolved = ContextResolver(project_root=tmp_path).resolve_page_id()

    assert resolved == "attached-page"


def test_page_context_resolver_errors_when_no_page_is_attached(tmp_path: Path) -> None:
    ProjectConfigStore.init_project(tmp_path)

    with pytest.raises(PageAttachmentNotFoundError) as exc_info:
        ContextResolver(project_root=tmp_path).resolve_page_id()

    assert "No page is attached for this project" in exc_info.value.message
    assert "notion-mcp page retrieve <page_id>" in exc_info.value.message
