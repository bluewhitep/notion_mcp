"""Small Python 3.10 compatibility shim for the release-readiness tests.

This module intentionally implements only the TOML subset used by this
repository's pyproject file.
"""

from __future__ import annotations

from typing import Any


def loads(text: str) -> dict[str, Any]:
    root: dict[str, Any] = {}
    current = root
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = _strip_comment(lines[index]).strip()
        index += 1
        if not line:
            continue
        if line.startswith("[") and line.endswith("]"):
            current = root
            for part in line.strip("[]").split("."):
                current = current.setdefault(part, {})
            continue
        if "=" not in line:
            continue
        key, raw_value = [part.strip() for part in line.split("=", 1)]
        if raw_value == "[":
            values: list[Any] = []
            while index < len(lines):
                item_line = _strip_comment(lines[index]).strip()
                index += 1
                if item_line == "]":
                    break
                if not item_line:
                    continue
                values.append(_parse_scalar(item_line.rstrip(",")))
            current[key] = values
        else:
            current[key] = _parse_scalar(raw_value.rstrip(","))
    return root


def _strip_comment(line: str) -> str:
    in_string = False
    for index, char in enumerate(line):
        if char == '"':
            in_string = not in_string
        if char == "#" and not in_string:
            return line[:index]
    return line


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("{") and value.endswith("}"):
        result: dict[str, Any] = {}
        body = value[1:-1].strip()
        if not body:
            return result
        for chunk in body.split(","):
            key, raw = [part.strip() for part in chunk.split("=", 1)]
            result[key] = _parse_scalar(raw)
        return result
    if value in {"true", "false"}:
        return value == "true"
    try:
        return int(value)
    except ValueError:
        return value
