import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from nilo.cli import app
from nilo.cli.commands import pages


runner = CliRunner()


class FakePagesService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def content(self, page_id: str, *, tree: bool = False) -> dict[str, object]:
        self.calls.append(("content", {"page_id": page_id, "tree": tree}))
        return {
            "page": {"id": page_id, "title": "Project Home", "properties": {"Status": {"type": "status"}}},
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


def test_page_content_uses_attached_page_by_default(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = FakePagesService()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(pages, "get_pages_service", lambda: service)
    attach = runner.invoke(app, ["page", "attach", "attached-page", "--no-verify", "--title", "Attached"])
    assert attach.exit_code == 0

    result = runner.invoke(app, ["page", "content", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["page"]["id"] == "attached-page"
    assert payload["blocks"][0]["id"] == "block-1"
    assert service.calls == [("content", {"page_id": "attached-page", "tree": False})]


def test_page_content_explicit_page_id_overrides_attachment(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = FakePagesService()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(pages, "get_pages_service", lambda: service)
    attach = runner.invoke(app, ["page", "attach", "attached-page", "--no-verify", "--title", "Attached"])
    assert attach.exit_code == 0

    result = runner.invoke(app, ["page", "content", "explicit-page", "--tree", "--json"])

    assert result.exit_code == 0
    assert json.loads(result.stdout)["page"]["id"] == "explicit-page"
    assert service.calls == [("content", {"page_id": "explicit-page", "tree": True})]


def test_page_content_human_output_lists_block_ids_and_text(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = FakePagesService()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(pages, "get_pages_service", lambda: service)
    attach = runner.invoke(app, ["page", "attach", "attached-page", "--no-verify", "--title", "Attached"])
    assert attach.exit_code == 0

    result = runner.invoke(app, ["page", "content"])

    assert result.exit_code == 0
    assert "Page: Project Home" in result.stdout
    assert "ID: attached-page" in result.stdout
    assert '1. [paragraph] block_id=block-1 "Intro"' in result.stdout
