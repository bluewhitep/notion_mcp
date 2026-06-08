import json

import pytest

from notion_mcp.mcp_server.server import create_mcp_server
from notion_mcp.mcp_server.tools import users


EXPECTED_STAGE5_TOOLS = {
    "page_property_retrieve",
    "comment_reply",
    "view_create",
    "view_update",
    "view_query",
    "file_upload_list",
    "custom_emoji_retrieve",
    "raw_api_registered_operations",
}


class FakeUsersService:
    def list(self, **params: object) -> dict[str, object]:
        return {
            "results": [{"id": "user-1"}],
            "has_more": True,
            "next_cursor": "next-1",
            "params": params,
        }


def text_result_to_json(result) -> dict[str, object]:
    assert result
    return json.loads(result[0].text)


@pytest.mark.asyncio
async def test_stage5_tool_inventory_contains_extended_tools() -> None:
    tools = await create_mcp_server().list_tools()
    names = {tool.name for tool in tools}

    assert EXPECTED_STAGE5_TOOLS <= names


@pytest.mark.asyncio
async def test_mcp_user_list_passes_pagination(monkeypatch) -> None:
    monkeypatch.setattr(users, "get_users_service", lambda: FakeUsersService())

    result = await create_mcp_server().call_tool(
        "user_list",
        {"page_size": 10, "start_cursor": "cursor-1"},
    )

    payload = text_result_to_json(result)
    assert payload["has_more"] is True
    assert payload["next_cursor"] == "next-1"
    assert payload["params"] == {"page_size": 10, "start_cursor": "cursor-1"}


@pytest.mark.asyncio
async def test_raw_api_registered_operations_tool_lists_extended_operations() -> None:
    result = await create_mcp_server().call_tool("raw_api_registered_operations", {})

    payload = text_result_to_json(result)
    assert "pages.properties.retrieve" in payload["operations"]
    assert "views.query" in payload["operations"]
    assert "custom_emojis.retrieve" in payload["operations"]
