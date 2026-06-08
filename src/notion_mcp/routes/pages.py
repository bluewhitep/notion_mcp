"""
页面相关路由。

提供页面的读取、创建和更新功能。根据 Notion API，可通过 `pages.retrieve`、
`pages.create` 和 `pages.update` 进行操作。
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


router = APIRouter(prefix="/pages", tags=["pages"])


@router.get("/{page_id}")
async def get_page(
    page_id: str,
    client: NotionClient = Depends(get_notion_client),
) -> Dict[str, Any]:
    """获取页面详情。"""
    try:
        result = client.pages.retrieve(page_id=page_id)
        return cast(Dict[str, Any], result)
    except APIResponseError as err:
        raise HTTPException(status_code=err.status, detail=str(err))


@router.post("/")
async def create_page(
    body: Dict[str, Any] = Body(...),
    client: NotionClient = Depends(get_notion_client),
) -> Dict[str, Any]:
    """创建新的页面。

    请求体示例：

    ```json
    {
      "parent": {"data_source_id": "..."},
      "properties": {"Name": {"title": [{"text": {"content": "Example"}}]}},
      "children": []
    }
    ```
    """
    try:
        result = client.pages.create(**body)
        return cast(Dict[str, Any], result)
    except APIResponseError as err:
        raise HTTPException(status_code=err.status, detail=str(err))


@router.patch("/{page_id}")
async def update_page(
    page_id: str,
    body: Dict[str, Any] = Body(...),
    client: NotionClient = Depends(get_notion_client),
) -> Dict[str, Any]:
    """更新页面属性。"""
    try:
        result = client.pages.update(page_id=page_id, **body)
        return cast(Dict[str, Any], result)
    except APIResponseError as err:
        raise HTTPException(status_code=err.status, detail=str(err))
