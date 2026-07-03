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

    def create(self, payload: dict[str, object]) -> dict[str, object]:
        self.calls.append(("create", payload))
        return {"object": "database", "payload": payload}

    def update(self, database_id: str, payload: dict[str, object]) -> dict[str, object]:
        self.calls.append(("update", {"database_id": database_id, "payload": payload}))
        return {"object": "database", "id": database_id, "payload": payload}

    def rename(self, database_id: str, new_name: str) -> dict[str, object]:
        self.calls.append(("rename", {"database_id": database_id, "new_name": new_name}))
        return {"object": "database", "id": database_id, "name": new_name}


def test_database_retrieve_uses_database_service(monkeypatch) -> None:
    service = FakeDatabasesService()
    monkeypatch.setattr(databases, "get_databases_service", lambda: service)

    result = runner.invoke(app, ["database", "retrieve", "db-1", "--json"])

    assert result.exit_code == 0
    assert json.loads(result.stdout)["id"] == "db-1"
    assert service.calls == [("retrieve", "db-1")]


def test_database_sources_uses_database_service(monkeypatch) -> None:
    service = FakeDatabasesService()
    monkeypatch.setattr(databases, "get_databases_service", lambda: service)

    result = runner.invoke(app, ["database", "sources", "db-1", "--json"])

    assert result.exit_code == 0
    assert json.loads(result.stdout)["data_sources"] == [{"id": "ds-1", "name": "Tasks"}]
    assert service.calls == [("list_data_sources", "db-1")]


def test_database_create_update_and_rename_use_database_service(monkeypatch, tmp_path) -> None:
    service = FakeDatabasesService()
    monkeypatch.setattr(databases, "get_databases_service", lambda: service)
    monkeypatch.chdir(tmp_path)

    create_result = runner.invoke(app, ["database", "create", "--payload", '{"title": []}', "--json"])
    update_result = runner.invoke(app, ["database", "update", "db-1", "--payload", '{"description": []}', "--json"])
    rename_result = runner.invoke(app, ["database", "rename", "db-1", "Project Database", "--json"])

    assert create_result.exit_code == 0
    assert update_result.exit_code == 0
    assert rename_result.exit_code == 0
    assert service.calls == [
        ("create", {"title": []}),
        ("update", {"database_id": "db-1", "payload": {"description": []}}),
        ("rename", {"database_id": "db-1", "new_name": "Project Database"}),
    ]
