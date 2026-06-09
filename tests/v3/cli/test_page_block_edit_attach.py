import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from notion_mcp.cli import app
from notion_mcp.cli.commands import pages


runner = CliRunner()


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
        return {"id": block_id, "parent": {"type": "page_id", "page_id": "attached-page"}}

    def update(self, block_id: str, payload: dict[str, object]) -> dict[str, object]:
        self.calls.append(("update", {"block_id": block_id, "payload": payload}))
        return {"operation": "update", "block_id": block_id, "payload": payload}

    def trash(self, block_id: str) -> dict[str, object]:
        self.calls.append(("trash", block_id))
        return {"operation": "trash", "block_id": block_id}


def attach_page(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, service: FakeBlocksService) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(pages, "get_blocks_service", lambda: service)
    result = runner.invoke(app, ["page", "attach", "attached-page", "--no-verify", "--title", "Attached"])
    assert result.exit_code == 0


def test_page_block_append_calls_block_service_with_payload_children(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = FakeBlocksService()
    attach_page(tmp_path, monkeypatch, service)

    result = runner.invoke(
        app,
        ["page", "block", "append", "block-1", "--payload", '{"children": [{"type": "paragraph"}]}', "--json"],
    )

    assert result.exit_code == 0
    assert json.loads(result.stdout)["operation"] == "append"
    assert service.calls == [
        ("append", {"block_id": "block-1", "children": [{"type": "paragraph"}], "position": None})
    ]


def test_page_block_insert_after_resolves_parent_and_uses_position(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = FakeBlocksService()
    attach_page(tmp_path, monkeypatch, service)

    result = runner.invoke(
        app,
        [
            "page",
            "block",
            "insert-after",
            "target-block",
            "--payload",
            '{"children": [{"type": "paragraph"}]}',
            "--json",
        ],
    )

    assert result.exit_code == 0
    assert json.loads(result.stdout)["position"] == {
        "type": "after_block",
        "after_block": {"id": "target-block"},
    }
    assert service.calls == [
        ("retrieve", "target-block"),
        (
            "append",
            {
                "block_id": "attached-page",
                "children": [{"type": "paragraph"}],
                "position": {"type": "after_block", "after_block": {"id": "target-block"}},
            },
        ),
    ]


def test_page_block_update_and_remove_call_block_service(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service = FakeBlocksService()
    attach_page(tmp_path, monkeypatch, service)

    update = runner.invoke(app, ["page", "block", "update", "block-1", "--payload", '{"paragraph": {}}', "--json"])
    remove = runner.invoke(app, ["page", "block", "remove", "block-1", "--json"])

    assert update.exit_code == 0
    assert remove.exit_code == 0
    assert service.calls == [
        ("update", {"block_id": "block-1", "payload": {"paragraph": {}}}),
        ("trash", "block-1"),
    ]
