import inspect
import json

from typer.testing import CliRunner

from notion_mcp.cli import app
from notion_mcp.cli.commands import comments, custom_emojis, data_sources, file_uploads, raw_api, search, users, views


runner = CliRunner()


class FakeService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def retrieve(self, resource_id: str) -> dict[str, object]:
        self.calls.append(("retrieve", resource_id))
        return {"id": resource_id}

    def me(self) -> dict[str, object]:
        self.calls.append(("me", {}))
        return {"object": "user"}

    def list(self, **params: object) -> dict[str, object]:
        self.calls.append(("list", params))
        return {"results": [], "params": params}

    def search(self, payload: dict[str, object]) -> dict[str, object]:
        self.calls.append(("search", payload))
        return {"results": [], "payload": payload}


class FakeRawService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def invoke(self, operation: str, arguments: dict[str, object]) -> dict[str, object]:
        self.calls.append(("invoke", {"operation": operation, "arguments": arguments}))
        return {"operation": operation, "arguments": arguments}


def test_extended_resource_command_groups_are_registered() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    for name in ["data-source", "user", "comment", "view", "file-upload", "search", "custom-emoji", "raw-api"]:
        assert name in result.stdout


def test_data_source_retrieve_calls_core_service(monkeypatch) -> None:
    service = FakeService()
    monkeypatch.setattr(data_sources, "get_data_sources_service", lambda: service)

    result = runner.invoke(app, ["data-source", "retrieve", "ds-1", "--json"])

    assert result.exit_code == 0
    assert json.loads(result.stdout)["id"] == "ds-1"
    assert service.calls == [("retrieve", "ds-1")]


def test_user_me_calls_core_service(monkeypatch) -> None:
    service = FakeService()
    monkeypatch.setattr(users, "get_users_service", lambda: service)

    result = runner.invoke(app, ["user", "me", "--json"])

    assert result.exit_code == 0
    assert json.loads(result.stdout)["object"] == "user"
    assert service.calls == [("me", {})]


def test_comment_list_calls_core_service(monkeypatch) -> None:
    service = FakeService()
    monkeypatch.setattr(comments, "get_comments_service", lambda: service)

    result = runner.invoke(app, ["comment", "list", "--block-id", "block-1", "--json"])

    assert result.exit_code == 0
    assert json.loads(result.stdout)["params"]["block_id"] == "block-1"
    assert service.calls == [("list", {"block_id": "block-1"})]


def test_view_retrieve_calls_core_service(monkeypatch) -> None:
    service = FakeService()
    monkeypatch.setattr(views, "get_views_service", lambda: service)

    result = runner.invoke(app, ["view", "retrieve", "view-1", "--json"])

    assert result.exit_code == 0
    assert json.loads(result.stdout)["id"] == "view-1"
    assert service.calls == [("retrieve", "view-1")]


def test_file_upload_retrieve_calls_core_service(monkeypatch) -> None:
    service = FakeService()
    monkeypatch.setattr(file_uploads, "get_file_uploads_service", lambda: service)

    result = runner.invoke(app, ["file-upload", "retrieve", "file-1", "--json"])

    assert result.exit_code == 0
    assert json.loads(result.stdout)["id"] == "file-1"
    assert service.calls == [("retrieve", "file-1")]


def test_search_query_calls_core_service(monkeypatch) -> None:
    service = FakeService()
    monkeypatch.setattr(search, "get_search_service", lambda: service)

    result = runner.invoke(app, ["search", "query", "--payload", '{"query": "Roadmap"}', "--json"])

    assert result.exit_code == 0
    assert json.loads(result.stdout)["payload"] == {"query": "Roadmap"}
    assert service.calls == [("search", {"query": "Roadmap"})]


def test_custom_emoji_list_calls_core_service(monkeypatch) -> None:
    service = FakeService()
    monkeypatch.setattr(custom_emojis, "get_custom_emojis_service", lambda: service)

    result = runner.invoke(app, ["custom-emoji", "list", "--page-size", "5", "--start-cursor", "cursor-1", "--json"])

    assert result.exit_code == 0
    assert json.loads(result.stdout)["results"] == []
    assert service.calls == [("list", {"page_size": 5, "start_cursor": "cursor-1"})]


def test_raw_api_invoke_calls_core_service(monkeypatch) -> None:
    service = FakeRawService()
    monkeypatch.setattr(raw_api, "get_raw_api_service", lambda: service)

    result = runner.invoke(app, ["raw-api", "invoke", "pages.retrieve", "--arguments", '{"page_id": "page-1"}', "--json"])

    assert result.exit_code == 0
    assert json.loads(result.stdout)["operation"] == "pages.retrieve"
    assert service.calls == [("invoke", {"operation": "pages.retrieve", "arguments": {"page_id": "page-1"}})]


def test_extended_cli_modules_do_not_import_notion_sdk() -> None:
    for module in [data_sources, users, comments, views, file_uploads, search, custom_emojis, raw_api]:
        assert "notion_client" not in inspect.getsource(module)
