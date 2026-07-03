import json

import pytest

from nilo.core.services.pages import PagesService
from nilo.mcp_server.server import create_mcp_server
from nilo.mcp_server.tools import pages as page_tools
from tests.v2.fixtures.fake_notion import FakeNotionClient


@pytest.mark.asyncio
async def test_mcp_page_create_flows_to_core_fake_notion(monkeypatch) -> None:
    fake_client = FakeNotionClient()
    monkeypatch.setattr(page_tools, "get_pages_service", lambda: PagesService(fake_client))

    result = await create_mcp_server().call_tool(
        "page_create",
        {"payload": {"parent": {"page_id": "root"}}},
    )

    payload = json.loads(result[0].text)
    assert payload["object"] == "page"
    assert fake_client.calls[-1] == (
        "pages.create",
        {"parent": {"page_id": "root"}},
    )
