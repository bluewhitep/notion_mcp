# File: src/nilo/core/project/project_paths.py
# Format: UTF-8
# =============================
# File Description:
# Path helpers for project-local .notion_mcp configuration and runtime state.
# TAG: core, project, paths
# =============================

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

PROJECT_DIR_NAME = ".notion_mcp"
PROJECT_CONFIG_NAME = "config.json"
PROJECT_STATE_DIR_NAME = "state"
PROJECT_CACHE_DIR_NAME = "cache"
PROJECT_LOGS_DIR_NAME = "logs"
PROJECT_GITIGNORE_NAME = ".gitignore"
PAGE_ATTACHMENT_NAME = "page.attach.json"
DATABASE_ATTACHMENT_NAME = "database.attach.json"


@dataclass(frozen=True)
class ProjectPaths:
    project_root: Path

    @property
    # --------------------------------
    # Function Description:
    # Returns the project-local .notion_mcp directory.
    # Inputs/Outputs:
    # No input; returns a Path derived from project_root.
    # Usage:
    # ProjectPaths(root).project_dir
    # --------------------------------
    def project_dir(self) -> Path:
        return self.project_root / PROJECT_DIR_NAME

    @property
    # --------------------------------
    # Function Description:
    # Returns the project-level config file path.
    # Inputs/Outputs:
    # No input; returns .notion_mcp/config.json path.
    # Usage:
    # ProjectPaths(root).config_file
    # --------------------------------
    def config_file(self) -> Path:
        return self.project_dir / PROJECT_CONFIG_NAME

    @property
    # --------------------------------
    # Function Description:
    # Returns the project-level attachment state directory.
    # Inputs/Outputs:
    # No input; returns .notion_mcp/state path.
    # Usage:
    # ProjectPaths(root).state_dir
    # --------------------------------
    def state_dir(self) -> Path:
        return self.project_dir / PROJECT_STATE_DIR_NAME

    @property
    # --------------------------------
    # Function Description:
    # Returns the reserved project cache directory.
    # Inputs/Outputs:
    # No input; returns .notion_mcp/cache path.
    # Usage:
    # ProjectPaths(root).cache_dir
    # --------------------------------
    def cache_dir(self) -> Path:
        return self.project_dir / PROJECT_CACHE_DIR_NAME

    @property
    # --------------------------------
    # Function Description:
    # Returns the reserved project logs directory.
    # Inputs/Outputs:
    # No input; returns .notion_mcp/logs path.
    # Usage:
    # ProjectPaths(root).logs_dir
    # --------------------------------
    def logs_dir(self) -> Path:
        return self.project_dir / PROJECT_LOGS_DIR_NAME

    @property
    # --------------------------------
    # Function Description:
    # Returns the project-local ignore file path.
    # Inputs/Outputs:
    # No input; returns .notion_mcp/.gitignore path.
    # Usage:
    # ProjectPaths(root).gitignore_file
    # --------------------------------
    def gitignore_file(self) -> Path:
        return self.project_dir / PROJECT_GITIGNORE_NAME

    @property
    # --------------------------------
    # Function Description:
    # Returns the page attachment state file path.
    # Inputs/Outputs:
    # No input; returns .notion_mcp/state/page.attach.json path.
    # Usage:
    # ProjectPaths(root).page_attachment_file
    # --------------------------------
    def page_attachment_file(self) -> Path:
        return self.state_dir / PAGE_ATTACHMENT_NAME

    @property
    # --------------------------------
    # Function Description:
    # Returns the database attachment state file path.
    # Inputs/Outputs:
    # No input; returns .notion_mcp/state/database.attach.json path.
    # Usage:
    # ProjectPaths(root).database_attachment_file
    # --------------------------------
    def database_attachment_file(self) -> Path:
        return self.state_dir / DATABASE_ATTACHMENT_NAME


# --------------------------------
# Function Description:
# Normalizes a filesystem path to an absolute Path without requiring it to exist.
# Inputs/Outputs:
# Input path-like value; returns absolute Path.
# Usage:
# normalize_path(Path("."))
# --------------------------------
def normalize_path(path: Path) -> Path:
    return Path(path).expanduser().resolve()
