from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]


def read_doc(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


def test_developer_and_user_doc_entrypoints_are_split() -> None:
    """Developer docs and user docs must expose separate MCP-oriented entrypoints."""
    assert (REPO_ROOT / "Docs" / "Developer").is_dir()
    assert (REPO_ROOT / "Docs" / "User").is_dir()
    assert (REPO_ROOT / "Docs" / "Developer" / "mcp_tools").is_dir()
    assert (REPO_ROOT / "Docs" / "User" / "MCP_Clients.md").is_file()


def test_requirements_distinguish_legacy_prototype_from_target() -> None:
    """Requirements must not present the legacy REST prototype as the final MCP server."""
    requirements = read_doc("Docs/Requirements.md")

    assert "已实现原型能力" in requirements
    assert "待实现目标能力" in requirements
    assert "FastAPI REST 原型" in requirements
    assert "Core + CLI + MCP Tool" in requirements
    assert "MCP Tool" in requirements


def test_design_documents_core_cli_mcp_call_boundaries() -> None:
    """Design docs must state that CLI and MCP both call Core."""
    design = read_doc("Docs/Design.md")

    assert "Core" in design
    assert "CLI" in design
    assert "MCP Tool" in design
    assert "CLI -> Core" in design
    assert "MCP Tool -> Core" in design
    assert "MCP Tool -> CLI" not in design


def test_tech_stack_includes_uv_and_mcp_sdk() -> None:
    """Tech stack must include uv and the MCP Python SDK as planned dependencies."""
    tech_stack = read_doc("Docs/TechStack.md")

    assert "uv" in tech_stack
    assert "mcp" in tech_stack
    assert "MCP Python SDK" in tech_stack
    assert "Notion API version" in tech_stack


def test_development_plan_marks_current_plan_as_legacy_prototype() -> None:
    """The old completion checklist must be labeled as legacy prototype scope."""
    plan = read_doc("Docs/Development_Plan.md")

    assert "legacy prototype" in plan
    assert "开发文档目录" in plan
