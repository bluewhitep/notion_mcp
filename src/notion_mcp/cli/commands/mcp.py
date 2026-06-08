# File: src/notion_mcp/cli/commands/mcp.py
# Format: UTF-8
# =============================
# File Description:
# CLI MCP command group for starting the future MCP server.
# TAG: cli, mcp
# =============================

from __future__ import annotations

import typer

app = typer.Typer(add_completion=False, help="MCP server commands")


# --------------------------------
# Function Description:
# Registers MCP subcommands.
# Inputs/Outputs:
# Input root Typer app; output is app with mcp subcommands.
# Usage:
# register(root_app)
# --------------------------------
def register(root_app: typer.Typer) -> None:
    root_app.add_typer(app, name="mcp")


@app.command(name="serve")
# --------------------------------
# Function Description:
# Starts the MCP server once Stage 4 has implemented it.
# Inputs/Outputs:
# Input transport option; output is process startup or current not-implemented message.
# Usage:
# notion-mcp mcp serve --transport stdio
# --------------------------------
def serve(
    transport: str = typer.Option("stdio", "--transport", help="stdio or streamable-http"),
) -> None:
    try:
        from notion_mcp.mcp_server.server import serve as serve_mcp
    except ImportError:
        typer.echo(
            "MCP server is not implemented yet. Stage 4 will provide the real server.",
            err=True,
        )
        raise typer.Exit(code=1)
    serve_mcp(transport=transport)
