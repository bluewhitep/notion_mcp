import json

from typer.testing import CliRunner

from nilo.cli import app
from nilo.cli.commands import data_sources


runner = CliRunner()


class FakeDataSourcesService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def retrieve(self, data_source_id: str) -> dict[str, object]:
        self.calls.append(("retrieve", data_source_id))
        return {"object": "data_source", "id": data_source_id}

    def query(self, data_source_id: str, payload: dict[str, object]) -> dict[str, object]:
        self.calls.append(("query", {"data_source_id": data_source_id, "payload": payload}))
        return {"results": [], "data_source_id": data_source_id}

    def create_for_database(self, database_id: str, payload: dict[str, object]) -> dict[str, object]:
        self.calls.append(("create_for_database", {"database_id": database_id, "payload": payload}))
        return {"object": "data_source", "database_id": database_id}

    def update(self, data_source_id: str, payload: dict[str, object]) -> dict[str, object]:
        self.calls.append(("update", {"data_source_id": data_source_id, "payload": payload}))
        return {"object": "data_source", "id": data_source_id, "payload": payload}

    def templates(self, data_source_id: str) -> dict[str, object]:
        self.calls.append(("templates", data_source_id))
        return {"templates": [{"id": "tmpl-1", "name": "Default"}]}

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


def test_data_source_retrieve_query_create_update_templates_and_property_rename(monkeypatch) -> None:
    service = FakeDataSourcesService()
    monkeypatch.setattr(data_sources, "get_data_sources_service", lambda: service)

    retrieve_result = runner.invoke(app, ["data-source", "retrieve", "ds-1", "--json"])
    query_result = runner.invoke(app, ["data-source", "query", "ds-1", "--payload", '{"page_size": 1}', "--json"])
    create_result = runner.invoke(
        app,
        [
            "data-source",
            "create",
            "db-1",
            "--payload",
            '{"title": [], "properties": {"Name": {"title": {}}}}',
            "--json",
        ],
    )
    update_result = runner.invoke(app, ["data-source", "update", "ds-1", "--payload", '{"description": []}', "--json"])
    templates_result = runner.invoke(app, ["data-source", "templates", "ds-1", "--json"])
    rename_result = runner.invoke(app, ["data-source", "property", "rename", "ds-1", "Status", "State", "--json"])

    assert retrieve_result.exit_code == 0
    assert query_result.exit_code == 0
    assert create_result.exit_code == 0
    assert update_result.exit_code == 0
    assert templates_result.exit_code == 0
    assert rename_result.exit_code == 0
    assert json.loads(templates_result.stdout)["templates"] == [{"id": "tmpl-1", "name": "Default"}]
    assert service.calls == [
        ("retrieve", "ds-1"),
        ("query", {"data_source_id": "ds-1", "payload": {"page_size": 1}}),
        (
            "create_for_database",
            {"database_id": "db-1", "payload": {"title": [], "properties": {"Name": {"title": {}}}}},
        ),
        ("update", {"data_source_id": "ds-1", "payload": {"description": []}}),
        ("templates", "ds-1"),
        (
            "rename_property",
            {"data_source_id": "ds-1", "property_id_or_name": "Status", "new_name": "State"},
        ),
    ]
