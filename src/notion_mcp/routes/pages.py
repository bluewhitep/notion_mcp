"""
Page-related routes.

Provides page retrieval, creation, and update operations.
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
    """Retrieve page details."""
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
    """Create a new page.

    Example body:

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
    """Update page properties."""
    try:
        result = client.pages.update(page_id=page_id, **body)
        return cast(Dict[str, Any], result)
    except APIResponseError as err:
        raise HTTPException(status_code=err.status, detail=str(err))
