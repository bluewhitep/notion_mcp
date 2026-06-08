# File: src/notion_mcp/cli/commands/config.py
# Format: UTF-8
# =============================
# File Description:
# Git-like CLI configuration commands backed by Core config.
# TAG: cli, config
# =============================

from __future__ import annotations

from typing import Any

import typer

from notion_mcp.core.config import CoreConfig, load_core_config, redacted_config, save_core_config
from notion_mcp.core.errors import ConfigNotFoundError, ConfigValidationError

from ..formatting import echo_json, exit_with_error

app = typer.Typer(add_completion=False, help="Read and update local configuration")
CONFIG_FIELDS = set(CoreConfig.model_fields)


# --------------------------------
# Function Description:
# Registers the config sub-application.
# Inputs/Outputs:
# Input root Typer app; output is app with config commands attached.
# Usage:
# register(root_app)
# --------------------------------
def register(root_app: typer.Typer) -> None:
    root_app.add_typer(app, name="config")


# --------------------------------
# Function Description:
# Validates a CoreConfig field name.
# Inputs/Outputs:
# Input key string; returns key or raises typer.BadParameter.
# Usage:
# require_known_key("user_name")
# --------------------------------
def require_known_key(key: str) -> str:
    if key not in CONFIG_FIELDS:
        typer.echo(f"unknown config key: {key}")
        raise typer.Exit(code=1)
    return key


# --------------------------------
# Function Description:
# Casts string CLI values to the target CoreConfig field type.
# Inputs/Outputs:
# Input key/value strings; returns typed value.
# Usage:
# cast_value("retry", "false")
# --------------------------------
def cast_value(key: str, value: str) -> Any:
    if key in {"retry", "audit_enabled"}:
        return value.lower() in {"1", "true", "yes", "on"}
    if key == "timeout_ms":
        return int(value)
    return value


@app.command(name="set")
# --------------------------------
# Function Description:
# Sets a Core configuration key.
# Inputs/Outputs:
# Input key and value; output is human text or JSON.
# Usage:
# notion-mcp config set user_name Ada
# --------------------------------
def set_value(
    key: str,
    value: str,
    json_output: bool = typer.Option(False, "--json", help="Print JSON output"),
) -> None:
    require_known_key(key)
    try:
        config = load_core_config()
    except ConfigNotFoundError:
        config = CoreConfig()
    current = config.model_dump()
    current[key] = cast_value(key, value)
    try:
        updated = CoreConfig(**current)
        save_core_config(updated)
    except ConfigValidationError as exc:
        exit_with_error(exc, json_output=json_output)
    if json_output:
        echo_json({"ok": True, "key": key})
    else:
        typer.echo(f"{key} 已更新")


@app.command(name="get")
# --------------------------------
# Function Description:
# Gets a Core configuration key with token redaction by default.
# Inputs/Outputs:
# Input key; output is human text or JSON.
# Usage:
# notion-mcp config get user_name --json
# --------------------------------
def get_value(
    key: str,
    json_output: bool = typer.Option(False, "--json", help="Print JSON output"),
    show_secret: bool = typer.Option(False, "--show-secret", help="Print secret values"),
) -> None:
    require_known_key(key)
    try:
        config = load_core_config()
    except ConfigNotFoundError as exc:
        exit_with_error(exc, json_output=json_output)
    if key == "notion_token" and not show_secret:
        value: Any = "********" if config.notion_token else None
    else:
        value = getattr(config, key)
    if json_output:
        echo_json({"key": key, "value": value})
    else:
        typer.echo(f"{key}={value}")


@app.command(name="unset")
# --------------------------------
# Function Description:
# Clears a nullable Core configuration key.
# Inputs/Outputs:
# Input key; output is human text or JSON.
# Usage:
# notion-mcp config unset user_name
# --------------------------------
def unset_value(
    key: str,
    json_output: bool = typer.Option(False, "--json", help="Print JSON output"),
) -> None:
    require_known_key(key)
    if key in {"notion_version", "timeout_ms", "retry", "default_transport", "audit_enabled"}:
        raise typer.BadParameter(f"{key} cannot be unset")
    try:
        config = load_core_config()
    except ConfigNotFoundError as exc:
        exit_with_error(exc, json_output=json_output)
    current = config.model_dump()
    current[key] = None
    updated = CoreConfig(**current)
    save_core_config(updated)
    if json_output:
        echo_json({"ok": True, "key": key})
    else:
        typer.echo(f"{key} 已清空")


@app.command(name="list")
# --------------------------------
# Function Description:
# Lists local Core configuration with secret redaction.
# Inputs/Outputs:
# Optional JSON flag; output is human text or JSON.
# Usage:
# notion-mcp config list --json
# --------------------------------
def list_values(json_output: bool = typer.Option(False, "--json", help="Print JSON output")) -> None:
    try:
        config = load_core_config()
    except ConfigNotFoundError as exc:
        exit_with_error(exc, json_output=json_output)
    public = redacted_config(config)
    if json_output:
        echo_json(public)
    else:
        for key, value in public.items():
            typer.echo(f"{key}={value}")
