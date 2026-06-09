import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from notion_mcp.cli import app
from notion_mcp.cli.commands import databases, pages


runner = CliRunner()
COMPACT_PAGE_ID = "3799a1afb97a80489bb0e7384f334958"
CANONICAL_PAGE_ID = "3799a1af-b97a-8048-9bb0-e7384f334958"
PAGE_URL = f"https://www.notion.so/Notion-MCP-{COMPACT_PAGE_ID}?source=copy_link"
MARKDOWN_PAGE_LINK = f"[Notion MCP]({PAGE_URL})"


class FakePagesService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def retrieve(self, page_id: str) -> dict[str, object]:
        self.calls.append(("retrieve", page_id))
        return {"object": "page", "id": page_id, "properties": {}, "url": PAGE_URL}

    def content(self, page_id: str, *, tree: bool = False) -> dict[str, object]:
        self.calls.append(("content", {"page_id": page_id, "tree": tree}))
        return {"page": {"id": page_id, "title": "Project Home", "properties": {}}, "blocks": []}


def test_page_attach_accepts_copied_notion_url(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = FakePagesService()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(pages, "get_pages_service", lambda: service)

    result = runner.invoke(app, ["page", "attach", PAGE_URL, "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["attachment"]["page"]["id"] == CANONICAL_PAGE_ID
    assert service.calls == [("retrieve", CANONICAL_PAGE_ID)]


def test_page_attach_no_verify_stores_id_from_markdown_link(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(
        app,
        ["page", "attach", MARKDOWN_PAGE_LINK, "--no-verify", "--title", "Manual", "--json"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["attachment"]["page"]["id"] == CANONICAL_PAGE_ID


def test_page_retrieve_and_blocks_accept_copied_notion_url(monkeypatch: pytest.MonkeyPatch) -> None:
    service = FakePagesService()
    monkeypatch.setattr(pages, "get_pages_service", lambda: service)

    retrieve = runner.invoke(app, ["page", "retrieve", PAGE_URL, "--json"])
    blocks = runner.invoke(app, ["page", "blocks", PAGE_URL, "--json"])

    assert retrieve.exit_code == 0
    assert blocks.exit_code == 0
    assert json.loads(retrieve.stdout)["id"] == CANONICAL_PAGE_ID
    assert json.loads(blocks.stdout)["page"]["id"] == CANONICAL_PAGE_ID
    assert service.calls == [
        ("retrieve", CANONICAL_PAGE_ID),
        ("content", {"page_id": CANONICAL_PAGE_ID, "tree": False}),
    ]


def test_page_create_parent_update_and_trash_accept_copied_notion_url() -> None:
    create = runner.invoke(
        app,
        ["page", "create", "--parent-page", PAGE_URL, "--payload", '{"properties": {}}', "--dry-run", "--json"],
    )
    update = runner.invoke(app, ["page", "update", PAGE_URL, "--payload", '{"properties": {}}', "--dry-run", "--json"])
    trash = runner.invoke(app, ["page", "trash", PAGE_URL, "--dry-run", "--json"])

    assert create.exit_code == 0
    assert update.exit_code == 0
    assert trash.exit_code == 0
    assert json.loads(create.stdout)["result"]["parent"] == {"type": "page_id", "page_id": CANONICAL_PAGE_ID}
    assert json.loads(update.stdout)["result"]["page_id"] == CANONICAL_PAGE_ID
    assert json.loads(trash.stdout)["result"]["page_id"] == CANONICAL_PAGE_ID


def test_database_create_parent_page_accepts_copied_notion_url() -> None:
    result = runner.invoke(
        app,
        [
            "database",
            "create",
            "--parent-page",
            PAGE_URL,
            "--payload",
            '{"title": []}',
            "--dry-run",
            "--json",
        ],
    )

    assert result.exit_code == 0
    assert json.loads(result.stdout)["result"]["parent"] == {"type": "page_id", "page_id": CANONICAL_PAGE_ID}
