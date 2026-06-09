import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from notion_mcp.cli import app
from notion_mcp.cli.commands import pages


runner = CliRunner()


class FakePagesService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def content(self, page_id: str, *, tree: bool = False) -> dict[str, object]:
        self.calls.append(("content", {"page_id": page_id, "tree": tree}))
        return {
            "page": {"id": page_id, "title": "Attached Home", "properties": {}},
            "blocks": [
                {
                    "id": "block-1",
                    "type": "paragraph",
                    "text": "Intro",
                    "parent_id": page_id,
                    "has_children": False,
                    "children": [],
                }
            ],
        }


def test_attach_page_status_content_from_child_and_detach(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = FakePagesService()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(pages, "get_pages_service", lambda: service)

    attach = runner.invoke(app, ["page", "attach", "page-1", "--no-verify", "--title", "Attached Home", "--json"])
    status = runner.invoke(app, ["page", "status", "--json"])

    child = tmp_path / "src" / "module"
    child.mkdir(parents=True)
    monkeypatch.chdir(child)
    content = runner.invoke(app, ["page", "content", "--json"])
    detach = runner.invoke(app, ["page", "detach", "--json"])
    missing = runner.invoke(app, ["page", "content"])

    assert attach.exit_code == 0
    assert status.exit_code == 0
    assert json.loads(status.stdout)["attachment"]["page"]["id"] == "page-1"
    assert content.exit_code == 0
    assert json.loads(content.stdout)["page"]["id"] == "page-1"
    assert service.calls == [("content", {"page_id": "page-1", "tree": False})]
    assert detach.exit_code == 0
    assert missing.exit_code == 1
    assert "No page is attached for this project" in missing.stdout
    assert not (tmp_path / ".notion_mcp" / "state" / "page.attach.json").exists()
