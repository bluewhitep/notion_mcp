import json
from pathlib import Path

import pytest

from nilo.core.attachments import PageAttachment, PageAttachmentStore
from nilo.core.errors import PageAttachmentNotFoundError
from nilo.core.project import ProjectConfigStore, ProjectPaths


def test_page_attachment_store_saves_loads_and_deletes_state(tmp_path: Path) -> None:
    ProjectConfigStore.init_project(tmp_path)
    attachment = PageAttachment.from_page_response(
        {
            "id": "page-1",
            "url": "https://www.notion.so/page-1",
            "parent": {"type": "workspace", "workspace": True},
            "archived": False,
            "in_trash": False,
            "properties": {
                "title": {
                    "type": "title",
                    "title": [{"plain_text": "Project Home"}],
                }
            },
        },
        command="nilo page attach",
    )

    PageAttachmentStore.save(tmp_path, attachment)
    state_file = ProjectPaths(tmp_path).page_attachment_file

    assert state_file.exists()
    assert state_file.read_text(encoding="utf-8").endswith("\n")
    raw = json.loads(state_file.read_text(encoding="utf-8"))
    assert raw["schema_version"] == 1
    assert raw["kind"] == "page_attach"
    assert raw["status"] == "attached"
    assert raw["page"]["id"] == "page-1"
    assert raw["page"]["title"] == "Project Home"
    assert "notion_token" not in json.dumps(raw)

    loaded = PageAttachmentStore.load(tmp_path)
    assert loaded.page.id == "page-1"
    assert loaded.page.title == "Project Home"
    assert loaded.verified_at is not None

    PageAttachmentStore.delete(tmp_path)
    assert not state_file.exists()
    with pytest.raises(PageAttachmentNotFoundError):
        PageAttachmentStore.load(tmp_path)


def test_page_attachment_store_no_verify_state_has_limited_metadata(tmp_path: Path) -> None:
    ProjectConfigStore.init_project(tmp_path)
    attachment = PageAttachment.from_manual(
        page_id="page-manual",
        title="Manual Title",
        command="nilo page attach --no-verify",
    )

    PageAttachmentStore.save(tmp_path, attachment)
    loaded = PageAttachmentStore.load(tmp_path)

    assert loaded.page.id == "page-manual"
    assert loaded.page.title == "Manual Title"
    assert loaded.page.url is None
    assert loaded.page.parent is None
    assert loaded.page.archived is None
    assert loaded.page.in_trash is None
    assert loaded.verified_at is None
