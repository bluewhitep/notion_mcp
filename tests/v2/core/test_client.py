import uuid

import pytest

from notion_mcp.core.client import NotionClientFactory
from notion_mcp.core.config import DEFAULT_NOTION_VERSION, CoreConfig
from notion_mcp.core.errors import ConfigValidationError


class FakeNotionClient:
    def __init__(self, **kwargs: object) -> None:
        self.kwargs = kwargs


def test_notion_client_factory_injects_auth_version_timeout_and_retry() -> None:
    cfg = CoreConfig(
        notion_token="secret-token",
        user_name="Ada",
        user_id=str(uuid.uuid4()),
        timeout_ms=2222,
        retry=False,
    )
    factory = NotionClientFactory(client_cls=FakeNotionClient)

    client = factory.create(cfg)

    assert isinstance(client, FakeNotionClient)
    assert client.kwargs == {
        "auth": "secret-token",
        "notion_version": DEFAULT_NOTION_VERSION,
        "timeout_ms": 2222,
        "retry": False,
    }


def test_notion_client_factory_rejects_missing_token() -> None:
    factory = NotionClientFactory(client_cls=FakeNotionClient)

    with pytest.raises(ConfigValidationError):
        factory.create(CoreConfig(user_name="Ada", user_id=str(uuid.uuid4())))


def test_notion_client_factory_allows_fake_client_passthrough() -> None:
    fake_client = object()
    factory = NotionClientFactory(fake_client=fake_client)

    assert factory.create(CoreConfig()) is fake_client
