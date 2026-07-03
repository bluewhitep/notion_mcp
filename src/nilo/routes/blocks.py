"""
Block-related routes.

Provides operations for listing, updating, and appending block children.
"""

from __future__ import annotations

from typing import Any, Dict, cast

from fastapi import APIRouter, Body, Depends, HTTPException

try:
    from notion_client import APIResponseError, Client as NotionClient  # type: ignore
except ImportError:
    from typing import Any

    APIResponseError = Exception  # type: ignore
    NotionClient = Any  # type: ignore

from ..dependencies import get_notion_client


router = APIRouter(prefix="/blocks", tags=["blocks"])


@router.get("/{block_id}/children")
async def list_block_children(
    block_id: str,
    client: NotionClient = Depends(get_notion_client),
) -> Dict[str, Any]:
    """List child blocks for a block."""
    try:
        result = client.blocks.children.list(block_id=block_id)  # type: ignore[attr-defined]
        return cast(Dict[str, Any], result)
    except APIResponseError as err:
        raise HTTPException(status_code=err.status, detail=str(err))


@router.post("/{block_id}/append")
async def append_block_children(
    block_id: str,
    body: Dict[str, Any] = Body(...),
    client: NotionClient = Depends(get_notion_client),
) -> Dict[str, Any]:
    """Append child blocks to a block. ``body`` should include ``children``."""
    try:
        result = client.blocks.children.append(block_id=block_id, **body)  # type: ignore[attr-defined]
        return cast(Dict[str, Any], result)
    except APIResponseError as err:
        raise HTTPException(status_code=err.status, detail=str(err))


@router.patch("/{block_id}")
async def update_block(
    block_id: str,
    body: Dict[str, Any] = Body(...),
    client: NotionClient = Depends(get_notion_client),
) -> Dict[str, Any]:
    """Update block content with fields matching the block type."""
    try:
        result = client.blocks.update(block_id=block_id, **body)  # type: ignore[attr-defined]
        return cast(Dict[str, Any], result)
    except APIResponseError as err:
        raise HTTPException(status_code=err.status, detail=str(err))
