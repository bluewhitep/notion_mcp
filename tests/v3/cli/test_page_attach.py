import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from nilo.cli import app
from nilo.cli.commands import pages


runner = CliRunner()


class FakePagesService:
    def __init__(self, title: str = "Verified Home") -> None:
        self.title = title
        self.calls: list[str] = []

    def retrieve(self, page_id: str) -> dict[str, object]:
        self.calls.append(page_id)
        return {
            "id": page_id,
            "url": f"https://www.notion.so/{page_id}",
            "parent": {"type": "workspace", "workspace": True},
            "archived": False,
            "in_trash": False,
            "properties": {
                "Name": {
                    "type": "title",
                    "title": [{"plain_text": self.title}],
                }
            },
        }


def test_page_attach_verifies_page_and_auto_initializes_project(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = FakePagesService()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(pages, "get_pages_service", lambda: service)

    result = runner.invoke(app, ["page", "attach", "page-1", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["project_root"] == str(tmp_path)
    assert payload["attachment"]["page"]["id"] == "page-1"
    assert payload["attachment"]["page"]["title"] == "Verified Home"
    assert payload["attachment"]["verified_at"] is not None
    assert service.calls == ["page-1"]
    assert (tmp_path / ".notion_mcp" / "config.json").exists()
    assert (tmp_path / ".notion_mcp" / "state" / "page.attach.json").exists()


def test_page_attach_no_verify_writes_manual_title_without_notion_call(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = FakePagesService()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(pages, "get_pages_service", lambda: service)

    result = runner.invoke(
        app,
        ["page", "attach", "page-manual", "--no-verify", "--title", "Manual Title", "--json"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["attachment"]["page"]["id"] == "page-manual"
    assert payload["attachment"]["page"]["title"] == "Manual Title"
    assert payload["attachment"]["verified_at"] is None
    assert payload["attachment"]["page"]["url"] is None
    assert service.calls == []


def test_page_attach_require_project_fails_without_project_config(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["page", "attach", "page-1", "--require-project"])

    assert result.exit_code == 1
    assert "No .notion_mcp/config.json found" in result.stdout
    assert not (tmp_path / ".notion_mcp").exists()
