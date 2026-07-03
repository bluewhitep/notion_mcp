import json
from pathlib import Path

import pytest

from nilo.config import (
    get_config_path,
    load_config,
    save_config,
    set_token,
    set_user,
)
from nilo.models import Config


def test_save_and_load_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """保存后能正确读取配置。"""
    cfg_file = tmp_path / "config.json"
    monkeypatch.setenv("NOTION_MCP_CONFIG", str(cfg_file))

    cfg = Config(notion_token="test-token", user_id="user-uuid")
    save_config(cfg)

    loaded = load_config()
    assert loaded.notion_token == "test-token"
    assert loaded.user_id == "user-uuid"


def test_set_token_and_user(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """调用 set_token 与 set_user 能正确修改配置文件。"""
    cfg_file = tmp_path / "config.json"
    monkeypatch.setenv("NOTION_MCP_CONFIG", str(cfg_file))

    # 初始写入 token
    set_token("abc")
    cfg = load_config()
    assert cfg.notion_token == "abc"
    assert cfg.user_id is None

    # 更新用户
    set_user("uid123")
    cfg2 = load_config()
    assert cfg2.notion_token == "abc"
    assert cfg2.user_id == "uid123"