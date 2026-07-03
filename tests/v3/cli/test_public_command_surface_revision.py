import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from nilo.cli import app
from nilo.cli.commands import pages
from nilo.core.config import load_core_config


runner = CliRunner()


class FakePagesService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def retrieve(self, page_id: str) -> dict[str, object]:
        self.calls.append(("retrieve", page_id))
        return {"object": "page", "id": page_id, "properties": {}, "url": "https://notion.so/page"}

    def content(self, page_id: str, *, tree: bool = False) -> dict[str, object]:
        self.calls.append(("content", {"page_id": page_id, "tree": tree}))
        return {
            "page": {"id": page_id, "title": "Project Home", "properties": {}},
            "blocks": [{"id": "block-1", "type": "paragraph", "text": "Intro"}],
        }


def test_root_help_exposes_new_public_entrypoints_only() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "init" in result.stdout
    assert "pwd" in result.stdout
    assert "version" in result.stdout
    assert "config" in result.stdout
    assert "│ project " not in result.stdout
    assert "│ local " not in result.stdout
    assert "│ status " not in result.stdout


def test_config_global_and_local_flag_workflows(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cfg_file = tmp_path / "global.json"
    monkeypatch.setenv("NOTION_MCP_CONFIG", str(cfg_file))
    monkeypatch.chdir(tmp_path)

    token_result = runner.invoke(app, ["config", "--global", "user.token", "secret-token"])
    name_result = runner.invoke(app, ["config", "--global", "user.name", "Ada"])
    show_global = runner.invoke(app, ["config", "--global", "--show", "--json"])
    init_result = runner.invoke(app, ["init", "--project-name", "Demo", "--json"])
    show_local = runner.invoke(app, ["config", "--local", "--show", "--json"])

    assert token_result.exit_code == 0
    assert name_result.exit_code == 0
    assert show_global.exit_code == 0
    assert init_result.exit_code == 0
    assert show_local.exit_code == 0
    assert load_core_config(path=cfg_file).notion_token == "secret-token"
    assert load_core_config(path=cfg_file).user_name == "Ada"
    global_payload = json.loads(show_global.stdout)
    assert global_payload["configured"] is True
    assert global_payload["token_set"] is True
    assert global_payload["user"]["name"] == "Ada"
    local_payload = json.loads(show_local.stdout)
    assert local_payload["config"]["project_name"] == "Demo"


def test_pwd_and_version_commands(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    init_result = runner.invoke(app, ["init", "--json"])
    pwd_result = runner.invoke(app, ["pwd", "--json"])
    version_result = runner.invoke(app, ["version", "--json"])

    assert init_result.exit_code == 0
    assert pwd_result.exit_code == 0
    assert version_result.exit_code == 0
    assert json.loads(pwd_result.stdout)["project_root"] == str(tmp_path)
    version_payload = json.loads(version_result.stdout)
    assert "mcp_version" in version_payload
    assert "notion_version" in version_payload


def test_page_help_uses_retrieve_blocks_and_hides_old_aliases() -> None:
    result = runner.invoke(app, ["page", "--help"])

    assert result.exit_code == 0
    assert "retrieve" in result.stdout
    assert "blocks" in result.stdout
    assert "create" in result.stdout
    assert "content" not in result.stdout
    assert "current" not in result.stdout
    assert "deattach" not in result.stdout


def test_page_retrieve_and_blocks_use_attached_page_by_default(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = FakePagesService()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(pages, "get_pages_service", lambda: service)
    attach = runner.invoke(app, ["page", "attach", "attached-page", "--no-verify", "--title", "Attached"])
    assert attach.exit_code == 0

    retrieve = runner.invoke(app, ["page", "retrieve", "--json"])
    blocks = runner.invoke(app, ["page", "blocks", "--json"])

    assert retrieve.exit_code == 0
    assert blocks.exit_code == 0
    assert json.loads(retrieve.stdout)["id"] == "attached-page"
    assert json.loads(blocks.stdout)["blocks"][0]["id"] == "block-1"
    assert service.calls == [
        ("retrieve", "attached-page"),
        ("content", {"page_id": "attached-page", "tree": False}),
    ]


def test_block_help_exposes_editing_commands() -> None:
    result = runner.invoke(app, ["block", "--help"])

    assert result.exit_code == 0
    assert "append" in result.stdout
    assert "insert-after" in result.stdout
    assert "update" in result.stdout
    assert "trash" in result.stdout


def test_database_and_data_source_help_use_formal_boundaries() -> None:
    database = runner.invoke(app, ["database", "--help"])
    database_query = runner.invoke(app, ["database", "query", "--help"])
    database_page = runner.invoke(app, ["database", "page", "create", "--help"])
    database_property = runner.invoke(app, ["database", "property", "rename", "--help"])
    data_source = runner.invoke(app, ["data-source", "--help"])

    assert database.exit_code == 0
    assert database_query.exit_code == 0
    assert database_page.exit_code == 0
    assert database_property.exit_code == 0
    assert data_source.exit_code == 0
    assert "current" not in database.stdout
    assert "deattach" not in database.stdout
    assert "--data-source" not in database_query.stdout
    assert "DATA_SOURCE_ID" not in database_page.stdout
    assert "DATA_SOURCE_ID" not in database_property.stdout
    assert "page" in data_source.stdout
