# File: src/nilo/cli/formatting.py
# Format: UTF-8
# =============================
# File Description:
# CLI output and parsing helpers shared by command modules.
# TAG: cli, formatting
# =============================

from __future__ import annotations

import json
from typing import Any

import typer

from nilo.core.errors import CoreError


# --------------------------------
# Function Description:
# Writes JSON output to stdout.
# Inputs/Outputs:
# Input JSON-serializable value; output is printed text.
# Usage:
# echo_json({"ok": True})
# --------------------------------
def echo_json(value: Any) -> None:
    typer.echo(json.dumps(value, ensure_ascii=False))


# --------------------------------
# Function Description:
# Handles Core errors for plain or JSON CLI modes.
# Inputs/Outputs:
# Input error and mode flag; raises typer.Exit after printing.
# Usage:
# exit_with_error(error, json_output=True)
# --------------------------------
def exit_with_error(error: CoreError, *, json_output: bool = False) -> None:
    if json_output:
        echo_json({"ok": False, "error": error.to_dict()})
    else:
        typer.echo(f"Error: {error.message}")
    raise typer.Exit(code=1)


# --------------------------------
# Function Description:
# Parses a JSON object supplied to a CLI option.
# Inputs/Outputs:
# Input JSON string; returns dictionary or raises typer.BadParameter.
# Usage:
# parse_json_object('{"page_size": 1}')
# --------------------------------
def parse_json_object(raw: str | None) -> dict[str, Any]:
    if not raw:
        return {}
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise typer.BadParameter("payload must be valid JSON") from exc
    if not isinstance(value, dict):
        raise typer.BadParameter("payload must be a JSON object")
    return value
