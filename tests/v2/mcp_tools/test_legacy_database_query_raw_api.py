import json

import pytest

from nilo.mcp_server.server import create_mcp_server
from nilo.mcp_server.tools import databases


class ContainerOnlyDatabasesService:
    pass


class SingleDataSourceDatabasesService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def list_data_sources(self, database_id: str) -> list[dict[str, object]]:
        self.calls.append(("list_data_sources", database_id))
        return [{"id": "ds-1", "name": "Tasks"}]


class MultiDataSourceDatabasesService:
    def list_data_sources(self, database_id: str) -> list[dict[str, object]]:
        return [
            {"id": "ds-1", "name": "Tasks"},
            {"id": "ds-2", "name": "Bugs"},
        ]


class FakeDataSourcesService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, object]]] = []

    def query(self, data_source_id: str, payload: dict[str, object]) -> dict[str, object]:
        self.calls.append((data_source_id, payload))
        return {"object": "list", "data_source_id": data_source_id, "payload": payload}


class FakeRawApiService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, object]]] = []

    def invoke(self, operation: str, arguments: dict[str, object]) -> dict[str, object]:
        self.calls.append((operation, arguments))
        return {"operation": operation, "arguments": arguments}


def text_result_to_json(result) -> dict[str, object]:
    assert result
    return json.loads(result[0].text)


@pytest.mark.asyncio
async def test_legacy_database_query_mcp_tool_uses_raw_api_compatibility_path(monkeypatch) -> None:
    raw_service = FakeRawApiService()
    monkeypatch.setattr(databases, "get_databases_service", lambda: ContainerOnlyDatabasesService())
    monkeypatch.setattr(databases, "get_raw_api_service", lambda: raw_service)

    result = await create_mcp_server().call_tool("database_query", {"database_id": "db-1", "payload": {"page_size": 1}})

    payload = text_result_to_json(result)
    assert payload["operation"] == "databases.query"
    assert raw_service.calls == [("databases.query", {"database_id": "db-1", "page_size": 1})]


@pytest.mark.asyncio
async def test_database_query_mcp_tool_uses_single_data_source_query(monkeypatch) -> None:
    database_service = SingleDataSourceDatabasesService()
    data_source_service = FakeDataSourcesService()
    monkeypatch.setattr(databases, "get_databases_service", lambda: database_service)
    monkeypatch.setattr(databases, "get_data_sources_service", lambda: data_source_service)

    result = await create_mcp_server().call_tool("database_query", {"database_id": "db-1", "payload": {"page_size": 1}})

    payload = text_result_to_json(result)
    assert payload == {"object": "list", "data_source_id": "ds-1", "payload": {"page_size": 1}}
    assert database_service.calls == [("list_data_sources", "db-1")]
    assert data_source_service.calls == [("ds-1", {"page_size": 1})]


@pytest.mark.asyncio
async def test_database_query_mcp_tool_requires_explicit_data_source_for_multiple_sources(monkeypatch) -> None:
    monkeypatch.setattr(databases, "get_databases_service", lambda: MultiDataSourceDatabasesService())

    result = await create_mcp_server().call_tool("database_query", {"database_id": "db-1", "payload": {"page_size": 1}})

    payload = text_result_to_json(result)
    assert payload["ok"] is False
    assert payload["error"]["code"] == "database_data_source_selection_required"
