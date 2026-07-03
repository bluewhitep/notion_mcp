import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from nilo.cli import app
from nilo.cli.commands import pages


runner = CliRunner()


class FakePagesService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def content(self, page_id: str, *, tree: bool = False) -> dict[str, object]:
        self.calls.append(("content", {"page_id": page_id, "tree": tree}))
        return {
            "page": {"id": page_id, "title": "Editable Page", "properties": {}},
            "blocks": [{"id": "block-1", "type": "paragraph", "text": "Intro", "parent_id": page_id}],
        }


class FakeBlocksService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def append_children(
        self,
        block_id: str,
        *,
        children: list[dict[str, object]],
        position: dict[str, object] | None = None,
    ) -> dict[str, object]:
        self.calls.append(("append", {"block_id": block_id, "children": children, "position": position}))
        return {"operation": "append", "block_id": block_id, "children": children, "position": position}

    def retrieve(self, block_id: str) -> dict[str, object]:
        self.calls.append(("retrieve", block_id))
        return {"id": block_id, "parent": {"type": "page_id", "page_id": "page-1"}}

    def update(self, block_id: str, payload: dict[str, object]) -> dict[str, object]:
        self.calls.append(("update", {"block_id": block_id, "payload": payload}))
        return {"operation": "update", "block_id": block_id}

    def trash(self, block_id: str) -> dict[str, object]:
        self.calls.append(("trash", block_id))
        return {"operation": "trash", "block_id": block_id}


def test_page_content_edit_workflow(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    page_service = FakePagesService()
    block_service = FakeBlocksService()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(pages, "get_pages_service", lambda: page_service)
    monkeypatch.setattr(pages, "get_blocks_service", lambda: block_service)

    attach = runner.invoke(app, ["page", "attach", "page-1", "--no-verify", "--title", "Editable Page"])
    content = runner.invoke(app, ["page", "content", "--json"])
    insert_after = runner.invoke(
        app,
        ["page", "block", "insert-after", "block-1", "--payload", '{"children": [{"type": "paragraph"}]}', "--json"],
    )
    append = runner.invoke(
        app,
        ["page", "block", "append", "page-1", "--payload", '{"children": [{"type": "bulleted_list_item"}]}', "--json"],
    )
    update = runner.invoke(app, ["page", "block", "update", "block-1", "--payload", '{"paragraph": {}}', "--json"])
    remove = runner.invoke(app, ["page", "block", "remove", "block-1", "--json"])

    assert attach.exit_code == 0
    assert content.exit_code == 0
    assert json.loads(content.stdout)["blocks"][0]["id"] == "block-1"
    assert insert_after.exit_code == 0
    assert append.exit_code == 0
    assert update.exit_code == 0
    assert remove.exit_code == 0
    assert page_service.calls == [("content", {"page_id": "page-1", "tree": False})]
    assert block_service.calls == [
        ("retrieve", "block-1"),
        (
            "append",
            {
                "block_id": "page-1",
                "children": [{"type": "paragraph"}],
                "position": {"type": "after_block", "after_block": {"id": "block-1"}},
            },
        ),
        ("append", {"block_id": "page-1", "children": [{"type": "bulleted_list_item"}], "position": None}),
        ("update", {"block_id": "block-1", "payload": {"paragraph": {}}}),
        ("trash", "block-1"),
    ]
