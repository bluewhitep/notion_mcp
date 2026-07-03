import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from nilo.cli import app
from nilo.cli.commands import auth as auth_commands
from tests.v2.fixtures.fake_notion import FakeNotionClient


runner = CliRunner()


def test_full_local_config_and_mock_auth_flow(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("NOTION_MCP_CONFIG", str(tmp_path / "config.json"))

    token_result = runner.invoke(app, ["config", "global", "set", "notion_token", "secret-token"])
    name_result = runner.invoke(app, ["config", "global", "set", "user_name", "Ada"])
    status_result = runner.invoke(app, ["status", "--json"])
    monkeypatch.setattr(
        auth_commands,
        "create_notion_client",
        lambda config: FakeNotionClient(user_name="Ada"),
    )
    auth_result = runner.invoke(app, ["auth", "validate", "--json"])

    assert token_result.exit_code == 0
    assert name_result.exit_code == 0
    assert status_result.exit_code == 0
    assert auth_result.exit_code == 0
    assert json.loads(status_result.stdout)["configured"] is True
    assert json.loads(auth_result.stdout)["valid"] is True
