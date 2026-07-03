import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from nilo.cli import app


runner = CliRunner()


def test_root_init_creates_project_config_without_touching_global_config(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    global_config = tmp_path / "global-config.json"
    monkeypatch.setenv("NOTION_MCP_CONFIG", str(global_config))
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["init", "--project-name", "Demo", "--workspace-hint", "Sandbox", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["project_root"] == str(tmp_path)
    assert payload["stores_tokens"] is False

    project_config = tmp_path / ".notion_mcp" / "config.json"
    assert project_config.exists()
    assert (tmp_path / ".notion_mcp" / "state").is_dir()
    assert (tmp_path / ".notion_mcp" / "cache").is_dir()
    assert (tmp_path / ".notion_mcp" / "logs").is_dir()
    raw = project_config.read_text(encoding="utf-8")
    data = json.loads(raw)
    assert data["project_name"] == "Demo"
    assert data["workspace_hint"] == "Sandbox"
    assert "token" not in raw.lower()
    assert not global_config.exists()


def test_root_init_rejects_global_token_options(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    global_config = tmp_path / "global-config.json"
    monkeypatch.setenv("NOTION_MCP_CONFIG", str(global_config))
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["init", "--token", "secret-token"])

    assert result.exit_code != 0
    assert not (tmp_path / ".notion_mcp" / "config.json").exists()
    assert not global_config.exists()
