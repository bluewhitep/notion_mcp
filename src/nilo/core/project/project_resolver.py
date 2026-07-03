# File: src/nilo/core/project/project_resolver.py
# Format: UTF-8
# =============================
# File Description:
# Git-like cwd-to-project-root resolver for .notion_mcp project context.
# TAG: core, project, resolver
# =============================

from __future__ import annotations

from pathlib import Path

from nilo.core.errors import ProjectConfigNotFoundError

from .project_config import ProjectConfig, ProjectConfigStore
from .project_paths import ProjectPaths


class ProjectResolver:
    # --------------------------------
    # Function Description:
    # Finds the nearest parent directory containing .notion_mcp/config.json.
    # Inputs/Outputs:
    # Input optional start path; returns project root Path or raises ProjectConfigNotFoundError.
    # Usage:
    # ProjectResolver.find_project_root(Path.cwd())
    # --------------------------------
    @staticmethod
    def find_project_root(cwd: Path | None = None) -> Path:
        start = Path.cwd() if cwd is None else Path(cwd)
        current = start.expanduser().resolve()
        if current.is_file():
            current = current.parent
        for candidate in (current, *current.parents):
            if ProjectPaths(candidate).config_file.exists():
                return candidate
        raise ProjectConfigNotFoundError(str(current))

    # --------------------------------
    # Function Description:
    # Finds the nearest project configuration file from a start path.
    # Inputs/Outputs:
    # Input optional start path; returns .notion_mcp/config.json Path.
    # Usage:
    # ProjectResolver.find_project_config(Path.cwd())
    # --------------------------------
    @staticmethod
    def find_project_config(cwd: Path | None = None) -> Path:
        root = ProjectResolver.find_project_root(cwd)
        return ProjectPaths(root).config_file

    # --------------------------------
    # Function Description:
    # Finds an existing project or initializes one at a fallback root.
    # Inputs/Outputs:
    # Input cwd and init metadata; returns project root and config.
    # Usage:
    # ProjectResolver.ensure_project(Path.cwd())
    # --------------------------------
    @staticmethod
    def ensure_project(
        cwd: Path | None = None,
        *,
        project_name: str | None = None,
        workspace_hint: str | None = None,
        force: bool = False,
        private: bool = False,
    ) -> tuple[Path, ProjectConfig]:
        start = Path.cwd() if cwd is None else Path(cwd)
        try:
            root = ProjectResolver.find_project_root(start)
            return root, ProjectConfigStore.load(root)
        except ProjectConfigNotFoundError:
            root = start.expanduser().resolve()
            config = ProjectConfigStore.init_project(
                root,
                project_name=project_name,
                workspace_hint=workspace_hint,
                force=force,
                private=private,
            )
            return root, config

    # --------------------------------
    # Function Description:
    # Initializes project context in the supplied directory.
    # Inputs/Outputs:
    # Input project root and metadata; returns the saved ProjectConfig.
    # Usage:
    # ProjectResolver.init_project(Path.cwd())
    # --------------------------------
    @staticmethod
    def init_project(
        project_root: Path | None = None,
        *,
        project_name: str | None = None,
        workspace_hint: str | None = None,
        force: bool = False,
        private: bool = False,
    ) -> ProjectConfig:
        root = Path.cwd() if project_root is None else Path(project_root)
        return ProjectConfigStore.init_project(
            root,
            project_name=project_name,
            workspace_hint=workspace_hint,
            force=force,
            private=private,
        )
