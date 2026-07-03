import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from nilo.cli import app
from nilo.cli.commands import pages


runner = CliRunner()


class RefreshPagesService:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def retrieve(self, page_id: str) -> dict[str, object]:
        self.calls.append(page_id)
        return {
            "id": page_id,
            "url": f"https://www.notion.so/{page_id}-refreshed",
            "parent": {"type": "page_id", "page_id": "parent-page"},
            "archived": False,
            "in_trash": True,
            "properties": {
                "title": {
                    "type": "title",
                    "title": [{"plain_text": "Refreshed Title"}],
                }
            },
        }


def test_page_status_outputs_attachment_from_child_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    attach = runner.invoke(app, ["page", "attach", "page-1", "--no-verify", "--title", "Manual"])
    assert attach.exit_code == 0
    child = tmp_path / "nested" / "child"
    child.mkdir(parents=True)
    monkeypatch.chdir(child)

    status = runner.invoke(app, ["page", "status", "--json"])
    current = runner.invoke(app, ["page", "current"])

    assert status.exit_code == 0
    payload = json.loads(status.stdout)
    assert payload["project_root"] == str(tmp_path)
    assert payload["state_file"] == str(tmp_path / ".notion_mcp" / "state" / "page.attach.json")
    assert payload["attachment"]["page"]["id"] == "page-1"
    assert current.exit_code == 0
    assert "Attached page" in current.stdout
    assert "Manual" in current.stdout
    assert "page-1" in current.stdout


def test_page_refresh_updates_attachment_metadata(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = RefreshPagesService()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(pages, "get_pages_service", lambda: service)
    attach = runner.invoke(app, ["page", "attach", "page-1", "--no-verify", "--title", "Old"])
    assert attach.exit_code == 0

    refresh = runner.invoke(app, ["page", "refresh", "--json"])

    assert refresh.exit_code == 0
    payload = json.loads(refresh.stdout)
    assert payload["attachment"]["page"]["title"] == "Refreshed Title"
    assert payload["attachment"]["page"]["url"] == "https://www.notion.so/page-1-refreshed"
    assert payload["attachment"]["page"]["in_trash"] is True
    assert payload["attachment"]["verified_at"] is not None
    assert service.calls == ["page-1"]


def test_page_status_errors_when_no_page_is_attached(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    init_result = runner.invoke(app, ["project", "init"])
    assert init_result.exit_code == 0

    status = runner.invoke(app, ["page", "status"])

    assert status.exit_code == 1
    assert "No page is attached for this project" in status.stdout
    assert "nilo page attach <page_id>" in status.stdout
