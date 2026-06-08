import json
import uuid
from pathlib import Path

import pytest
from typer.testing import CliRunner

from notion_mcp.cli import app
from notion_mcp.core.config import init_core_config


runner = CliRunner()


def test_status_json_has_stable_shape(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NOTION_MCP_CONFIG", str(tmp_path / "config.json"))
    init_core_config(
        notion_token="secret-token",
        user_name="Ada",
        user_id=str(uuid.uuid4()),
    )

    result = runner.invoke(app, ["status", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["configured"] is True
    assert payload["config"]["notion_token_set"] is True
    assert payload["config"]["notion_token"] == "********"
    assert payload["capabilities"]["core"] is True
    assert payload["capabilities"]["mcp_server"] is False
    assert "secret-token" not in result.stdout


def test_status_plain_output_is_human_readable_and_redacted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("NOTION_MCP_CONFIG", str(tmp_path / "config.json"))
    init_core_config(
        notion_token="secret-token",
        user_name="Ada",
        user_id=str(uuid.uuid4()),
    )

    result = runner.invoke(app, ["status"])

    assert result.exit_code == 0
    assert "Configured: yes" in result.stdout
    assert "Token: set" in result.stdout
    assert "secret-token" not in result.stdout
