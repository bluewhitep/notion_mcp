from pathlib import Path

import pytest
from typer.testing import CliRunner

from nilo.cli import app


runner = CliRunner()


def test_page_detach_removes_local_state_only(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    attach = runner.invoke(app, ["page", "attach", "page-1", "--no-verify", "--title", "Manual"])
    assert attach.exit_code == 0
    state_file = tmp_path / ".notion_mcp" / "state" / "page.attach.json"
    assert state_file.exists()

    detach = runner.invoke(app, ["page", "detach"])

    assert detach.exit_code == 0
    assert "Detached page:" in detach.stdout
    assert "Manual" in detach.stdout
    assert "Removed:" in detach.stdout
    assert not state_file.exists()
    assert (tmp_path / ".notion_mcp" / "config.json").exists()


def test_page_deattach_alias_removes_local_state(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    attach = runner.invoke(app, ["page", "attach", "page-1", "--no-verify", "--title", "Manual"])
    assert attach.exit_code == 0

    detach = runner.invoke(app, ["page", "deattach", "--json"])

    assert detach.exit_code == 0
    assert not (tmp_path / ".notion_mcp" / "state" / "page.attach.json").exists()


def test_page_detach_errors_when_no_page_is_attached(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    init_result = runner.invoke(app, ["project", "init"])
    assert init_result.exit_code == 0

    detach = runner.invoke(app, ["page", "detach"])

    assert detach.exit_code == 1
    assert "No page is attached for this project" in detach.stdout
