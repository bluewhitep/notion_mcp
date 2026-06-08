# File: src/notion_mcp/core/audit.py
# Format: UTF-8
# =============================
# File Description:
# Local JSONL audit recorder for Core operations.
# TAG: core, audit
# =============================

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SENSITIVE_KEYS = {"auth", "authorization", "notion_token", "token", "bearer"}


@dataclass(frozen=True)
class AuditEntry:
    timestamp: str
    configured_user_id: str | None
    operation: str
    target: str | None
    dry_run: bool
    metadata: dict[str, Any]


class AuditRecorder:
    # --------------------------------
    # Function Description:
    # Initializes a JSONL audit recorder.
    # Inputs/Outputs:
    # Input output path; output is AuditRecorder.
    # Usage:
    # AuditRecorder(Path("audit.jsonl"))
    # --------------------------------
    def __init__(self, path: Path) -> None:
        self.path = path

    # --------------------------------
    # Function Description:
    # Records one Core operation and strips sensitive metadata.
    # Inputs/Outputs:
    # Input operation metadata; returns the stored AuditEntry.
    # Usage:
    # recorder.record(operation="pages.create", target="parent")
    # --------------------------------
    def record(
        self,
        *,
        configured_user_id: str | None,
        operation: str,
        target: str | None,
        dry_run: bool,
        metadata: dict[str, Any] | None = None,
    ) -> AuditEntry:
        entry = AuditEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            configured_user_id=configured_user_id,
            operation=operation,
            target=target,
            dry_run=dry_run,
            metadata=scrub_sensitive_metadata(metadata or {}),
        )
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")
        return entry


# --------------------------------
# Function Description:
# Removes sensitive values from an audit metadata dictionary.
# Inputs/Outputs:
# Input metadata dictionary; returns a sanitized copy.
# Usage:
# scrub_sensitive_metadata({"notion_token": "secret"})
# --------------------------------
def scrub_sensitive_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    clean: dict[str, Any] = {}
    for key, value in metadata.items():
        if key.lower() in SENSITIVE_KEYS:
            continue
        if isinstance(value, dict):
            clean[key] = scrub_sensitive_metadata(value)
        else:
            clean[key] = value
    return clean
