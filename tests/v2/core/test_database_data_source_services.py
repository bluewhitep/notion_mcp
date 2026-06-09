from notion_mcp.core.services.data_sources import DataSourcesService
from notion_mcp.core.services.databases import DatabasesService


class Recorder:
    def __init__(self, name: str) -> None:
        self.name = name
        self.calls: list[tuple[str, dict[str, object]]] = []

    def retrieve(self, **kwargs: object) -> dict[str, object]:
        self.calls.append(("retrieve", kwargs))
        if self.name == "databases":
            return {
                "object": "database",
                "id": kwargs["database_id"],
                "data_sources": [
                    {"id": "ds-1", "name": "Tasks"},
                    {"id": "ds-2", "name": "Archive"},
                ],
            }
        return {"object": "data_source", "id": kwargs["data_source_id"], "properties": {}}

    def create(self, **kwargs: object) -> dict[str, object]:
        self.calls.append(("create", kwargs))
        return {"method": f"{self.name}.create", "kwargs": kwargs}

    def update(self, **kwargs: object) -> dict[str, object]:
        self.calls.append(("update", kwargs))
        return {"method": f"{self.name}.update", "kwargs": kwargs}

    def query(self, **kwargs: object) -> dict[str, object]:
        self.calls.append(("query", kwargs))
        return {"method": f"{self.name}.query", "kwargs": kwargs}

    def list_templates(self, **kwargs: object) -> dict[str, object]:
        self.calls.append(("list_templates", kwargs))
        return {"templates": [{"id": "tmpl-1", "name": "Default"}]}


class FakeClient:
    def __init__(self) -> None:
        self.databases = Recorder("databases")
        self.data_sources = Recorder("data_sources")


def test_database_service_retrieves_container_and_lists_child_data_sources() -> None:
    client = FakeClient()
    service = DatabasesService(client)

    database = service.retrieve("db-1")
    sources = service.list_data_sources("db-1")

    assert database["object"] == "database"
    assert sources == [
        {"id": "ds-1", "name": "Tasks"},
        {"id": "ds-2", "name": "Archive"},
    ]
    assert client.databases.calls == [
        ("retrieve", {"database_id": "db-1"}),
        ("retrieve", {"database_id": "db-1"}),
    ]
    assert client.data_sources.calls == []


def test_database_service_rename_updates_container_title_only() -> None:
    client = FakeClient()
    service = DatabasesService(client)

    result = service.rename("db-1", "Project Database")

    assert result["method"] == "databases.update"
    assert client.databases.calls[-1] == (
        "update",
        {
            "database_id": "db-1",
            "title": [{"type": "text", "text": {"content": "Project Database"}}],
        },
    )
    assert client.data_sources.calls == []


def test_data_source_service_handles_table_level_operations_without_database_calls() -> None:
    client = FakeClient()
    service = DataSourcesService(client)

    service.retrieve("ds-1")
    service.query("ds-1", {"page_size": 1})
    service.update("ds-1", {"title": [{"plain_text": "Tasks"}]})
    service.templates("ds-1")
    service.rename_property("ds-1", "Status", "State")

    assert client.databases.calls == []
    assert client.data_sources.calls == [
        ("retrieve", {"data_source_id": "ds-1"}),
        ("query", {"data_source_id": "ds-1", "page_size": 1}),
        ("update", {"data_source_id": "ds-1", "title": [{"plain_text": "Tasks"}]}),
        ("list_templates", {"data_source_id": "ds-1"}),
        ("update", {"data_source_id": "ds-1", "properties": {"Status": {"name": "State"}}}),
    ]


def test_data_source_service_can_create_under_database_container() -> None:
    client = FakeClient()
    service = DataSourcesService(client)

    service.create_for_database("db-1", {"title": [{"plain_text": "Tasks"}], "properties": {"Name": {"title": {}}}})

    assert client.data_sources.calls[-1] == (
        "create",
        {
            "parent": {"type": "database_id", "database_id": "db-1"},
            "title": [{"plain_text": "Tasks"}],
            "properties": {"Name": {"title": {}}},
        },
    )
    assert client.databases.calls == []
