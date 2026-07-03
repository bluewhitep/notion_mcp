import json
from pathlib import Path

from typer.testing import CliRunner

from nilo.cli import app


runner = CliRunner()


def test_raw_api_operations_remain_available() -> None:
    result = runner.invoke(app, ["raw-api", "operations", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert "pages.create" in payload["operations"]
    assert "data_sources.query" in payload["operations"]


def test_common_page_database_workflows_have_dedicated_cli_commands() -> None:
    for command in [
        ["page", "retrieve", "--help"],
        ["page", "blocks", "--help"],
        ["block", "update", "--help"],
        ["block", "trash", "--help"],
        ["database", "query", "--help"],
        ["database", "page", "create", "--help"],
        ["data-source", "query", "--help"],
    ]:
        result = runner.invoke(app, command)
        assert result.exit_code == 0, result.output


def test_raw_api_help_positions_it_as_advanced_fallback() -> None:
    result = runner.invoke(app, ["raw-api", "--help"])

    assert result.exit_code == 0
    help_text = result.output.lower()
    assert "advanced" in help_text
    assert "fallback" in help_text


def test_user_docs_position_raw_api_as_advanced_not_common_page_database_path() -> None:
    user_cli_paths = [
        Path("Docs/EN/User/Cli.md"),
        *sorted(Path("Docs/EN/User/Cli").glob("*.md")),
    ]
    user_cli = "\n".join(path.read_text(encoding="utf-8") for path in user_cli_paths)

    assert "Raw API is an advanced fallback entrypoint" in user_cli
    assert "nilo block update" in user_cli
    assert "nilo database query --payload" in user_cli
