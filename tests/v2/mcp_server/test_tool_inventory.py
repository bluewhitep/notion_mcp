import pytest

from notion_mcp.mcp_server.server import create_mcp_server


EXPECTED_TOOLS = {
    "config_status",
    "config_get",
    "auth_validate",
    "auth_whoami",
    "page_retrieve",
    "page_create",
    "page_update",
    "page_trash",
    "block_children_list",
    "block_append",
    "block_update",
    "block_trash",
    "database_retrieve",
    "database_query",
    "data_source_retrieve",
    "data_source_query",
    "user_list",
    "user_retrieve",
    "user_me",
    "comment_list",
    "comment_create",
    "view_list",
    "view_retrieve",
    "file_upload_create",
    "file_upload_retrieve",
    "file_upload_send",
    "file_upload_complete",
    "search",
    "custom_emoji_list",
    "raw_api_invoke",
}


@pytest.mark.asyncio
async def test_tool_inventory_contains_required_domains() -> None:
    tools = await create_mcp_server().list_tools()
    names = {tool.name for tool in tools}

    assert EXPECTED_TOOLS <= names


@pytest.mark.asyncio
async def test_each_tool_has_description_and_input_schema() -> None:
    tools = await create_mcp_server().list_tools()

    for tool in tools:
        assert tool.description
        assert tool.inputSchema["type"] == "object"
