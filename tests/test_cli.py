from pathlib import Path

import pytest
from typer.testing import CliRunner

from notion_mcp.cli import app as cli_app
from notion_mcp.config import load_config


runner = CliRunner()


def test_config_global_set_creates_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cfg_file = tmp_path / "config.json"
    monkeypatch.setenv("NOTION_MCP_CONFIG", str(cfg_file))
    result = runner.invoke(cli_app, ["config", "global", "set", "notion_token", "abc"])
    assert result.exit_code == 0
    cfg = load_config(path=cfg_file)
    assert cfg.notion_token == "abc"


def test_set_token_and_user_commands(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cfg_file = tmp_path / "config.json"
    monkeypatch.setenv("NOTION_MCP_CONFIG", str(cfg_file))

    # 修改 token
    result_token = runner.invoke(cli_app, ["set-token", "--token", "newtoken"])
    assert result_token.exit_code == 0
    cfg = load_config(path=cfg_file)
    assert cfg.notion_token == "newtoken"
    # 修改用户
    result_user = runner.invoke(cli_app, ["set-user", "--user", "newuid"])
    assert result_user.exit_code == 0
    cfg2 = load_config(path=cfg_file)
    assert cfg2.user_id == "newuid"


def test_show_without_config(monkeypatch: pytest.MonkeyPatch) -> None:
    """当配置不存在时，show 命令应返回错误码。"""
    runner = CliRunner()
    # 使用不存在的临时路径
    monkeypatch.setenv("NOTION_MCP_CONFIG", "/tmp/nonexistent/config.json")
    result = runner.invoke(cli_app, ["show"])
    # TyperExit 会产生退出码 1
    assert result.exit_code != 0
