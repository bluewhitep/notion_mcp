from typer.testing import CliRunner

from notion_mcp.cli import app

from .helpers import plain_cli_output


runner = CliRunner()


def test_root_help_describes_direct_commands() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "init" in result.stdout
    assert "Initialize project-local .notion_mcp context" in result.stdout
    assert "status" in result.stdout
    assert "Show global configuration and capability status" in result.stdout
    assert "server" in result.stdout
    assert "Manage the local MCP server" in result.stdout
    assert "set-token" not in result.stdout
    assert "set-user" not in result.stdout
    assert "Show legacy global configuration" not in result.stdout
    assert "Run the legacy FastAPI REST server" not in result.stdout


def test_short_help_option_matches_root_help() -> None:
    result = runner.invoke(app, ["-h"])
    output = plain_cli_output(result.stdout)

    assert result.exit_code == 0
    assert "Usage:" in output
    assert "--help" in output
    assert "-h" in output
    assert "init" in output


def test_short_help_option_reaches_subcommands() -> None:
    server_result = runner.invoke(app, ["server", "run", "-h"])
    config_result = runner.invoke(app, ["config", "global", "-h"])
    server_output = plain_cli_output(server_result.stdout)
    config_output = plain_cli_output(config_result.stdout)

    assert server_result.exit_code == 0
    assert "--help" in server_output
    assert "-h" in server_output
    assert "--host" in server_output

    assert config_result.exit_code == 0
    assert "--help" in config_output
    assert "-h" in config_output
    assert "Set a global configuration value" in config_output


def test_project_and_config_help_describe_dynamic_subcommands() -> None:
    project_result = runner.invoke(app, ["project", "--help"])
    config_global_result = runner.invoke(app, ["config", "global", "--help"])
    config_local_result = runner.invoke(app, ["config", "local", "--help"])

    assert project_result.exit_code == 0
    assert "Create .notion_mcp project context" in project_result.stdout
    assert "Show project-local context status" in project_result.stdout
    assert "Print resolved project root" in project_result.stdout

    assert config_global_result.exit_code == 0
    assert "Set a global configuration value" in config_global_result.stdout
    assert "Get a global configuration value" in config_global_result.stdout
    assert "Unset a nullable global configuration value" in config_global_result.stdout
    assert "List global configuration values" in config_global_result.stdout

    assert config_local_result.exit_code == 0
    assert "Create .notion_mcp project context" in config_local_result.stdout
    assert "Show project-local context status" in config_local_result.stdout
    assert "Print resolved project root" in config_local_result.stdout
