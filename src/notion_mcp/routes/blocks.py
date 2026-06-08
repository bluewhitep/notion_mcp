"""
区块相关路由。

提供列出区块子元素、更新区块和追加子区块等功能。
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
    """列出区块的子元素。"""
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
    """在区块末尾追加子元素。``body`` 应包含 ``children`` 字段。"""
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
    """更新区块内容。根据区块类型传入相应字段。"""
    try:
        result = client.blocks.update(block_id=block_id, **body)  # type: ignore[attr-defined]
        return cast(Dict[str, Any], result)
    except APIResponseError as err:
        raise HTTPException(status_code=err.status, detail=str(err))
