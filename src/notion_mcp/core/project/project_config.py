# File: src/notion_mcp/core/project/project_config.py
# Format: UTF-8
# =============================
# File Description:
# Project-level .notion_mcp configuration models and storage operations.
# TAG: core, project, config
# =============================

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from notion_mcp.core.errors import (
    ProjectAlreadyInitializedError,
    ProjectConfigNotFoundError,
    ProjectConfigValidationError,
)

from .project_paths import ProjectPaths

DEFAULT_PROJECT_GITIGNORE = "state/\ncache/\nlogs/\n"
PROJECT_FILE_MODE = 0o644
PRIVATE_PROJECT_FILE_MODE = 0o600


class ProjectSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prefer_attached_page: bool = True
    prefer_attached_database: bool = True
    json_output_default: bool = False


class ProjectConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = 1
    project_name: str | None = None
    workspace_hint: str | None = None
    created_at: str
    updated_at: str
    settings: ProjectSettings = Field(default_factory=ProjectSettings)

    # --------------------------------
    # Function Description:
    # Validates the supported project config schema version.
    # Inputs/Outputs:
    # Input integer schema version; returns supported version or raises ValueError.
    # Usage:
    # ProjectConfig(schema_version=1, created_at=now, updated_at=now)
    # --------------------------------
    @field_validator("schema_version")
    @classmethod
    def validate_schema_version(cls, value: int) -> int:
        if value != 1:
            raise ValueError("project config schema_version must be 1")
        return value


# --------------------------------
# Function Description:
# Returns the current UTC timestamp in stable JSON form.
# Inputs/Outputs:
# No input; returns an ISO-8601 UTC string.
# Usage:
# timestamp_utc()
# --------------------------------
def timestamp_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


# --------------------------------
# Function Description:
# Recursively rejects credential-looking project config keys.
# Inputs/Outputs:
# Input JSON-like value; raises ProjectConfigValidationError on token/credential keys.
# Usage:
# reject_credential_fields({"schema_version": 1})
# --------------------------------
def reject_credential_fields(value: Any, *, path: str = "") -> None:
    credential_terms = ("token", "secret", "credential", "private_key", "refresh")
    if isinstance(value, dict):
        for key, nested in value.items():
            key_path = f"{path}.{key}" if path else str(key)
            lowered = str(key).lower()
            if any(term in lowered for term in credential_terms):
                raise ProjectConfigValidationError(
                    "Project config must not contain token or credential fields",
                    details={"field": key_path},
                )
            reject_credential_fields(nested, path=key_path)
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            reject_credential_fields(nested, path=f"{path}[{index}]")


# --------------------------------
# Function Description:
# Writes a JSON object atomically with stable formatting and permissions.
# Inputs/Outputs:
# Input target path, payload, and mode; writes file with trailing newline.
# Usage:
# atomic_write_json(Path("config.json"), {"schema_version": 1})
# --------------------------------
def atomic_write_json(path: Path, payload: dict[str, Any], *, mode: int = PROJECT_FILE_MODE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(f"{path.name}.tmp")
    encoded = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    try:
        fd = os.open(tmp_path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, mode)
        with os.fdopen(fd, "w", encoding="utf-8") as file_obj:
            file_obj.write(encoded)
            file_obj.flush()
            os.fsync(file_obj.fileno())
        os.replace(tmp_path, path)
        os.chmod(path, mode)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


class ProjectConfigStore:
    # --------------------------------
    # Function Description:
    # Creates a default project configuration directory and config file.
    # Inputs/Outputs:
    # Input project root and metadata; returns the saved ProjectConfig.
    # Usage:
    # ProjectConfigStore.init_project(Path.cwd(), project_name="Demo")
    # --------------------------------
    @staticmethod
    def init_project(
        project_root: Path,
        *,
        project_name: str | None = None,
        workspace_hint: str | None = None,
        force: bool = False,
        private: bool = False,
    ) -> ProjectConfig:
        root = Path(project_root).expanduser().resolve()
        paths = ProjectPaths(root)
        if paths.config_file.exists() and not force:
            raise ProjectAlreadyInitializedError(str(paths.config_file))
        root.mkdir(parents=True, exist_ok=True)
        paths.project_dir.mkdir(parents=True, exist_ok=True)
        paths.state_dir.mkdir(parents=True, exist_ok=True)
        paths.cache_dir.mkdir(parents=True, exist_ok=True)
        paths.logs_dir.mkdir(parents=True, exist_ok=True)
        paths.gitignore_file.write_text(DEFAULT_PROJECT_GITIGNORE, encoding="utf-8")
        mode = PRIVATE_PROJECT_FILE_MODE if private else PROJECT_FILE_MODE
        os.chmod(paths.gitignore_file, mode)
        now = timestamp_utc()
        config = ProjectConfig(
            schema_version=1,
            project_name=project_name,
            workspace_hint=workspace_hint,
            created_at=now,
            updated_at=now,
            settings=ProjectSettings(),
        )
        ProjectConfigStore.save(root, config, private=private)
        return config

    # --------------------------------
    # Function Description:
    # Loads and validates a project configuration file.
    # Inputs/Outputs:
    # Input project root; returns ProjectConfig or raises Core project errors.
    # Usage:
    # ProjectConfigStore.load(Path.cwd())
    # --------------------------------
    @staticmethod
    def load(project_root: Path) -> ProjectConfig:
        root = Path(project_root).expanduser().resolve()
        config_file = ProjectPaths(root).config_file
        if not config_file.exists():
            raise ProjectConfigNotFoundError(str(root))
        try:
            raw = json.loads(config_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ProjectConfigValidationError(
                "Project configuration file is not valid JSON",
                details={"path": str(config_file)},
            ) from exc
        if not isinstance(raw, dict):
            raise ProjectConfigValidationError(
                "Project configuration file must contain a JSON object",
                details={"path": str(config_file)},
            )
        reject_credential_fields(raw)
        try:
            return ProjectConfig(**raw)
        except ValidationError as exc:
            raise ProjectConfigValidationError(
                "Invalid project configuration",
                details={"path": str(config_file), "errors": exc.errors()},
            ) from exc

    # --------------------------------
    # Function Description:
    # Saves a validated project configuration file.
    # Inputs/Outputs:
    # Input project root and config; writes .notion_mcp/config.json.
    # Usage:
    # ProjectConfigStore.save(root, config)
    # --------------------------------
    @staticmethod
    def save(project_root: Path, config: ProjectConfig, *, private: bool = False) -> None:
        root = Path(project_root).expanduser().resolve()
        paths = ProjectPaths(root)
        paths.project_dir.mkdir(parents=True, exist_ok=True)
        paths.state_dir.mkdir(parents=True, exist_ok=True)
        paths.cache_dir.mkdir(parents=True, exist_ok=True)
        paths.logs_dir.mkdir(parents=True, exist_ok=True)
        payload = config.model_dump(mode="json", exclude_none=True)
        reject_credential_fields(payload)
        mode = PRIVATE_PROJECT_FILE_MODE if private else PROJECT_FILE_MODE
        atomic_write_json(paths.config_file, payload, mode=mode)
