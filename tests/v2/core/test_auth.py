import uuid

import pytest

from nilo.core.auth import AuthService
from nilo.core.errors import NotionAuthError


class FakeUsers:
    def __init__(self, response: dict[str, object]) -> None:
        self.response = response

    def me(self) -> dict[str, object]:
        return self.response


class FakeClient:
    def __init__(self, response: dict[str, object]) -> None:
        self.users = FakeUsers(response)


def test_auth_validate_returns_current_notion_user() -> None:
    user_id = str(uuid.uuid4())
    service = AuthService(FakeClient({"id": user_id, "name": "Ada", "type": "bot"}))

    result = service.validate(expected_user_id=user_id)

    assert result.valid is True
    assert result.user_id == user_id
    assert result.name == "Ada"
    assert result.raw["type"] == "bot"


def test_auth_validate_rejects_configured_user_mismatch() -> None:
    service = AuthService(FakeClient({"id": str(uuid.uuid4()), "name": "Ada"}))

    with pytest.raises(NotionAuthError):
        service.validate(expected_user_id=str(uuid.uuid4()))


def test_auth_validate_wraps_notion_api_error() -> None:
    class FailingUsers:
        def me(self) -> dict[str, object]:
            raise RuntimeError("unauthorized")

    class FailingClient:
        users = FailingUsers()

    with pytest.raises(NotionAuthError) as exc:
        AuthService(FailingClient()).validate()

    assert exc.value.to_dict()["code"] == "notion_auth_failed"
    assert "unauthorized" in exc.value.to_dict()["message"]
