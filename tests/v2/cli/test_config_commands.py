import json
import uuid
from pathlib import Path

import pytest
from typer.testing import CliRunner

from notion_mcp.cli import app
from notion_mcp.core.config import init_core_config, load_core_config


runner = CliRunner()


def test_config_get_set_unset_and_list_json(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    cfg_file = tmp_path / "config.json"
    monkeypatch.setenv("NOTION_MCP_CONFIG", str(cfg_file))
    init_core_config(
        notion_token="secret-token",
        user_name="Ada",
        user_id=str(uuid.uuid4()),
    )

    set_result = runner.invoke(app, ["config", "set", "user_name", "Grace"])
    assert set_result.exit_code == 0
    assert load_core_config().user_name == "Grace"

    get_result = runner.invoke(app, ["config", "get", "user_name", "--json"])
    assert get_result.exit_code == 0
    assert json.loads(get_result.stdout) == {"key": "user_name", "value": "Grace"}

    token_result = runner.invoke(app, ["config", "get", "notion_token", "--json"])
    assert token_result.exit_code == 0
    assert "secret-token" not in token_result.stdout
    assert json.loads(token_result.stdout)["value"] == "********"

    list_result = runner.invoke(app, ["config", "list", "--json"])
    assert list_result.exit_code == 0
    listed = json.loads(list_result.stdout)
    assert listed["notion_token_set"] is True
    assert listed["notion_token"] == "********"

    unset_result = runner.invoke(app, ["config", "unset", "user_name"])
    assert unset_result.exit_code == 0
    assert load_core_config().user_name is None


def test_config_rejects_unknown_key(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NOTION_MCP_CONFIG", str(tmp_path / "config.json"))

    result = runner.invoke(app, ["config", "set", "unknown", "value"])

    assert result.exit_code != 0
    assert "unknown" in result.stdout or "unknown" in str(result.exception)
