import json
from pathlib import Path

import pytest

from nilo.mcp_server.server import create_mcp_server
from nilo.mcp_server.tools import data_sources, databases


EXPECTED_DATABASE_DATA_SOURCE_TOOLS = {
    "database_sources",
    "database_rename",
    "data_source_templates",
    "data_source_property_rename",
}


class FakeDatabasesService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def list_data_sources(self, database_id: str) -> list[dict[str, object]]:
        self.calls.append(("list_data_sources", database_id))
        return [{"id": "ds-1", "name": "Tasks"}]

    def rename(self, database_id: str, new_name: str) -> dict[str, object]:
        self.calls.append(("rename", {"database_id": database_id, "new_name": new_name}))
        return {"object": "database", "id": database_id, "title": new_name}


class FakeDataSourcesService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def create_for_database(self, database_id: str, payload: dict[str, object]) -> dict[str, object]:
        self.calls.append(("create_for_database", {"database_id": database_id, "payload": payload}))
        return {"object": "data_source", "parent_database_id": database_id}

    def templates(self, data_source_id: str) -> dict[str, object]:
        self.calls.append(("templates", data_source_id))
        return {"results": [{"id": "tmpl-1", "name": "Default"}]}

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


def text_result_to_json(result) -> dict[str, object]:
    assert result
    return json.loads(result[0].text)


@pytest.mark.asyncio
async def test_mcp_inventory_contains_database_data_source_separation_tools() -> None:
    tools = await create_mcp_server().list_tools()
    names = {tool.name for tool in tools}

    assert EXPECTED_DATABASE_DATA_SOURCE_TOOLS <= names


@pytest.mark.asyncio
async def test_database_mcp_tools_call_database_service(monkeypatch) -> None:
    service = FakeDatabasesService()
    monkeypatch.setattr(databases, "get_databases_service", lambda: service)
    server = create_mcp_server()

    sources_result = await server.call_tool("database_sources", {"database_id": "db-1"})
    rename_result = await server.call_tool(
        "database_rename",
        {"database_id": "db-1", "new_name": "Project Database"},
    )

    assert text_result_to_json(sources_result) == {
        "database_id": "db-1",
        "data_sources": [{"id": "ds-1", "name": "Tasks"}],
    }
    assert text_result_to_json(rename_result)["title"] == "Project Database"
    assert service.calls == [
        ("list_data_sources", "db-1"),
        ("rename", {"database_id": "db-1", "new_name": "Project Database"}),
    ]


@pytest.mark.asyncio
async def test_data_source_mcp_tools_call_data_source_service(monkeypatch) -> None:
    service = FakeDataSourcesService()
    monkeypatch.setattr(data_sources, "get_data_sources_service", lambda: service)
    server = create_mcp_server()

    create_result = await server.call_tool(
        "data_source_create",
        {
            "database_id": "db-1",
            "payload": {"title": [{"plain_text": "Tasks"}], "properties": {"Name": {"title": {}}}},
        },
    )
    templates_result = await server.call_tool("data_source_templates", {"data_source_id": "ds-1"})
    rename_result = await server.call_tool(
        "data_source_property_rename",
        {"data_source_id": "ds-1", "property_id_or_name": "Status", "new_name": "State"},
    )

    assert text_result_to_json(create_result)["parent_database_id"] == "db-1"
    assert text_result_to_json(templates_result)["results"] == [{"id": "tmpl-1", "name": "Default"}]
    assert text_result_to_json(rename_result)["id"] == "ds-1"
    assert service.calls == [
        (
            "create_for_database",
            {
                "database_id": "db-1",
                "payload": {"title": [{"plain_text": "Tasks"}], "properties": {"Name": {"title": {}}}},
            },
        ),
        ("templates", "ds-1"),
        (
            "rename_property",
            {"data_source_id": "ds-1", "property_id_or_name": "Status", "new_name": "State"},
        ),
    ]


def test_database_data_source_mcp_tools_do_not_import_cli_or_sdk_directly() -> None:
    for relative_path in [
        "src/nilo/mcp_server/tools/databases.py",
        "src/nilo/mcp_server/tools/data_sources.py",
    ]:
        source = Path(relative_path).read_text(encoding="utf-8")
        assert "nilo.cli" not in source
        assert "notion_client" not in source
        assert "from notion_client" not in source
        assert "import notion_client" not in source
