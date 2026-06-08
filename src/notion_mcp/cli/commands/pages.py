# File: src/notion_mcp/cli/commands/pages.py
# Format: UTF-8
# =============================
# File Description:
# CLI page commands backed by Core page service.
# TAG: cli, pages
# =============================

from __future__ import annotations

import typer

from notion_mcp.core.errors import CoreError
from notion_mcp.core.models import dry_run_result

from ..core_services import get_pages_service as _get_pages_service
from ..formatting import echo_json, exit_with_error, parse_json_object

app = typer.Typer(add_completion=False, help="Page operations")


# --------------------------------
# Function Description:
# Registers page command aliases.
# Inputs/Outputs:
# Input root Typer app; output is app with page/pages subcommands.
# Usage:
# register(root_app)
# --------------------------------
def register(root_app: typer.Typer) -> None:
    root_app.add_typer(app, name="page")
    root_app.add_typer(app, name="pages")


# --------------------------------
# Function Description:
# Returns the Core pages service.
# Inputs/Outputs:
# No input; returns PagesService.
# Usage:
# get_pages_service().retrieve("page-id")
# --------------------------------
def get_pages_service():
    return _get_pages_service()


@app.command(name="retrieve")
# --------------------------------
# Function Description:
# Retrieves a Notion page through Core.
# Inputs/Outputs:
# Input page_id and JSON flag; output is page response.
# Usage:
# notion-mcp page retrieve PAGE_ID --json
# --------------------------------
def retrieve_page(
    page_id: str,
    json_output: bool = typer.Option(False, "--json", help="Print JSON output"),
) -> None:
    try:
        result = get_pages_service().retrieve(page_id)
    except CoreError as exc:
        exit_with_error(exc, json_output=json_output)
    if json_output:
        echo_json(result)
    else:
        typer.echo(result)


@app.command(name="create")
# --------------------------------
# Function Description:
# Creates a Notion page through Core or prints dry-run payload.
# Inputs/Outputs:
# Input JSON payload and dry-run flag; output is create response or dry-run result.
# Usage:
# notion-mcp page create --payload '{"parent": {}}' --dry-run --json
# --------------------------------
def create_page(
    payload: str = typer.Option(..., "--payload", help="JSON payload for pages.create"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Do not call Notion"),
    json_output: bool = typer.Option(False, "--json", help="Print JSON output"),
) -> None:
    data = parse_json_object(payload)
    if dry_run:
        result = dry_run_result("pages.create", data).__dict__
    else:
        try:
            result = get_pages_service().create(data)
        except CoreError as exc:
            exit_with_error(exc, json_output=json_output)
    if json_output:
        echo_json(result)
    else:
        typer.echo(result)


@app.command(name="update")
# --------------------------------
# Function Description:
# Updates a Notion page through Core or prints dry-run payload.
# Inputs/Outputs:
# Input page_id, payload, and dry-run flag; output is update response or dry-run result.
# Usage:
# notion-mcp page update PAGE_ID --payload '{"properties": {}}'
# --------------------------------
def update_page(
    page_id: str,
    payload: str = typer.Option(..., "--payload", help="JSON payload for pages.update"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Do not call Notion"),
    json_output: bool = typer.Option(False, "--json", help="Print JSON output"),
) -> None:
    data = parse_json_object(payload)
    if dry_run:
        result = dry_run_result("pages.update", {"page_id": page_id, **data}).__dict__
    else:
        try:
            result = get_pages_service().update(page_id, data)
        except CoreError as exc:
            exit_with_error(exc, json_output=json_output)
    if json_output:
        echo_json(result)
    else:
        typer.echo(result)


@app.command(name="trash")
# --------------------------------
# Function Description:
# Moves a page to trash through Core or prints dry-run payload.
# Inputs/Outputs:
# Input page_id and dry-run flag; output is trash response or dry-run result.
# Usage:
# notion-mcp page trash PAGE_ID --dry-run
# --------------------------------
def trash_page(
    page_id: str,
    dry_run: bool = typer.Option(False, "--dry-run", help="Do not call Notion"),
    json_output: bool = typer.Option(False, "--json", help="Print JSON output"),
) -> None:
    if dry_run:
        result = dry_run_result("pages.trash", {"page_id": page_id}).__dict__
    else:
        try:
            result = get_pages_service().trash(page_id)
        except CoreError as exc:
            exit_with_error(exc, json_output=json_output)
    if json_output:
        echo_json(result)
    else:
        typer.echo(result)
