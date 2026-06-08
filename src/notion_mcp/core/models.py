# File: src/notion_mcp/core/models.py
# Format: UTF-8
# =============================
# File Description:
# Shared lightweight Core models for operation results and dry-run responses.
# TAG: core, models
# =============================

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class OperationResult:
    operation: str
    result: dict[str, Any]
    dry_run: bool = False


# --------------------------------
# Function Description:
# Builds a standard dry-run operation result.
# Inputs/Outputs:
# Input operation and payload; returns OperationResult with dry_run enabled.
# Usage:
# dry_run_result("pages.create", {"parent": {}})
# --------------------------------
def dry_run_result(operation: str, payload: dict[str, Any]) -> OperationResult:
    return OperationResult(operation=operation, result=payload, dry_run=True)
