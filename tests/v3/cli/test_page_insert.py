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

    def create(self, payload: dict[str, object]) -> dict[str, object]:
        self.calls.append(("page.create", payload))
        return {"object": "page", "payload": payload}


class FakeDatabasesService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def create(self, payload: dict[str, object]) -> dict[str, object]:
        self.calls.append(("database.create", payload))
        return {"object": "database", "payload": payload}


def test_page_insert_page_uses_attached_page_as_parent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = FakePagesService()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(pages, "get_pages_service", lambda: service)
    attach = runner.invoke(app, ["page", "attach", "attached-page", "--no-verify", "--title", "Attached"])
    assert attach.exit_code == 0

    result = runner.invoke(app, ["page", "insert", "page", "--payload", '{"properties": {}}', "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)["payload"]
    assert payload["parent"] == {"type": "page_id", "page_id": "attached-page"}
    assert service.calls == [("page.create", {"properties": {}, "parent": {"type": "page_id", "page_id": "attached-page"}})]


def test_page_insert_database_uses_attached_page_as_parent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = FakeDatabasesService()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(pages, "get_databases_service", lambda: service)
    attach = runner.invoke(app, ["page", "attach", "attached-page", "--no-verify", "--title", "Attached"])
    assert attach.exit_code == 0

    result = runner.invoke(app, ["page", "insert", "database", "--payload", '{"title": []}', "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)["payload"]
    assert payload["parent"] == {"type": "page_id", "page_id": "attached-page"}
    assert service.calls == [("database.create", {"title": [], "parent": {"type": "page_id", "page_id": "attached-page"}})]
