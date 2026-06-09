import json

from typer.testing import CliRunner

from notion_mcp.cli import app
from notion_mcp.cli.commands import databases


runner = CliRunner()


class FakeDatabasesService:
    def __init__(self, response: dict[str, object]) -> None:
        self.response = response
        self.calls: list[tuple[str, object]] = []

    def retrieve(self, database_id: str) -> dict[str, object]:
        self.calls.append(("retrieve", database_id))
        return self.response


def database_response(data_sources: list[dict[str, object]]) -> dict[str, object]:
    return {
        "id": "db-1",
        "title": [{"plain_text": "Project Database"}],
        "url": "https://www.notion.so/db-1",
        "is_inline": False,
        "archived": False,
        "in_trash": False,
        "data_sources": data_sources,
    }


def test_database_attach_verified_single_source_auto_selects_active_data_source(monkeypatch, tmp_path) -> None:
    service = FakeDatabasesService(database_response([{"id": "ds-1", "name": "Tasks"}]))
    monkeypatch.setattr(databases, "get_databases_service", lambda: service)
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["database", "attach", "db-1", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["attachment"]["database"]["id"] == "db-1"
    assert payload["attachment"]["active_data_source"]["id"] == "ds-1"
    assert service.calls == [("retrieve", "db-1")]
    assert (tmp_path / ".notion_mcp" / "state" / "database.attach.json").exists()


def test_database_attach_requires_data_source_for_multiple_sources(monkeypatch, tmp_path) -> None:
    service = FakeDatabasesService(
        database_response(
            [
                {"id": "ds-1", "name": "Tasks"},
                {"id": "ds-2", "name": "Archive"},
            ]
        )
    )
    monkeypatch.setattr(databases, "get_databases_service", lambda: service)
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["database", "attach", "db-1"])

    assert result.exit_code != 0
    assert "multiple data sources" in result.stdout.lower()
    assert "Tasks" in result.stdout
    assert "Archive" in result.stdout


def test_database_attach_can_select_data_source_by_name(monkeypatch, tmp_path) -> None:
    service = FakeDatabasesService(
        database_response(
            [
                {"id": "ds-1", "name": "Tasks"},
                {"id": "ds-2", "name": "Archive"},
            ]
        )
    )
    monkeypatch.setattr(databases, "get_databases_service", lambda: service)
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["database", "attach", "db-1", "--data-source", "Archive", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["attachment"]["active_data_source"] == {
        "id": "ds-2",
        "name": "Archive",
        "parent_database_id": "db-1",
    }


def test_database_attach_no_verify_writes_limited_state(monkeypatch, tmp_path) -> None:
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(
        app,
        ["database", "attach", "db-1", "--no-verify", "--title", "Manual Database", "--json"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["attachment"]["database"]["title"] == "Manual Database"
    assert payload["attachment"]["active_data_source"] is None
    assert payload["attachment"]["verified_at"] is None
