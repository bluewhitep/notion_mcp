import json

import pytest

from nilo.mcp_server.server import create_mcp_server
from nilo.mcp_server.tools import pages


class FakePagesService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def retrieve(self, page_id: str) -> dict[str, object]:
        self.calls.append(("retrieve", page_id))
        return {"id": page_id, "object": "page"}

    def create(self, payload: dict[str, object]) -> dict[str, object]:
        self.calls.append(("create", payload))
        return {"created": payload}


def text_result_to_json(result) -> dict[str, object]:
    assert result
    return json.loads(result[0].text)


@pytest.mark.asyncio
async def test_page_retrieve_tool_calls_core_service(monkeypatch) -> None:
    service = FakePagesService()
    monkeypatch.setattr(pages, "get_pages_service", lambda: service)
    server = create_mcp_server()

    result = await server.call_tool("page_retrieve", {"page_id": "page-1"})

    assert text_result_to_json(result)["id"] == "page-1"
    assert service.calls == [("retrieve", "page-1")]


@pytest.mark.asyncio
async def test_page_create_dry_run_does_not_call_core_write(monkeypatch) -> None:
    service = FakePagesService()
    monkeypatch.setattr(pages, "get_pages_service", lambda: service)
    server = create_mcp_server()

    result = await server.call_tool(
        "page_create",
        {"payload": {"parent": {"page_id": "root"}}, "dry_run": True},
    )

    payload = text_result_to_json(result)
    assert payload["dry_run"] is True
    assert payload["operation"] == "pages.create"
    assert service.calls == []


@pytest.mark.asyncio
async def test_config_status_tool_returns_structured_result(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("NOTION_MCP_CONFIG", str(tmp_path / "missing.json"))
    server = create_mcp_server()

    result = await server.call_tool("config_status", {})

    payload = text_result_to_json(result)
    assert payload["configured"] is False
    assert payload["capabilities"]["core"] is True
