from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]


def test_stage7_required_documentation_files_exist() -> None:
    required = [
        "Docs/EN/Developer/architecture/overview.md",
        "Docs/EN/Developer/api/core.md",
        "Docs/EN/Developer/api/cli.md",
        "Docs/EN/Developer/mcp_tools/README.md",
        "Docs/EN/Developer/testing/strategy.md",
        "Docs/EN/Developer/testing/live.md",
        "Docs/EN/Developer/testing/scenarios.md",
        "Docs/EN/Developer/packaging.md",
        "Docs/EN/User/Installation.md",
        "Docs/EN/User/Configuration.md",
        "Docs/EN/User/Cli.md",
        "Docs/EN/User/Cli/Overview.md",
        "Docs/EN/User/Cli/Project_Config.md",
        "Docs/EN/User/Cli/Page.md",
        "Docs/EN/User/Cli/Block.md",
        "Docs/EN/User/Cli/Database_DataSource.md",
        "Docs/EN/User/Cli/Auth_And_User.md",
        "Docs/EN/User/Cli/Comments.md",
        "Docs/EN/User/Cli/Views.md",
        "Docs/EN/User/Cli/File_Uploads.md",
        "Docs/EN/User/Cli/Search_And_Custom_Emoji.md",
        "Docs/EN/User/Cli/Raw_API.md",
        "Docs/EN/User/Cli/MCP_Server.md",
        "Docs/EN/User/MCP_Clients.md",
        "Docs/EN/User/Troubleshooting.md",
    ]

    for relative_path in required:
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_user_docs_do_not_expose_internal_source_paths() -> None:
    for user_docs in sorted((REPO_ROOT / "Docs").glob("*/User")):
        for path in user_docs.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            assert "src/nilo" not in text
            assert "tests/v2" not in text


def test_user_doc_file_names_start_with_uppercase_letter() -> None:
    for user_docs in sorted((REPO_ROOT / "Docs").glob("*/User")):
        for path in user_docs.rglob("*.md"):
            assert path.name[0].isupper(), path.relative_to(REPO_ROOT)


def test_developer_docs_state_core_cli_mcp_boundary() -> None:
    overview = (REPO_ROOT / "Docs/EN/Developer/architecture/overview.md").read_text(
        encoding="utf-8"
    )

    assert "Core" in overview
    assert "CLI -> Core" in overview
    assert "MCP Tool -> Core" in overview
    assert "MCP Tool -> CLI" not in overview
