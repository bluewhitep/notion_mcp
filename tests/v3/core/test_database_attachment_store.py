import json

import pytest

from nilo.core.attachments import DatabaseAttachment, DatabaseAttachmentStore
from nilo.core.errors import DatabaseAttachmentNotFoundError
from nilo.core.project import ProjectResolver


def test_database_attachment_store_save_load_and_delete(tmp_path) -> None:
    ProjectResolver.init_project(tmp_path)
    attachment = DatabaseAttachment.from_manual(
        database_id="db-1",
        title="Project Database",
        command="nilo database attach --no-verify",
    )

    DatabaseAttachmentStore.save(tmp_path, attachment)
    state_file = tmp_path / ".notion_mcp" / "state" / "database.attach.json"

    assert state_file.exists()
    raw = json.loads(state_file.read_text(encoding="utf-8"))
    assert raw["kind"] == "database_attach"
    assert raw["database"]["id"] == "db-1"
    assert "notion_token" not in state_file.read_text(encoding="utf-8")

    loaded = DatabaseAttachmentStore.load(tmp_path)
    assert loaded.database.id == "db-1"
    assert loaded.active_data_source is None

    DatabaseAttachmentStore.delete(tmp_path)
    with pytest.raises(DatabaseAttachmentNotFoundError):
        DatabaseAttachmentStore.load(tmp_path)


def test_database_attachment_store_rejects_token_fields(tmp_path) -> None:
    ProjectResolver.init_project(tmp_path)
    state_file = tmp_path / ".notion_mcp" / "state" / "database.attach.json"
    state_file.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "kind": "database_attach",
                "status": "attached",
                "database": {"id": "db-1", "title": "Tasks", "notion_token": "secret_xxx"},
                "active_data_source": None,
                "available_data_sources": [],
                "attached_at": "2026-06-08T00:00:00Z",
                "updated_at": "2026-06-08T00:00:00Z",
                "verified_at": None,
                "source": {"created_by": "cli", "command": "test"},
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(Exception, match="credential"):
        DatabaseAttachmentStore.load(tmp_path)
