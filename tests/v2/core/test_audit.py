import json
import uuid
from pathlib import Path

from notion_mcp.core.audit import AuditRecorder


def test_audit_recorder_writes_jsonl_without_token(tmp_path: Path) -> None:
    audit_file = tmp_path / "audit" / "operations.jsonl"
    recorder = AuditRecorder(audit_file)

    entry = recorder.record(
        configured_user_id=str(uuid.uuid4()),
        operation="pages.create",
        target="page-parent",
        dry_run=True,
        metadata={"notion_token": "secret-token", "title": "Example"},
    )

    assert audit_file.exists()
    stored = json.loads(audit_file.read_text(encoding="utf-8"))
    assert stored["operation"] == "pages.create"
    assert stored["target"] == "page-parent"
    assert stored["dry_run"] is True
    assert stored["configured_user_id"] == entry.configured_user_id
    assert stored["metadata"] == {"title": "Example"}
    assert "secret-token" not in audit_file.read_text(encoding="utf-8")
