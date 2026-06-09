import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from notion_mcp.cli import app


runner = CliRunner()


def test_project_status_and_root_work_from_child_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    init_result = runner.invoke(app, ["project", "init", "--project-name", "Demo"], catch_exceptions=False)
    assert init_result.exit_code == 0

    child = tmp_path / "src" / "module"
    child.mkdir(parents=True)
    monkeypatch.chdir(child)

    status = runner.invoke(app, ["project", "status", "--json"])
    root = runner.invoke(app, ["project", "root"])

    assert status.exit_code == 0
    payload = json.loads(status.stdout)
    assert payload["project_root"] == str(tmp_path)
    assert payload["config_file"] == str(tmp_path / ".notion_mcp" / "config.json")
    assert payload["config"]["project_name"] == "Demo"
    assert "notion_token" not in json.dumps(payload)
    assert root.exit_code == 0
    assert root.stdout.strip() == str(tmp_path)


def test_project_status_human_output_includes_config_paths(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    init_result = runner.invoke(app, ["project", "init", "--project-name", "Demo"])
    assert init_result.exit_code == 0

    status = runner.invoke(app, ["project", "status"])

    assert status.exit_code == 0
    assert "Project root:" in status.stdout
    assert str(tmp_path) in status.stdout
    assert ".notion_mcp/config.json" in status.stdout
    assert "Does not store Notion tokens: yes" in status.stdout


def test_project_status_reports_missing_project_context(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["project", "status"])

    assert result.exit_code == 1
    assert "No .notion_mcp/config.json found" in result.stdout
    assert "notion-mcp init" in result.stdout


def test_local_status_and_root_aliases_match_project_commands(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    init_result = runner.invoke(app, ["local", "init", "--project-name", "Alias"])
    assert init_result.exit_code == 0

    status = runner.invoke(app, ["local", "status", "--json"])
    root = runner.invoke(app, ["local", "root", "--json"])

    assert status.exit_code == 0
    assert json.loads(status.stdout)["project_root"] == str(tmp_path)
    assert root.exit_code == 0
    assert json.loads(root.stdout)["project_root"] == str(tmp_path)
