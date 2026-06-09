import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from notion_mcp.cli import app
from notion_mcp.cli.commands import pages


runner = CliRunner()


class FakePagesService:
    def content(self, page_id: str, *, tree: bool = False) -> dict[str, object]:
        return {"page": {"id": page_id, "title": "Root Page", "properties": {}}, "blocks": []}


def test_project_context_discovery_from_nested_directories(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(pages, "get_pages_service", lambda: FakePagesService())
    init = runner.invoke(app, ["init", "--project-name", "Demo", "--json"])
    attach = runner.invoke(app, ["page", "attach", "page-1", "--no-verify", "--title", "Root Page"])

    nested = tmp_path / "a" / "b" / "c"
    nested.mkdir(parents=True)
    monkeypatch.chdir(nested)
    root = runner.invoke(app, ["pwd", "--json"])
    content = runner.invoke(app, ["page", "blocks", "--json"])

    assert init.exit_code == 0
    assert attach.exit_code == 0
    assert root.exit_code == 0
    assert json.loads(root.stdout)["project_root"] == str(tmp_path)
    assert content.exit_code == 0
    assert json.loads(content.stdout)["page"]["id"] == "page-1"


def test_missing_project_context_errors_include_remediation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    child = tmp_path / "no-project" / "child"
    child.mkdir(parents=True)
    monkeypatch.chdir(child)

    status = runner.invoke(app, ["config", "--local", "--show"])
    content = runner.invoke(app, ["page", "blocks"])

    assert status.exit_code == 1
    assert "No .notion_mcp/config.json found" in status.stdout
    assert "notion-mcp init" in status.stdout
    assert content.exit_code == 1
    assert "notion-mcp page attach <page_id>" in content.stdout
