import json

from typer.testing import CliRunner

from nilo.cli import app
from nilo.cli.commands import databases


runner = CliRunner()


class ContainerOnlyDatabasesService:
    pass


class FakeRawApiService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, object]]] = []

    def invoke(self, operation: str, arguments: dict[str, object]) -> dict[str, object]:
        self.calls.append((operation, arguments))
        return {"operation": operation, "arguments": arguments}


def test_legacy_database_query_uses_raw_api_compatibility_path(monkeypatch) -> None:
    raw_service = FakeRawApiService()
    monkeypatch.setattr(databases, "get_databases_service", lambda: ContainerOnlyDatabasesService())
    monkeypatch.setattr(databases, "get_raw_api_service", lambda: raw_service)

    result = runner.invoke(
        app,
        ["database", "query", "db-1", "--payload", '{"page_size": 1}', "--json"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["operation"] == "databases.query"
    assert raw_service.calls == [("databases.query", {"database_id": "db-1", "page_size": 1})]
