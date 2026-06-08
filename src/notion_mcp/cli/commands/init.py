# File: src/notion_mcp/cli/commands/init.py
# Format: UTF-8
# =============================
# File Description:
# CLI init command backed by Core configuration.
# TAG: cli, init, config
# =============================

from __future__ import annotations

import typer

from notion_mcp.config import save_config as save_legacy_config
from notion_mcp.core.config import (
    DEFAULT_NOTION_VERSION,
    config_path_from_env,
    init_core_config,
    redacted_config,
)
from notion_mcp.core.errors import ConfigValidationError
from notion_mcp.models import Config as LegacyConfig

from ..formatting import echo_json, exit_with_error


# --------------------------------
# Function Description:
# Registers the init command on a Typer app.
# Inputs/Outputs:
# Input Typer app; output is the app with init command attached.
# Usage:
# register(app)
# --------------------------------
def register(app: typer.Typer) -> None:
    app.command(name="init")(init_command)


# --------------------------------
# Function Description:
# Initializes local configuration for the Notion MCP tool.
# Inputs/Outputs:
# Input token/user metadata/options; output is CLI text or JSON.
# Usage:
# notion-mcp init --token ... --user-name Ada --user-id ...
# --------------------------------
def init_command(
    token: str = typer.Option(None, "--token", prompt="请输入 Notion 集成 token", hide_input=True),
    user_name: str | None = typer.Option(None, "--user-name", help="Notion user display name"),
    user_id: str | None = typer.Option(None, "--user-id", help="Notion user UUID"),
    legacy_user: str | None = typer.Option(
        None,
        "--user",
        help="Legacy alias for --user-id",
    ),
    notion_version: str = typer.Option(
        DEFAULT_NOTION_VERSION,
        "--notion-version",
        help="Notion API version",
    ),
    json_output: bool = typer.Option(False, "--json", help="Print JSON output"),
) -> None:
    effective_user_id = user_id or legacy_user
    effective_user_name = user_name or ""
    if not effective_user_id:
        effective_user_id = typer.prompt("请输入当前 Notion 用户 UUID")
    try:
        config = init_core_config(
            notion_token=token,
            user_name=effective_user_name,
            user_id=effective_user_id,
            notion_version=notion_version,
        )
    except ConfigValidationError as exc:
        if legacy_user and not user_id and not user_name:
            save_legacy_config(LegacyConfig(notion_token=token, user_id=legacy_user))
            typer.echo(f"配置已保存至 {config_path_from_env()}")
            return
        exit_with_error(exc, json_output=json_output)
    if json_output:
        echo_json({"ok": True, "path": str(config_path_from_env()), "config": redacted_config(config)})
    else:
        typer.echo(f"配置已保存至 {config_path_from_env()}")
