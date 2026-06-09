import json

from typer.testing import CliRunner

from notion_mcp.cli import app
from notion_mcp.cli.commands import databases


runner = CliRunner()


class FakeDatabasesService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def retrieve(self, database_id: str) -> dict[str, object]:
        self.calls.append(("retrieve", database_id))
        return {
            "id": database_id,
            "title": [{"plain_text": "Refreshed Database"}],
            "url": "https://www.notion.so/refreshed",
            "is_inline": False,
            "archived": False,
            "in_trash": False,
            "data_sources": [{"id": "ds-1", "name": "Tasks"}],
        }


def test_database_status_current_refresh_and_json(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(databases, "get_databases_service", lambda: FakeDatabasesService())
    monkeypatch.chdir(tmp_path)

    attach = runner.invoke(
        app,
        ["database", "attach", "db-1", "--no-verify", "--title", "Manual Database", "--json"],
    )
    assert attach.exit_code == 0

    status = runner.invoke(app, ["database", "status", "--json"])
    current = runner.invoke(app, ["database", "current"])
    refresh = runner.invoke(app, ["database", "refresh", "--json"])

    assert status.exit_code == 0
    assert current.exit_code == 0
    assert refresh.exit_code == 0
    assert json.loads(status.stdout)["attachment"]["database"]["title"] == "Manual Database"
    assert "Attached database" in current.stdout
    assert json.loads(refresh.stdout)["attachment"]["database"]["title"] == "Refreshed Database"
    assert json.loads(refresh.stdout)["attachment"]["active_data_source"]["id"] == "ds-1"
