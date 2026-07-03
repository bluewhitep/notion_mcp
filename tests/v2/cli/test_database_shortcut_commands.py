import json

from typer.testing import CliRunner

from nilo.cli import app
from nilo.cli.commands import databases


runner = CliRunner()


class FakePagesService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def create(self, payload: dict[str, object]) -> dict[str, object]:
        self.calls.append(("create", payload))
        return {"object": "page", "payload": payload}

    def update(self, page_id: str, payload: dict[str, object]) -> dict[str, object]:
        self.calls.append(("update", {"page_id": page_id, "payload": payload}))
        return {"object": "page", "id": page_id, "payload": payload}


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


def test_database_query_can_explicitly_target_data_source(monkeypatch) -> None:
    service = FakeDataSourcesService()
    monkeypatch.setattr(databases, "get_data_sources_service", lambda: service)

    result = runner.invoke(
        app,
        ["database", "query", "--data-source", "ds-1", "--payload", '{"page_size": 1}', "--json"],
    )

    assert result.exit_code == 0
    assert json.loads(result.stdout)["data_source_id"] == "ds-1"
    assert service.calls == [("query", {"data_source_id": "ds-1", "payload": {"page_size": 1}})]


def test_database_page_create_and_update_use_page_service(monkeypatch) -> None:
    service = FakePagesService()
    monkeypatch.setattr(databases, "get_pages_service", lambda: service)

    create_result = runner.invoke(
        app,
        [
            "database",
            "page",
            "create",
            "ds-1",
            "--properties",
            '{"Name": {"title": [{"text": {"content": "Task"}}]}}',
            "--json",
        ],
    )
    update_result = runner.invoke(
        app,
        [
            "database",
            "page",
            "update",
            "page-1",
            "--properties",
            '{"Status": {"select": {"name": "Done"}}}',
            "--json",
        ],
    )

    assert create_result.exit_code == 0
    assert update_result.exit_code == 0
    assert service.calls == [
        (
            "create",
            {
                "parent": {"type": "data_source_id", "data_source_id": "ds-1"},
                "properties": {"Name": {"title": [{"text": {"content": "Task"}}]}},
            },
        ),
        ("update", {"page_id": "page-1", "payload": {"properties": {"Status": {"select": {"name": "Done"}}}}}),
    ]


def test_database_property_rename_uses_data_source_service(monkeypatch) -> None:
    service = FakeDataSourcesService()
    monkeypatch.setattr(databases, "get_data_sources_service", lambda: service)

    result = runner.invoke(app, ["database", "property", "rename", "ds-1", "Status", "State", "--json"])

    assert result.exit_code == 0
    assert service.calls == [
        (
            "rename_property",
            {"data_source_id": "ds-1", "property_id_or_name": "Status", "new_name": "State"},
        )
    ]
