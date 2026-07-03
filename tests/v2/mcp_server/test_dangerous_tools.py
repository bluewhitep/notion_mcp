import json

import pytest

from nilo.mcp_server.server import create_mcp_server


def text_result_to_json(result) -> dict[str, object]:
    assert result
    return json.loads(result[0].text)


@pytest.mark.asyncio
async def test_destructive_tools_are_annotated_and_require_confirmation() -> None:
    server = create_mcp_server()
    tools = {tool.name: tool for tool in await server.list_tools()}

    for name in ["page_trash", "block_trash"]:
        assert tools[name].annotations is not None
        assert tools[name].annotations.destructiveHint is True
        assert "confirm" in tools[name].inputSchema.get("required", [])


@pytest.mark.asyncio
async def test_destructive_tool_without_confirm_returns_error() -> None:
    result = await create_mcp_server().call_tool("page_trash", {"page_id": "page-1"})

    payload = text_result_to_json(result)
    assert payload["ok"] is False
    assert payload["error"]["code"] == "confirmation_required"
