# File: src/notion_mcp/cli/commands/blocks.py
# Format: UTF-8
# =============================
# File Description:
# CLI block commands backed by Core block service.
# TAG: cli, blocks
# =============================

from __future__ import annotations

import typer

from notion_mcp.core.errors import CoreError
from notion_mcp.core.models import dry_run_result

from ..core_services import get_blocks_service as _get_blocks_service
from ..formatting import echo_json, exit_with_error, parse_json_object

app = typer.Typer(add_completion=False, help="Block operations")


# --------------------------------
# Function Description:
# Registers block command aliases.
# Inputs/Outputs:
# Input root Typer app; output is app with block/blocks subcommands.
# Usage:
# register(root_app)
# --------------------------------
def register(root_app: typer.Typer) -> None:
    root_app.add_typer(app, name="block")
    root_app.add_typer(app, name="blocks")


# --------------------------------
# Function Description:
# Returns the Core blocks service.
# Inputs/Outputs:
# No input; returns BlocksService.
# Usage:
# get_blocks_service().list_children("block-id")
# --------------------------------
def get_blocks_service():
    return _get_blocks_service()


@app.command(name="children")
# --------------------------------
# Function Description:
# Lists child blocks through Core.
# Inputs/Outputs:
# Input block_id and JSON flag; output is children list response.
# Usage:
# notion-mcp block children BLOCK_ID --json
# --------------------------------
def children(
    block_id: str,
    json_output: bool = typer.Option(False, "--json", help="Print JSON output"),
) -> None:
    try:
        result = get_blocks_service().list_children(block_id)
    except CoreError as exc:
        exit_with_error(exc, json_output=json_output)
    if json_output:
        echo_json(result)
    else:
        typer.echo(result)


@app.command(name="append")
# --------------------------------
# Function Description:
# Appends child blocks through Core or prints dry-run payload.
# Inputs/Outputs:
# Input block_id and JSON payload; output is append response or dry-run result.
# Usage:
# notion-mcp block append BLOCK_ID --payload '{"children": []}' --dry-run
# --------------------------------
def append(
    block_id: str,
    payload: str = typer.Option(..., "--payload", help="JSON payload with children/position"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Do not call Notion"),
    json_output: bool = typer.Option(False, "--json", help="Print JSON output"),
) -> None:
    data = parse_json_object(payload)
    children_payload = data.get("children", [])
    children_list = children_payload if isinstance(children_payload, list) else []
    position = data.get("position")
    if dry_run:
        result = dry_run_result("blocks.children.append", {"block_id": block_id, **data}).__dict__
    else:
        try:
            result = get_blocks_service().append_children(
                block_id,
                children=children_list,
                position=position if isinstance(position, dict) else None,
            )
        except CoreError as exc:
            exit_with_error(exc, json_output=json_output)
    if json_output:
        echo_json(result)
    else:
        typer.echo(result)
