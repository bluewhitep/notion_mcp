from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]


def read_user_cli_docs() -> str:
    paths = [
        REPO_ROOT / "Docs/EN/User/Cli.md",
        *sorted((REPO_ROOT / "Docs/EN/User/Cli").glob("*.md")),
    ]
    return "\n".join(path.read_text(encoding="utf-8") for path in paths)


def test_user_cli_doc_lists_all_current_cli_commands() -> None:
    text = read_user_cli_docs()

    required_commands = [
        "nilo init",
        "nilo pwd",
        "nilo version",
        "nilo config --global --show",
        "nilo config --local --show",
        "nilo config --global user.token",
        "nilo config --global user.name",
        "nilo auth validate",
        "nilo auth whoami",
        "nilo page attach",
        "nilo page status",
        "nilo page refresh",
        "nilo page detach",
        "nilo page retrieve",
        "nilo page blocks",
        "nilo page create",
        "nilo page update",
        "nilo page trash",
        "nilo block children",
        "nilo block append",
        "nilo block insert-after",
        "nilo block update",
        "nilo block trash",
        "nilo database attach",
        "nilo database status",
        "nilo database refresh",
        "nilo database detach",
        "nilo database retrieve",
        "nilo database sources",
        "nilo database create",
        "nilo database update",
        "nilo database rename",
        "nilo database query",
        "nilo database page create",
        "nilo database property rename",
        "nilo data-source retrieve",
        "nilo data-source query",
        "nilo data-source create",
        "nilo data-source update",
        "nilo data-source templates",
        "nilo data-source property rename",
        "nilo data-source page create",
        "nilo user me",
        "nilo user list",
        "nilo user retrieve",
        "nilo comment list",
        "nilo comment create",
        "nilo comment reply",
        "nilo view retrieve",
        "nilo view list",
        "nilo view query",
        "nilo view create",
        "nilo view update",
        "nilo file-upload retrieve",
        "nilo file-upload list",
        "nilo file-upload create",
        "nilo file-upload send",
        "nilo file-upload complete",
        "nilo search query",
        "nilo custom-emoji list",
        "nilo custom-emoji retrieve",
        "nilo raw-api operations",
        "nilo raw-api invoke",
        "nilo server run",
        "nilo server status",
        "nilo server stop",
        "nilo server logs",
        "nilo server remove",
        "nilo server stdio",
    ]

    for command in required_commands:
        assert command in text, command


def test_user_cli_doc_positions_raw_api_as_advanced_fallback() -> None:
    text = read_user_cli_docs()

    assert "Raw API is an advanced fallback entrypoint" in text
    assert "nilo raw-api operations" in text
    assert "nilo raw-api invoke" in text
