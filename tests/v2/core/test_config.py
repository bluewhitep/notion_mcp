import json
import stat
import uuid
from pathlib import Path

import pytest

from notion_mcp.core.config import (
    DEFAULT_NOTION_VERSION,
    CoreConfig,
    config_path_from_env,
    init_core_config,
    load_core_config,
    redacted_config,
    save_core_config,
    update_core_config,
)
from notion_mcp.core.errors import ConfigValidationError


def test_init_core_config_writes_secure_file_and_defaults(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    cfg_file = tmp_path / "config.json"
    user_id = str(uuid.uuid4())
    monkeypatch.setenv("NOTION_MCP_CONFIG", str(cfg_file))

    cfg = init_core_config(
        notion_token="secret-token",
        user_name="Ada",
        user_id=user_id,
    )

    assert cfg.notion_token == "secret-token"
    assert cfg.user_name == "Ada"
    assert cfg.user_id == user_id
    assert cfg.notion_version == DEFAULT_NOTION_VERSION
    assert cfg.default_transport == "stdio"
    assert cfg_file.exists()
    assert stat.S_IMODE(cfg_file.stat().st_mode) == 0o600

    stored = json.loads(cfg_file.read_text(encoding="utf-8"))
    assert stored["notion_token"] == "secret-token"
    assert stored["user_name"] == "Ada"
    assert stored["user_id"] == user_id
    assert stored["notion_version"] == DEFAULT_NOTION_VERSION


def test_load_update_and_path_override(tmp_path: Path) -> None:
    cfg_file = tmp_path / "custom" / "config.json"
    user_id = str(uuid.uuid4())
    save_core_config(
        CoreConfig(
            notion_token="token-a",
            user_name="Ada",
            user_id=user_id,
        ),
        path=cfg_file,
    )

    updated = update_core_config(
        path=cfg_file,
        notion_version="2025-09-03",
        timeout_ms=12345,
        retry=False,
    )

    assert updated.notion_token == "token-a"
    assert updated.user_name == "Ada"
    assert updated.user_id == user_id
    assert updated.notion_version == "2025-09-03"
    assert updated.timeout_ms == 12345
    assert updated.retry is False
    assert load_core_config(path=cfg_file).timeout_ms == 12345


def test_config_path_from_env_expands_user(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NOTION_MCP_CONFIG", "~/notion-test-config.json")

    assert config_path_from_env().name == "notion-test-config.json"
    assert str(config_path_from_env()).startswith(str(Path.home()))


def test_redacted_config_never_leaks_token() -> None:
    cfg = CoreConfig(
        notion_token="secret-token",
        user_name="Ada",
        user_id=str(uuid.uuid4()),
    )

    public = redacted_config(cfg)

    assert "secret-token" not in json.dumps(public)
    assert public["notion_token_set"] is True
    assert public["notion_token"] == "********"
    assert public["user_name"] == "Ada"


def test_user_id_must_be_uuid() -> None:
    with pytest.raises(ConfigValidationError):
        CoreConfig(
            notion_token="secret-token",
            user_name="Ada",
            user_id="not-a-uuid",
        )
