from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]


def test_stage7_required_documentation_files_exist() -> None:
    required = [
        "Docs/Developer/architecture/overview.md",
        "Docs/Developer/api/core.md",
        "Docs/Developer/api/cli.md",
        "Docs/Developer/mcp_tools/README.md",
        "Docs/Developer/testing/strategy.md",
        "Docs/Developer/testing/live.md",
        "Docs/Developer/testing/scenarios.md",
        "Docs/Developer/packaging.md",
        "Docs/User/installation.md",
        "Docs/User/configuration.md",
        "Docs/User/cli.md",
        "Docs/User/mcp_clients.md",
        "Docs/User/troubleshooting.md",
    ]

    for relative_path in required:
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_user_docs_do_not_expose_internal_source_paths() -> None:
    user_docs = REPO_ROOT / "Docs" / "User"

    for path in user_docs.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        assert "src/notion_mcp" not in text
        assert "tests/v2" not in text


def test_developer_docs_state_core_cli_mcp_boundary() -> None:
    overview = (REPO_ROOT / "Docs/Developer/architecture/overview.md").read_text(
        encoding="utf-8"
    )

    assert "Core" in overview
    assert "CLI -> Core" in overview
    assert "MCP Tool -> Core" in overview
    assert "MCP Tool -> CLI" not in overview
