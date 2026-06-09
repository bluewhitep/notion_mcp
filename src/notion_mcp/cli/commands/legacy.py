# File: src/notion_mcp/cli/commands/legacy.py
# Format: UTF-8
# =============================
# File Description:
# Legacy CLI compatibility commands retained for existing tests and users.
# TAG: cli, legacy
# =============================

from __future__ import annotations

import typer

from notion_mcp.config import get_config_path, load_config, set_token, set_user


# --------------------------------
# Function Description:
# Registers legacy CLI commands.
# Inputs/Outputs:
# Input Typer app; output is app with legacy commands attached.
# Usage:
# register(app)
# --------------------------------
def register(app: typer.Typer) -> None:
    app.command(
        name="set-token",
        help="Set the legacy global Notion token",
    )(set_token_command)
    app.command(
        name="set-user",
        help="Set the legacy global Notion user id",
    )(set_user_command)
    app.command(
        name="show",
        help="Show legacy global configuration",
    )(show_command)
    app.command(
        name="run",
        help="Run the legacy FastAPI REST server",
    )(run_command)


# --------------------------------
# Function Description:
# Updates the legacy Notion token field.
# Inputs/Outputs:
# Input token; output is human text.
# Usage:
# notion-mcp set-token --token secret
# --------------------------------
def set_token_command(
    token: str = typer.Option(..., "--token", prompt="Enter the new Notion token", hide_input=True),
) -> None:
    set_token(token)
    typer.echo("Notion token updated")


# --------------------------------
# Function Description:
# Updates the legacy user id field.
# Inputs/Outputs:
# Input user value; output is human text.
# Usage:
# notion-mcp set-user --user uuid
# --------------------------------
def set_user_command(
    user: str = typer.Option(..., "--user", prompt="Enter the new user UUID"),
) -> None:
    set_user(user)
    typer.echo("User ID updated")


# --------------------------------
# Function Description:
# Shows legacy config content with existing behavior.
# Inputs/Outputs:
# No input; output is human text or exit code 1 when missing.
# Usage:
# notion-mcp show
# --------------------------------
def show_command() -> None:
    try:
        cfg = load_config()
    except FileNotFoundError:
        typer.echo("Global configuration is not set. Run: notion-mcp config --global user.token <token>")
        raise typer.Exit(code=1)
    typer.echo(f"Current configuration file: {get_config_path()}")
    typer.echo(f"Notion token: {cfg.notion_token}\nUser UUID: {cfg.user_id}")


# --------------------------------
# Function Description:
# Starts the legacy FastAPI REST server.
# Inputs/Outputs:
# Input host/port/reload options; output is uvicorn process startup.
# Usage:
# notion-mcp run --host 127.0.0.1 --port 8000
# --------------------------------
def run_command(
    host: str = typer.Option("127.0.0.1", "--host", help="Bind address"),
    port: int = typer.Option(8000, "--port", help="Bind port"),
    reload: bool = typer.Option(False, "--reload", help="Enable auto-reload"),
) -> None:
    try:
        import uvicorn
    except ImportError:
        typer.echo("uvicorn is required for the legacy REST server")
        raise typer.Exit(code=1)
    from notion_mcp.server import app as fastapi_app

    uvicorn.run(
        fastapi_app,
        host=host,
        port=port,
        reload=reload,
        log_level="info",
    )
