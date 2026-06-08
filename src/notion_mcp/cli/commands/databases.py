# File: src/notion_mcp/cli/commands/databases.py
# Format: UTF-8
# =============================
# File Description:
# CLI database commands backed by Core database service.
# TAG: cli, databases
# =============================

from __future__ import annotations

import typer

from notion_mcp.core.errors import CoreError
from notion_mcp.core.models import dry_run_result

from ..core_services import get_databases_service as _get_databases_service
from ..formatting import echo_json, exit_with_error, parse_json_object

app = typer.Typer(add_completion=False, help="Database operations")


# --------------------------------
# Function Description:
# Registers database command aliases.
# Inputs/Outputs:
# Input root Typer app; output is app with database/databases subcommands.
# Usage:
# register(root_app)
# --------------------------------
def register(root_app: typer.Typer) -> None:
    root_app.add_typer(app, name="database")
    root_app.add_typer(app, name="databases")


# --------------------------------
# Function Description:
# Returns the Core databases service.
# Inputs/Outputs:
# No input; returns DatabasesService.
# Usage:
# get_databases_service().query("database-id", {})
# --------------------------------
def get_databases_service():
    return _get_databases_service()


@app.command(name="retrieve")
# --------------------------------
# Function Description:
# Retrieves a legacy Notion database through Core.
# Inputs/Outputs:
# Input database_id and JSON flag; output is database response.
# Usage:
# notion-mcp database retrieve DATABASE_ID --json
# --------------------------------
def retrieve(
    database_id: str,
    json_output: bool = typer.Option(False, "--json", help="Print JSON output"),
) -> None:
    try:
        result = get_databases_service().retrieve(database_id)
    except CoreError as exc:
        exit_with_error(exc, json_output=json_output)
    if json_output:
        echo_json(result)
    else:
        typer.echo(result)


@app.command(name="query")
# --------------------------------
# Function Description:
# Queries a legacy Notion database through Core.
# Inputs/Outputs:
# Input database_id and JSON payload; output is query response or dry-run result.
# Usage:
# notion-mcp database query DATABASE_ID --payload '{"page_size": 1}' --json
# --------------------------------
def query(
    database_id: str,
    payload: str = typer.Option("{}", "--payload", help="JSON payload for databases.query"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Do not call Notion"),
    json_output: bool = typer.Option(False, "--json", help="Print JSON output"),
) -> None:
    data = parse_json_object(payload)
    if dry_run:
        result = dry_run_result("databases.query", {"database_id": database_id, **data}).__dict__
    else:
        try:
            result = get_databases_service().query(database_id, data)
        except CoreError as exc:
            exit_with_error(exc, json_output=json_output)
    if json_output:
        echo_json(result)
    else:
        typer.echo(result)
