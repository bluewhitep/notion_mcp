import json
from pathlib import Path

import pytest

from nilo.core.errors import ProjectConfigNotFoundError
from nilo.core.project import ProjectConfigStore, ProjectResolver


def test_project_resolver_finds_project_root_from_child_directory(tmp_path: Path) -> None:
    root = tmp_path / "workspace" / "my-project"
    child = root / "src" / "module"
    child.mkdir(parents=True)
    ProjectConfigStore.init_project(root, project_name="Demo")

    assert ProjectResolver.find_project_root(child) == root
    assert ProjectResolver.find_project_config(child) == root / ".notion_mcp" / "config.json"


def test_project_resolver_returns_clear_error_when_config_is_missing(tmp_path: Path) -> None:
    child = tmp_path / "missing" / "child"
    child.mkdir(parents=True)

    with pytest.raises(ProjectConfigNotFoundError) as exc_info:
        ProjectResolver.find_project_root(child)

    assert ".notion_mcp/config.json" in exc_info.value.message
    assert str(child) in exc_info.value.details["start"]


def test_project_config_store_initializes_expected_directory_shape(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    config = ProjectConfigStore.init_project(
        project_root,
        project_name="Demo",
        workspace_hint="Sandbox",
    )

    project_dir = project_root / ".notion_mcp"
    config_file = project_dir / "config.json"
    assert config.schema_version == 1
    assert config.project_name == "Demo"
    assert config.workspace_hint == "Sandbox"
    assert config_file.exists()
    assert (project_dir / "state").is_dir()
    assert (project_dir / "cache").is_dir()
    assert (project_dir / "logs").is_dir()
    assert (project_dir / ".gitignore").read_text(encoding="utf-8") == "state/\ncache/\nlogs/\n"

    raw_config = json.loads(config_file.read_text(encoding="utf-8"))
    assert raw_config["settings"]["prefer_attached_page"] is True
    assert raw_config["settings"]["prefer_attached_database"] is True
    assert raw_config["settings"]["json_output_default"] is False
    assert "notion_token" not in raw_config
    assert "token" not in config_file.read_text(encoding="utf-8").lower()


def test_project_config_store_rejects_token_fields(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    config_file = project_root / ".notion_mcp" / "config.json"
    config_file.parent.mkdir(parents=True)
    config_file.write_text('{"schema_version": 1, "notion_token": "secret"}\n', encoding="utf-8")

    with pytest.raises(ValueError) as exc_info:
        ProjectConfigStore.load(project_root)

    assert "token" in str(exc_info.value)
