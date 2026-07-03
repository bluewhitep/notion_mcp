import json

from typer.testing import CliRunner

from nilo.cli import app


runner = CliRunner()


def test_database_detach_and_deattach_remove_local_state_only(monkeypatch, tmp_path) -> None:
    monkeypatch.chdir(tmp_path)
    attach = runner.invoke(
        app,
        ["database", "attach", "db-1", "--no-verify", "--title", "Manual Database", "--json"],
    )
    assert attach.exit_code == 0
    state_file = tmp_path / ".notion_mcp" / "state" / "database.attach.json"
    assert state_file.exists()

    detach = runner.invoke(app, ["database", "detach", "--json"])

    assert detach.exit_code == 0
    assert not state_file.exists()
    assert json.loads(detach.stdout)["previous_database"]["id"] == "db-1"

    attach_again = runner.invoke(
        app,
        ["database", "attach", "db-2", "--no-verify", "--title", "Second Database"],
    )
    assert attach_again.exit_code == 0

    deattach = runner.invoke(app, ["database", "deattach"])

    assert deattach.exit_code == 0
    assert not state_file.exists()
    assert "Detached database" in deattach.stdout
