import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from notion_mcp.cli import app
from notion_mcp.cli.commands import databases


runner = CliRunner()


class FakeDatabasesService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def retrieve(self, database_id: str) -> dict[str, object]:
        self.calls.append(("retrieve", database_id))
        return {
            "id": database_id,
            "title": [{"plain_text": "Project Database"}],
            "url": f"https://www.notion.so/{database_id}",
            "is_inline": False,
            "archived": False,
            "in_trash": False,
            "data_sources": [{"id": "ds-1", "name": "Tasks"}],
        }


class FakeDataSourcesService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def query(self, data_source_id: str, payload: dict[str, object]) -> dict[str, object]:
        self.calls.append(("query", {"data_source_id": data_source_id, "payload": payload}))
        return {"results": [{"id": "page-1"}], "data_source_id": data_source_id}


class FakePagesService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def create(self, payload: dict[str, object]) -> dict[str, object]:
        self.calls.append(("create", payload))
        return {"object": "page", "payload": payload}

    def update(self, page_id: str, payload: dict[str, object]) -> dict[str, object]:
        self.calls.append(("update", {"page_id": page_id, "payload": payload}))
        return {"object": "page", "id": page_id, "payload": payload}


def test_attach_database_query_create_update_and_detach(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    db_service = FakeDatabasesService()
    ds_service = FakeDataSourcesService()
    page_service = FakePagesService()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(databases, "get_databases_service", lambda: db_service)
    monkeypatch.setattr(databases, "get_data_sources_service", lambda: ds_service)
    monkeypatch.setattr(databases, "get_pages_service", lambda: page_service)

    attach = runner.invoke(app, ["database", "attach", "db-1", "--json"])
    status = runner.invoke(app, ["database", "status", "--json"])
    query = runner.invoke(app, ["database", "query", "--payload", '{"page_size": 1}', "--json"])
    explicit_query = runner.invoke(
        app,
        ["database", "query", "--data-source", "ds-explicit", "--payload", '{"page_size": 2}', "--json"],
    )
    create_page = runner.invoke(
        app,
        [
            "database",
            "page",
            "create",
            "--properties",
            '{"Name": {"title": [{"text": {"content": "Task"}}]}}',
            "--json",
        ],
    )
    update_page = runner.invoke(
        app,
        ["database", "page", "update", "page-1", "--properties", '{"Status": {"select": {"name": "Done"}}}', "--json"],
    )
    detach = runner.invoke(app, ["database", "detach", "--json"])
    missing = runner.invoke(app, ["database", "query", "--payload", "{}"])

    assert attach.exit_code == 0
    assert status.exit_code == 0
    assert json.loads(status.stdout)["attachment"]["active_data_source"]["id"] == "ds-1"
    assert query.exit_code == 0
    assert explicit_query.exit_code == 0
    assert create_page.exit_code == 0
    assert update_page.exit_code == 0
    assert detach.exit_code == 0
    assert missing.exit_code == 1
    assert "No database is attached for this project" in missing.stdout
    assert db_service.calls == [("retrieve", "db-1")]
    assert ds_service.calls == [
        ("query", {"data_source_id": "ds-1", "payload": {"page_size": 1}}),
        ("query", {"data_source_id": "ds-explicit", "payload": {"page_size": 2}}),
    ]
    assert page_service.calls == [
        (
            "create",
            {
                "parent": {"type": "data_source_id", "data_source_id": "ds-1"},
                "properties": {"Name": {"title": [{"text": {"content": "Task"}}]}},
            },
        ),
        ("update", {"page_id": "page-1", "payload": {"properties": {"Status": {"select": {"name": "Done"}}}}}),
    ]
    assert not (tmp_path / ".notion_mcp" / "state" / "database.attach.json").exists()
