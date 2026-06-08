import inspect
import json

from typer.testing import CliRunner

from notion_mcp.cli import app
from notion_mcp.cli.commands import blocks, databases, pages


runner = CliRunner()


class FakePagesService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def retrieve(self, page_id: str) -> dict[str, object]:
        self.calls.append(("retrieve", page_id))
        return {"id": page_id, "object": "page"}


class FakeBlocksService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def list_children(self, block_id: str) -> dict[str, object]:
        self.calls.append(("children", block_id))
        return {"results": [], "block_id": block_id}


class FakeDatabasesService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def query(self, database_id: str, payload: dict[str, object]) -> dict[str, object]:
        self.calls.append(("query", {"database_id": database_id, "payload": payload}))
        return {"results": [], "database_id": database_id}


def test_page_retrieve_calls_core_service(monkeypatch) -> None:
    service = FakePagesService()
    monkeypatch.setattr(pages, "get_pages_service", lambda: service)

    result = runner.invoke(app, ["page", "retrieve", "page-1", "--json"])

    assert result.exit_code == 0
    assert json.loads(result.stdout)["id"] == "page-1"
    assert service.calls == [("retrieve", "page-1")]


def test_block_children_list_calls_core_service(monkeypatch) -> None:
    service = FakeBlocksService()
    monkeypatch.setattr(blocks, "get_blocks_service", lambda: service)

    result = runner.invoke(app, ["block", "children", "block-1", "--json"])

    assert result.exit_code == 0
    assert json.loads(result.stdout)["block_id"] == "block-1"
    assert service.calls == [("children", "block-1")]


def test_database_query_calls_core_service(monkeypatch) -> None:
    service = FakeDatabasesService()
    monkeypatch.setattr(databases, "get_databases_service", lambda: service)

    result = runner.invoke(
        app,
        [
            "database",
            "query",
            "db-1",
            "--payload",
            '{"page_size": 1}',
            "--json",
        ],
    )

    assert result.exit_code == 0
    assert json.loads(result.stdout)["database_id"] == "db-1"
    assert service.calls == [("query", {"database_id": "db-1", "payload": {"page_size": 1}})]


def test_cli_command_modules_do_not_import_notion_sdk() -> None:
    for module in [pages, blocks, databases]:
        assert "notion_client" not in inspect.getsource(module)
