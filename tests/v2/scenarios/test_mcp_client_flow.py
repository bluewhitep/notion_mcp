import json

import pytest

from nilo.mcp_server.server import create_mcp_server


@pytest.mark.asyncio
async def test_mcp_client_style_list_and_call_flow(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("NOTION_MCP_CONFIG", str(tmp_path / "missing.json"))
    server = create_mcp_server()

    tools = await server.list_tools()
    names = {tool.name for tool in tools}
    result = await server.call_tool("config_status", {})

    assert "config_status" in names
    payload = json.loads(result[0].text)
    assert payload["configured"] is False
    assert payload["capabilities"]["core"] is True
