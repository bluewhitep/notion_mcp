# File: tests/live/test_live_mcp_server_http_e2e.py
# Format: UTF-8
# =============================
# File Description:
# Live MCP HTTP server E2E tests for real Notion page, block, search, and data source entry workflows.
# TAG: tests, live, e2e, mcp, server, notion
# =============================

from __future__ import annotations

import json
import os
import socket
import subprocess
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, BinaryIO, Callable
from uuid import uuid4

import pytest

from notion_mcp.core.config import CoreConfig, load_core_config, save_core_config
from notion_mcp.core.errors import CoreError
from notion_mcp.core.identifiers import extract_notion_uuid_from_input
from notion_mcp.core.services.pages import extract_block_text
from notion_mcp.mcp_server.process_manager import (
    DEFAULT_TRANSPORT,
    RUNTIME_DIR_ENV,
    STREAMABLE_HTTP_PATH,
    build_server_command,
)
from tests.live.test_live_content_consistency_e2e import (
    _data_source_title_property_name,
    _page_title_text,
    _paragraph,
    _query_contains_page,
    _resolve_data_source_id,
    _resolve_parent_page_id,
    _rich_text,
)


pytestmark = pytest.mark.live


@dataclass
class McpServerProcessHandle:
    process: subprocess.Popen
    url: str
    log_file: Path
    log_handle: BinaryIO

    # --------------------------------
    # Function Description:
    # Stops the test server process using the retained subprocess handle.
    # Inputs/Outputs:
    # No input; output is None after process and log handle cleanup.
    # Usage:
    # server.stop()
    # --------------------------------
    def stop(self) -> None:
        try:
            if self.process.poll() is None:
                self.process.terminate()
                try:
                    self.process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                    self.process.wait(timeout=5)
        finally:
            self.log_handle.close()


class McpHttpClient:
    # --------------------------------
    # Function Description:
    # Initializes a minimal JSON-RPC client for the streamable HTTP MCP endpoint.
    # Inputs/Outputs:
    # Input server URL; output is a reusable client instance.
    # Usage:
    # client = McpHttpClient("http://127.0.0.1:8000/mcp")
    # --------------------------------
    def __init__(self, url: str) -> None:
        self.url = url
        self.session_id: str | None = None
        self.request_id = 0

    # --------------------------------
    # Function Description:
    # Performs the MCP initialize handshake with retry while the server starts.
    # Inputs/Outputs:
    # Input timeout seconds; output is None after session setup.
    # Usage:
    # client.initialize()
    # --------------------------------
    def initialize(self, *, timeout_seconds: float = 20.0) -> None:
        deadline = time.monotonic() + timeout_seconds
        last_error: Exception | None = None
        while time.monotonic() < deadline:
            try:
                self.request(
                    "initialize",
                    {
                        "protocolVersion": "2025-06-18",
                        "capabilities": {},
                        "clientInfo": {"name": "notion-mcp-live-server-e2e", "version": "1.0"},
                    },
                )
                self.notify("notifications/initialized")
                return
            except (AssertionError, urllib.error.URLError) as exc:
                last_error = exc
                time.sleep(0.25)
        raise AssertionError(f"MCP server did not initialize within {timeout_seconds:g}s") from last_error

    # --------------------------------
    # Function Description:
    # Sends a JSON-RPC request and returns the decoded response object.
    # Inputs/Outputs:
    # Input method and optional params; returns JSON-RPC response dictionary.
    # Usage:
    # client.request("tools/list")
    # --------------------------------
    def request(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        self.request_id += 1
        payload: dict[str, Any] = {"jsonrpc": "2.0", "id": self.request_id, "method": method}
        if params is not None:
            payload["params"] = params
        message = self._post(payload)
        error = message.get("error")
        if isinstance(error, dict):
            raise AssertionError(f"MCP JSON-RPC error for {method}: {error}")
        return message

    # --------------------------------
    # Function Description:
    # Sends a JSON-RPC notification without requiring a response payload.
    # Inputs/Outputs:
    # Input method and optional params; returns None.
    # Usage:
    # client.notify("notifications/initialized")
    # --------------------------------
    def notify(self, method: str, params: dict[str, Any] | None = None) -> None:
        payload: dict[str, Any] = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            payload["params"] = params
        self._post(payload)

    # --------------------------------
    # Function Description:
    # Lists MCP tools exposed by the server.
    # Inputs/Outputs:
    # No input; returns tool dictionaries from tools/list.
    # Usage:
    # tools = client.tools_list()
    # --------------------------------
    def tools_list(self) -> list[dict[str, Any]]:
        message = self.request("tools/list")
        result = message.get("result")
        if not isinstance(result, dict):
            raise AssertionError("tools/list did not return a result object")
        tools = result.get("tools")
        if not isinstance(tools, list):
            raise AssertionError("tools/list result has no tools list")
        return [tool for tool in tools if isinstance(tool, dict)]

    # --------------------------------
    # Function Description:
    # Calls an MCP tool and parses its JSON text payload.
    # Inputs/Outputs:
    # Input tool name and args; returns parsed tool payload.
    # Usage:
    # client.tool_json("page_retrieve", {"page_id": "..."})
    # --------------------------------
    def tool_json(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        message = self.request("tools/call", {"name": name, "arguments": arguments})
        result = message.get("result")
        if not isinstance(result, dict):
            raise AssertionError(f"{name} did not return a result object")
        if result.get("isError") is True:
            raise AssertionError(f"{name} returned an MCP tool error: {result}")
        content = result.get("content")
        if not isinstance(content, list) or not content:
            raise AssertionError(f"{name} returned no content")
        first_item = content[0]
        if not isinstance(first_item, dict) or not isinstance(first_item.get("text"), str):
            raise AssertionError(f"{name} returned non-text content: {content}")
        payload = json.loads(first_item["text"])
        if not isinstance(payload, dict):
            raise AssertionError(f"{name} payload is not a JSON object")
        if payload.get("ok") is False:
            raise AssertionError(f"{name} returned Core error: {payload}")
        return payload

    # --------------------------------
    # Function Description:
    # Sends one HTTP POST request to the streamable HTTP MCP endpoint.
    # Inputs/Outputs:
    # Input JSON-RPC payload; returns decoded JSON-RPC response or empty object.
    # Usage:
    # self._post({"jsonrpc": "2.0", "method": "..."})
    # --------------------------------
    def _post(self, payload: dict[str, Any]) -> dict[str, Any]:
        encoded = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        if self.session_id:
            headers["Mcp-Session-Id"] = self.session_id
        request = urllib.request.Request(self.url, data=encoded, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                session_id = response.headers.get("Mcp-Session-Id")
                if session_id:
                    self.session_id = session_id
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            raise AssertionError(f"MCP HTTP {exc.code}: {error_body}") from exc
        if not body.strip():
            return {}
        return _decode_rpc_body(body)


# --------------------------------
# Function Description:
# Skips unless destructive live MCP server E2E checks were explicitly requested.
# Inputs/Outputs:
# No input; skips test process unless NOTION_MCP_LIVE_SERVER_E2E=1.
# Usage:
# _require_live_server_e2e()
# --------------------------------
def _require_live_server_e2e() -> None:
    if os.getenv("NOTION_MCP_LIVE_SERVER_E2E") != "1":
        pytest.skip("Set NOTION_MCP_LIVE_SERVER_E2E=1 to run live MCP server create/update/trash tests")


# --------------------------------
# Function Description:
# Ensures the child MCP server process can load a global config file.
# Inputs/Outputs:
# Input temp path and monkeypatch; returns None or skips if no token is available.
# Usage:
# _prepare_server_config(tmp_path, monkeypatch)
# --------------------------------
def _prepare_server_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    try:
        config = load_core_config()
        if config.notion_token:
            return
    except CoreError:
        pass
    token = os.getenv("NOTION_MCP_TOKEN")
    if not token:
        pytest.skip("No global Notion MCP config or NOTION_MCP_TOKEN available for live MCP server E2E")
    config_path = tmp_path / "global-config.json"
    save_core_config(
        CoreConfig(
            notion_token=token,
            user_id=os.getenv("NOTION_MCP_USER_ID") or None,
        ),
        path=config_path,
    )
    monkeypatch.setenv("NOTION_MCP_CONFIG", str(config_path))


# --------------------------------
# Function Description:
# Decodes a JSON or SSE-wrapped JSON-RPC response body.
# Inputs/Outputs:
# Input response body text; returns JSON-RPC dictionary.
# Usage:
# _decode_rpc_body("data: {...}")
# --------------------------------
def _decode_rpc_body(body: str) -> dict[str, Any]:
    stripped = body.strip()
    data_messages: list[str] = []
    for line in stripped.splitlines():
        if line.startswith("data:"):
            data = line.removeprefix("data:").strip()
            if data and data != "[DONE]":
                data_messages.append(data)
    raw_message = data_messages[-1] if data_messages else stripped
    message = json.loads(raw_message)
    if not isinstance(message, dict):
        raise AssertionError("MCP response body is not a JSON object")
    return message


# --------------------------------
# Function Description:
# Returns an available local TCP port for a temporary server.
# Inputs/Outputs:
# No input; returns an integer port.
# Usage:
# port = _unused_local_port()
# --------------------------------
def _unused_local_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


# --------------------------------
# Function Description:
# Starts the MCP server runner for live HTTP testing and retains the process handle.
# Inputs/Outputs:
# Input host, port, and runtime directory; returns a managed test server process.
# Usage:
# server = _start_test_server("127.0.0.1", port, tmp_path)
# --------------------------------
def _start_test_server(host: str, port: int, runtime_dir: Path) -> McpServerProcessHandle:
    runtime_dir.mkdir(parents=True, exist_ok=True)
    log_file = runtime_dir / "server.log"
    log_handle = log_file.open("ab")
    command = build_server_command(host, port, DEFAULT_TRANSPORT)
    env = os.environ.copy()
    env.setdefault("PYTHONUNBUFFERED", "1")
    env[RUNTIME_DIR_ENV] = str(runtime_dir)
    process = subprocess.Popen(
        command,
        stdin=subprocess.DEVNULL,
        stdout=log_handle,
        stderr=subprocess.STDOUT,
        cwd=Path.cwd(),
        env=env,
    )
    time.sleep(0.2)
    if process.poll() is not None:
        log_handle.close()
        log_text = log_file.read_text(encoding="utf-8", errors="replace") if log_file.exists() else ""
        raise AssertionError(f"MCP server exited early with code {process.returncode}:\n{log_text}")
    return McpServerProcessHandle(
        process=process,
        url=f"http://{host}:{port}{STREAMABLE_HTTP_PATH}",
        log_file=log_file,
        log_handle=log_handle,
    )


# --------------------------------
# Function Description:
# Normalizes a Notion id-like input that may contain a URL.
# Inputs/Outputs:
# Input raw id or URL; returns extracted UUID when present.
# Usage:
# _normalize_notion_id("https://www.notion.so/Page-...")
# --------------------------------
def _normalize_notion_id(value: str) -> str:
    return extract_notion_uuid_from_input(value) or value


# --------------------------------
# Function Description:
# Finds a block id by exact rich text in a children list response.
# Inputs/Outputs:
# Input children response and text; returns block id or fails.
# Usage:
# block_id = _block_id_with_text(children, "body")
# --------------------------------
def _block_id_with_text(children: dict[str, Any], text: str) -> str:
    results = children.get("results", [])
    if isinstance(results, list):
        for block in results:
            if not isinstance(block, dict):
                continue
            block_type = block.get("type")
            block_type_text = block_type if isinstance(block_type, str) else "unsupported"
            if extract_block_text(block, block_type_text) == text and isinstance(block.get("id"), str):
                return block["id"]
    pytest.fail(f"Could not find block with text: {text}")


# --------------------------------
# Function Description:
# Checks if a block children response includes a specific block id.
# Inputs/Outputs:
# Input children response and block id; returns boolean.
# Usage:
# _children_contain_block(children, block_id)
# --------------------------------
def _children_contain_block(children: dict[str, Any], block_id: str) -> bool:
    results = children.get("results", [])
    return isinstance(results, list) and any(isinstance(item, dict) and item.get("id") == block_id for item in results)


# --------------------------------
# Function Description:
# Checks whether a search response includes a page id.
# Inputs/Outputs:
# Input search response and page id; returns boolean.
# Usage:
# _search_contains_page(search_response, page_id)
# --------------------------------
def _search_contains_page(search_response: dict[str, Any], page_id: str) -> bool:
    results = search_response.get("results", [])
    return isinstance(results, list) and any(isinstance(item, dict) and item.get("id") == page_id for item in results)


# --------------------------------
# Function Description:
# Retries a live condition until it becomes true or times out.
# Inputs/Outputs:
# Input predicate and timeout settings; output is None or raises AssertionError.
# Usage:
# _eventually(lambda: client.tool_json(...))
# --------------------------------
def _eventually(predicate: Callable[[], bool], *, timeout_seconds: float = 60.0, interval_seconds: float = 2.0) -> None:
    deadline = time.monotonic() + timeout_seconds
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            if predicate():
                return
        except Exception as exc:  # noqa: BLE001 - test retries transient Notion indexing and transport timing.
            last_error = exc
        time.sleep(interval_seconds)
    try:
        assert predicate()
    except Exception as exc:  # noqa: BLE001 - preserve the last live failure in the assertion chain.
        if last_error is not None:
            raise AssertionError("Condition did not become true before timeout") from last_error
        raise AssertionError("Condition did not become true before timeout") from exc


# --------------------------------
# Function Description:
# Calls a destructive cleanup tool and ignores failures after the main assertion path.
# Inputs/Outputs:
# Input client, tool name, and args; output is None.
# Usage:
# _safe_tool_cleanup(client, "page_trash", {"page_id": page_id, "confirm": True})
# --------------------------------
def _safe_tool_cleanup(client: McpHttpClient | None, tool_name: str, arguments: dict[str, Any]) -> None:
    if client is None or client.session_id is None:
        return
    try:
        client.tool_json(tool_name, arguments)
    except (AssertionError, json.JSONDecodeError, urllib.error.URLError):
        return


# --------------------------------
# Function Description:
# Verifies real Notion mutations through the MCP HTTP server, independent of CLI command handlers.
# Inputs/Outputs:
# Input pytest temp path and monkeypatch; performs live create/read/search/update/trash operations.
# Usage:
# NOTION_MCP_LIVE_SERVER_E2E=1 uv run pytest -q tests/live/test_live_mcp_server_http_e2e.py
# --------------------------------
def test_live_mcp_http_server_create_read_search_update_trash_consistency(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _require_live_server_e2e()
    _prepare_server_config(tmp_path, monkeypatch)
    parent_page_id = _normalize_notion_id(_resolve_parent_page_id())
    data_source_id = _normalize_notion_id(_resolve_data_source_id())
    runtime_dir = tmp_path / "runtime"
    port = _unused_local_port()
    server: McpServerProcessHandle | None = None
    client: McpHttpClient | None = None
    created_page_id: str | None = None
    created_block_id: str | None = None
    created_entry_id: str | None = None

    try:
        server = _start_test_server("127.0.0.1", port, runtime_dir)
        client = McpHttpClient(server.url)
        client.initialize()

        tool_names = {tool.get("name") for tool in client.tools_list()}
        assert {
            "page_create",
            "page_retrieve",
            "page_update",
            "page_trash",
            "block_append",
            "block_children_list",
            "block_update",
            "block_trash",
            "data_source_retrieve",
            "data_source_query",
            "search",
        }.issubset(tool_names)

        suffix = uuid4().hex[:8]
        original_page_title = f"Live MCP server page {suffix}"
        updated_page_title = f"Live MCP server page updated {suffix}"
        initial_page_body = f"Live MCP server initial body {suffix}"
        original_block_text = f"Live MCP server appended block {suffix}"
        updated_block_text = f"Live MCP server appended block updated {suffix}"
        original_entry_title = f"Live MCP server entry {suffix}"
        updated_entry_title = f"Live MCP server entry updated {suffix}"

        created_page = client.tool_json(
            "page_create",
            {
                "payload": {
                    "parent": {"type": "page_id", "page_id": parent_page_id},
                    "properties": {"title": {"title": _rich_text(original_page_title)}},
                    "children": [_paragraph(initial_page_body)],
                }
            },
        )
        created_page_id = str(created_page["id"])

        retrieved_page = client.tool_json("page_retrieve", {"page_id": created_page_id})
        page_title_property = _data_source_title_property_name({"properties": retrieved_page.get("properties", {})})
        assert _page_title_text(retrieved_page, page_title_property) == original_page_title
        page_children = client.tool_json("block_children_list", {"block_id": created_page_id, "page_size": 100})
        assert _block_id_with_text(page_children, initial_page_body)

        _eventually(
            lambda: _search_contains_page(
                client.tool_json(
                    "search",
                    {
                        "payload": {
                            "query": original_page_title,
                            "filter": {"value": "page", "property": "object"},
                            "page_size": 10,
                        }
                    },
                ),
                created_page_id or "",
            ),
            timeout_seconds=90.0,
            interval_seconds=3.0,
        )

        client.tool_json(
            "block_append",
            {
                "block_id": created_page_id,
                "children": [_paragraph(original_block_text)],
            },
        )
        appended_children = client.tool_json("block_children_list", {"block_id": created_page_id, "page_size": 100})
        created_block_id = _block_id_with_text(appended_children, original_block_text)
        client.tool_json(
            "block_update",
            {
                "block_id": created_block_id,
                "payload": {"paragraph": {"rich_text": _rich_text(updated_block_text)}},
            },
        )
        updated_children = client.tool_json("block_children_list", {"block_id": created_page_id, "page_size": 100})
        assert _block_id_with_text(updated_children, updated_block_text) == created_block_id

        client.tool_json(
            "page_update",
            {
                "page_id": created_page_id,
                "payload": {"properties": {page_title_property: {"title": _rich_text(updated_page_title)}}},
            },
        )
        updated_page = client.tool_json("page_retrieve", {"page_id": created_page_id})
        assert _page_title_text(updated_page, page_title_property) == updated_page_title

        client.tool_json("block_trash", {"block_id": created_block_id, "confirm": True})
        _eventually(
            lambda: not _children_contain_block(
                client.tool_json("block_children_list", {"block_id": created_page_id, "page_size": 100}),
                created_block_id or "",
            ),
            timeout_seconds=30.0,
            interval_seconds=1.0,
        )
        created_block_id = None

        data_source = client.tool_json("data_source_retrieve", {"data_source_id": data_source_id})
        data_source_title_property = _data_source_title_property_name(data_source)
        created_entry = client.tool_json(
            "page_create",
            {
                "payload": {
                    "parent": {"type": "data_source_id", "data_source_id": data_source_id},
                    "properties": {data_source_title_property: {"title": _rich_text(original_entry_title)}},
                }
            },
        )
        created_entry_id = str(created_entry["id"])
        retrieved_entry = client.tool_json("page_retrieve", {"page_id": created_entry_id})
        assert _page_title_text(retrieved_entry, data_source_title_property) == original_entry_title
        original_query = client.tool_json(
            "data_source_query",
            {
                "data_source_id": data_source_id,
                "payload": {
                    "filter": {"property": data_source_title_property, "title": {"equals": original_entry_title}},
                    "page_size": 10,
                },
            },
        )
        assert _query_contains_page(original_query, created_entry_id)

        client.tool_json(
            "page_update",
            {
                "page_id": created_entry_id,
                "payload": {"properties": {data_source_title_property: {"title": _rich_text(updated_entry_title)}}},
            },
        )
        updated_entry = client.tool_json("page_retrieve", {"page_id": created_entry_id})
        assert _page_title_text(updated_entry, data_source_title_property) == updated_entry_title
        updated_query = client.tool_json(
            "data_source_query",
            {
                "data_source_id": data_source_id,
                "payload": {
                    "filter": {"property": data_source_title_property, "title": {"equals": updated_entry_title}},
                    "page_size": 10,
                },
            },
        )
        assert _query_contains_page(updated_query, created_entry_id)

        trashed_entry = client.tool_json("page_trash", {"page_id": created_entry_id, "confirm": True})
        assert trashed_entry.get("in_trash") is True
        assert client.tool_json("page_retrieve", {"page_id": created_entry_id}).get("in_trash") is True
        created_entry_id = None

        trashed_page = client.tool_json("page_trash", {"page_id": created_page_id, "confirm": True})
        assert trashed_page.get("in_trash") is True
        assert client.tool_json("page_retrieve", {"page_id": created_page_id}).get("in_trash") is True
        created_page_id = None
    finally:
        if created_block_id:
            _safe_tool_cleanup(client, "block_trash", {"block_id": created_block_id, "confirm": True})
        if created_entry_id:
            _safe_tool_cleanup(client, "page_trash", {"page_id": created_entry_id, "confirm": True})
        if created_page_id:
            _safe_tool_cleanup(client, "page_trash", {"page_id": created_page_id, "confirm": True})
        if server is not None:
            server.stop()
