import json
import stat
import uuid
from pathlib import Path

import pytest
from typer.testing import CliRunner

from notion_mcp.cli import app
from notion_mcp.core.config import DEFAULT_NOTION_VERSION, load_core_config


runner = CliRunner()


def test_init_noninteractive_writes_core_config_and_secure_permissions(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    cfg_file = tmp_path / "config.json"
    user_id = str(uuid.uuid4())
    monkeypatch.setenv("NOTION_MCP_CONFIG", str(cfg_file))

    result = runner.invoke(
        app,
        [
            "init",
            "--token",
            "secret-token",
            "--user-name",
            "Ada",
            "--user-id",
            user_id,
            "--json",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["config"]["notion_token_set"] is True
    assert "secret-token" not in result.stdout
    assert stat.S_IMODE(cfg_file.stat().st_mode) == 0o600

    cfg = load_core_config(path=cfg_file)
    assert cfg.notion_token == "secret-token"
    assert cfg.user_name == "Ada"
    assert cfg.user_id == user_id
    assert cfg.notion_version == DEFAULT_NOTION_VERSION


def test_init_rejects_invalid_user_uuid(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NOTION_MCP_CONFIG", str(tmp_path / "config.json"))

    result = runner.invoke(
        app,
        [
            "init",
            "--token",
            "secret-token",
            "--user-name",
            "Ada",
            "--user-id",
            "not-a-uuid",
        ],
    )

    assert result.exit_code != 0
    assert "user_id" in result.stdout or "user_id" in str(result.exception)
