# File: src/notion_mcp/cli/commands/data_sources.py
# Format: UTF-8
# =============================
# File Description:
# CLI data source commands backed by Core data source service.
# TAG: cli, data-sources
# =============================

from __future__ import annotations

import typer

from notion_mcp.core.errors import CoreError
from notion_mcp.core.models import dry_run_result

from ..core_services import get_data_sources_service as _get_data_sources_service
from ..formatting import echo_json, exit_with_error, parse_json_object

app = typer.Typer(add_completion=False, help="Data source operations")


def register(root_app: typer.Typer) -> None:
    root_app.add_typer(app, name="data-source")
    root_app.add_typer(app, name="data-sources")


def get_data_sources_service():
    return _get_data_sources_service()


@app.command(name="retrieve")
def retrieve(data_source_id: str, json_output: bool = typer.Option(False, "--json")) -> None:
    try:
        result = get_data_sources_service().retrieve(data_source_id)
    except CoreError as exc:
        exit_with_error(exc, json_output=json_output)
    echo_json(result) if json_output else typer.echo(result)


@app.command(name="query")
def query(
    data_source_id: str,
    payload: str = typer.Option("{}", "--payload"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    data = parse_json_object(payload)
    if dry_run:
        result = dry_run_result("data_sources.query", {"data_source_id": data_source_id, **data}).__dict__
    else:
        try:
            result = get_data_sources_service().query(data_source_id, data)
        except CoreError as exc:
            exit_with_error(exc, json_output=json_output)
    echo_json(result) if json_output else typer.echo(result)


@app.command(name="create")
def create(
    payload: str = typer.Option(..., "--payload"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    data = parse_json_object(payload)
    if dry_run:
        result = dry_run_result("data_sources.create", data).__dict__
    else:
        try:
            result = get_data_sources_service().create(data)
        except CoreError as exc:
            exit_with_error(exc, json_output=json_output)
    echo_json(result) if json_output else typer.echo(result)


@app.command(name="update")
def update(
    data_source_id: str,
    payload: str = typer.Option(..., "--payload"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    json_output: bool = typer.Option(False, "--json"),
) -> None:
    data = parse_json_object(payload)
    if dry_run:
        result = dry_run_result("data_sources.update", {"data_source_id": data_source_id, **data}).__dict__
    else:
        try:
            result = get_data_sources_service().update(data_source_id, data)
        except CoreError as exc:
            exit_with_error(exc, json_output=json_output)
    echo_json(result) if json_output else typer.echo(result)
