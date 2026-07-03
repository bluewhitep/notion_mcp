# File: src/nilo/core/identifiers.py
# Format: UTF-8
# =============================
# File Description:
# Shared Notion identifier parsing helpers for CLI and future entrypoints.
# TAG: core, identifiers, notion
# =============================

from __future__ import annotations

import re

_HYPHENATED_UUID_RE = re.compile(
    r"(?i)(?<![0-9a-f])"
    r"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"
    r"(?![0-9a-f])"
)
_COMPACT_UUID_RE = re.compile(r"(?i)(?<![0-9a-f])([0-9a-f]{32})(?![0-9a-f])")


# --------------------------------
# Function Description:
# Formats a 32-character hex Notion id as a hyphenated UUID string.
# Inputs/Outputs:
# Input compact 32-character hex id; returns lower-case hyphenated id.
# Usage:
# canonicalize_compact_notion_id("3799a1afb97a80489bb0e7384f334958")
# --------------------------------
def canonicalize_compact_notion_id(compact_id: str) -> str:
    normalized = compact_id.replace("-", "").lower()
    return (
        f"{normalized[0:8]}-"
        f"{normalized[8:12]}-"
        f"{normalized[12:16]}-"
        f"{normalized[16:20]}-"
        f"{normalized[20:32]}"
    )


# --------------------------------
# Function Description:
# Extracts the first Notion-style UUID candidate from free-form input.
# Inputs/Outputs:
# Input id, URL, or Markdown link; returns canonical id or None.
# Usage:
# extract_notion_uuid_from_input("https://www.notion.so/Page-<id>")
# --------------------------------
def extract_notion_uuid_from_input(value: str) -> str | None:
    match = _HYPHENATED_UUID_RE.search(value)
    if match:
        return canonicalize_compact_notion_id(match.group(1))
    match = _COMPACT_UUID_RE.search(value)
    if match:
        return canonicalize_compact_notion_id(match.group(1))
    return None


# --------------------------------
# Function Description:
# Parses a page id argument that may be a raw id, copied Notion URL, or Markdown link.
# Inputs/Outputs:
# Input user-supplied page id value; returns parsed page id.
# Usage:
# parse_notion_page_id("https://www.notion.so/Page-3799...")
# --------------------------------
def parse_notion_page_id(value: str) -> str:
    stripped = value.strip()
    extracted = extract_notion_uuid_from_input(stripped)
    return extracted or stripped
