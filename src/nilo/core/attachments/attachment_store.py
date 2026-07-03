# File: src/nilo/core/attachments/attachment_store.py
# Format: UTF-8
# =============================
# File Description:
# Project-local attachment state load/save/delete operations.
# TAG: core, attachments, store
# =============================

from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from nilo.core.errors import (
    DatabaseAttachmentNotFoundError,
    PageAttachmentNotFoundError,
    ProjectConfigValidationError,
)
from nilo.core.project import ProjectPaths
from nilo.core.project.project_config import PROJECT_FILE_MODE, atomic_write_json, reject_credential_fields

from .database_attachment import DatabaseAttachment
from .page_attachment import PageAttachment


class PageAttachmentStore:
    # --------------------------------
    # Function Description:
    # Loads attached page state from a project root.
    # Inputs/Outputs:
    # Input project root; returns PageAttachment or raises PageAttachmentNotFoundError.
    # Usage:
    # PageAttachmentStore.load(project_root)
    # --------------------------------
    @staticmethod
    def load(project_root: Path) -> PageAttachment:
        root = Path(project_root).expanduser().resolve()
        state_file = ProjectPaths(root).page_attachment_file
        if not state_file.exists():
            raise PageAttachmentNotFoundError(str(root))
        try:
            raw = json.loads(state_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ProjectConfigValidationError(
                "Page attachment state is not valid JSON",
                details={"path": str(state_file)},
            ) from exc
        if not isinstance(raw, dict):
            raise ProjectConfigValidationError(
                "Page attachment state must contain a JSON object",
                details={"path": str(state_file)},
            )
        reject_credential_fields(raw)
        try:
            return PageAttachment(**raw)
        except ValidationError as exc:
            raise ProjectConfigValidationError(
                "Invalid page attachment state",
                details={"path": str(state_file), "errors": exc.errors()},
            ) from exc

    # --------------------------------
    # Function Description:
    # Saves attached page state under .notion_mcp/state.
    # Inputs/Outputs:
    # Input project root and PageAttachment; writes page.attach.json.
    # Usage:
    # PageAttachmentStore.save(project_root, attachment)
    # --------------------------------
    @staticmethod
    def save(project_root: Path, attachment: PageAttachment) -> None:
        root = Path(project_root).expanduser().resolve()
        payload = attachment.model_dump(mode="json", exclude_none=False)
        reject_credential_fields(payload)
        atomic_write_json(ProjectPaths(root).page_attachment_file, payload, mode=PROJECT_FILE_MODE)

    # --------------------------------
    # Function Description:
    # Deletes attached page state if present.
    # Inputs/Outputs:
    # Input project root; output is None after deleting local state.
    # Usage:
    # PageAttachmentStore.delete(project_root)
    # --------------------------------
    @staticmethod
    def delete(project_root: Path) -> None:
        root = Path(project_root).expanduser().resolve()
        state_file = ProjectPaths(root).page_attachment_file
        if state_file.exists():
            state_file.unlink()


class DatabaseAttachmentStore:
    # --------------------------------
    # Function Description:
    # Loads attached database state from a project root.
    # Inputs/Outputs:
    # Input project root; returns DatabaseAttachment or raises DatabaseAttachmentNotFoundError.
    # Usage:
    # DatabaseAttachmentStore.load(project_root)
    # --------------------------------
    @staticmethod
    def load(project_root: Path) -> DatabaseAttachment:
        root = Path(project_root).expanduser().resolve()
        state_file = ProjectPaths(root).database_attachment_file
        if not state_file.exists():
            raise DatabaseAttachmentNotFoundError(str(root))
        try:
            raw = json.loads(state_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ProjectConfigValidationError(
                "Database attachment state is not valid JSON",
                details={"path": str(state_file)},
            ) from exc
        if not isinstance(raw, dict):
            raise ProjectConfigValidationError(
                "Database attachment state must contain a JSON object",
                details={"path": str(state_file)},
            )
        reject_credential_fields(raw)
        try:
            return DatabaseAttachment(**raw)
        except ValidationError as exc:
            raise ProjectConfigValidationError(
                "Invalid database attachment state",
                details={"path": str(state_file), "errors": exc.errors()},
            ) from exc

    # --------------------------------
    # Function Description:
    # Saves attached database state under .notion_mcp/state.
    # Inputs/Outputs:
    # Input project root and DatabaseAttachment; writes database.attach.json.
    # Usage:
    # DatabaseAttachmentStore.save(project_root, attachment)
    # --------------------------------
    @staticmethod
    def save(project_root: Path, attachment: DatabaseAttachment) -> None:
        root = Path(project_root).expanduser().resolve()
        payload = attachment.model_dump(mode="json", exclude_none=False)
        reject_credential_fields(payload)
        atomic_write_json(ProjectPaths(root).database_attachment_file, payload, mode=PROJECT_FILE_MODE)

    # --------------------------------
    # Function Description:
    # Deletes attached database state if present.
    # Inputs/Outputs:
    # Input project root; output is None after deleting local state.
    # Usage:
    # DatabaseAttachmentStore.delete(project_root)
    # --------------------------------
    @staticmethod
    def delete(project_root: Path) -> None:
        root = Path(project_root).expanduser().resolve()
        state_file = ProjectPaths(root).database_attachment_file
        if state_file.exists():
            state_file.unlink()
