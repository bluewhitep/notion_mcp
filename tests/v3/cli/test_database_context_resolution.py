import json

from typer.testing import CliRunner

from nilo.cli import app
from nilo.cli.commands import databases


runner = CliRunner()


class FakeDatabasesService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def retrieve(self, database_id: str) -> dict[str, object]:
        self.calls.append(("retrieve", database_id))
        return {"object": "database", "id": database_id}

    def list_data_sources(self, database_id: str) -> list[dict[str, object]]:
        self.calls.append(("list_data_sources", database_id))
        return [{"id": "ds-1", "name": "Tasks"}]


class FakeDataSourcesService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def query(self, data_source_id: str, payload: dict[str, object]) -> dict[str, object]:
        self.calls.append(("query", {"data_source_id": data_source_id, "payload": payload}))
        return {"results": [], "data_source_id": data_source_id}

    def rename_property(self, data_source_id: str, property_id_or_name: str, new_name: str) -> dict[str, object]:
        self.calls.append(
            (
                "rename_property",
                {
                    "data_source_id": data_source_id,
                    "property_id_or_name": property_id_or_name,
                    "new_name": new_name,
                },
            )
        )
        return {"object": "data_source", "id": data_source_id}


class FakePagesService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def create(self, payload: dict[str, object]) -> dict[str, object]:
        self.calls.append(("create", payload))
        return {"object": "page", "payload": payload}


def attach_database(tmp_path) -> None:
    result = runner.invoke(
        app,
        ["database", "attach", "db-1", "--no-verify", "--title", "Manual Database"],
    )
    assert result.exit_code == 0
    state_file = tmp_path / ".notion_mcp" / "state" / "database.attach.json"
    payload = json.loads(state_file.read_text(encoding="utf-8"))
    payload["active_data_source"] = {"id": "ds-1", "name": "Tasks", "parent_database_id": "db-1"}
    payload["available_data_sources"] = [{"id": "ds-1", "name": "Tasks", "parent_database_id": "db-1"}]
    state_file.write_text(json.dumps(payload), encoding="utf-8")


def test_attached_database_defaults_for_container_and_data_source_commands(monkeypatch, tmp_path) -> None:
    db_service = FakeDatabasesService()
    ds_service = FakeDataSourcesService()
    page_service = FakePagesService()
    monkeypatch.setattr(databases, "get_databases_service", lambda: db_service)
    monkeypatch.setattr(databases, "get_data_sources_service", lambda: ds_service)
    monkeypatch.setattr(databases, "get_pages_service", lambda: page_service)
    monkeypatch.chdir(tmp_path)

    attach_database(tmp_path)

    retrieve = runner.invoke(app, ["database", "retrieve", "--json"])
    sources = runner.invoke(app, ["database", "sources", "--json"])
    query = runner.invoke(app, ["database", "query", "--payload", '{"page_size": 1}', "--json"])
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
    rename = runner.invoke(app, ["database", "property", "rename", "Status", "State", "--json"])

    assert retrieve.exit_code == 0
    assert sources.exit_code == 0
    assert query.exit_code == 0
    assert create_page.exit_code == 0
    assert rename.exit_code == 0
    assert db_service.calls == [("retrieve", "db-1"), ("list_data_sources", "db-1")]
    assert ds_service.calls == [
        ("query", {"data_source_id": "ds-1", "payload": {"page_size": 1}}),
        (
            "rename_property",
            {"data_source_id": "ds-1", "property_id_or_name": "Status", "new_name": "State"},
        ),
    ]
    assert page_service.calls == [
        (
            "create",
            {
                "parent": {"type": "data_source_id", "data_source_id": "ds-1"},
                "properties": {"Name": {"title": [{"text": {"content": "Task"}}]}},
            },
        )
    ]


def test_missing_active_data_source_errors_for_table_level_default(monkeypatch, tmp_path) -> None:
    monkeypatch.chdir(tmp_path)
    attach = runner.invoke(
        app,
        ["database", "attach", "db-1", "--no-verify", "--title", "Manual Database"],
    )
    assert attach.exit_code == 0

    result = runner.invoke(app, ["database", "query", "--payload", "{}", "--json"])

    assert result.exit_code != 0
    payload = json.loads(result.stdout)
    assert payload["error"]["code"] == "active_data_source_not_found"
