import os

import pytest

from nilo.core.auth import AuthService
from nilo.core.client import create_notion_client
from nilo.core.config import CoreConfig


pytestmark = pytest.mark.live


def test_live_auth_validate_requires_opt_in() -> None:
    if os.getenv("NOTION_MCP_LIVE") != "1":
        pytest.skip("Set NOTION_MCP_LIVE=1 and NOTION_MCP_TOKEN to run live auth validation")
    token = os.getenv("NOTION_MCP_TOKEN")
    user_id = os.getenv("NOTION_MCP_USER_ID")
    if not token:
        pytest.skip("NOTION_MCP_TOKEN is required for live auth validation")

    config = CoreConfig(notion_token=token, user_id=user_id)
    result = AuthService(create_notion_client(config)).validate(expected_user_id=user_id)

    assert result.valid is True
    assert result.user_id
