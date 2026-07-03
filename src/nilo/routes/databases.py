"""
Database-related routes.

Provides listing, retrieval, and query operations for data sources and legacy
database compatibility paths.
"""

from __future__ import annotations

from typing import Any, Dict, cast

from fastapi import APIRouter, Body, Depends, HTTPException

try:
    from notion_client import APIResponseError, Client as NotionClient  # type: ignore
except ImportError:
    # Define placeholders so tests can import this module without notion-client.
    APIResponseError = Exception  # type: ignore
    NotionClient = Any  # type: ignore

from ..dependencies import get_notion_client


router = APIRouter(prefix="/databases", tags=["databases"])


@router.get("/")
async def list_databases(
    kind: str = "data_source",
    client: NotionClient = Depends(get_notion_client),
) -> Dict[str, Any]:
    """List databases or data sources.

    Args:
        kind: Query type, either ``data_source`` or ``database``. Defaults to data sources.
        client: Injected Notion client.

    Returns:
        Search results returned by Notion.

    Raises:
        HTTPException: Raised when accessing the Notion API fails.
    """
    if kind not in {"data_source", "database"}:
        raise HTTPException(status_code=400, detail="kind must be data_source or database")
    try:
        # Filter search results by object type.
        search_filter = {"value": kind, "property": "object"}
        result = client.search(filter=search_filter)
        return cast(Dict[str, Any], result)
    except APIResponseError as err:
        raise HTTPException(status_code=err.status, detail=str(err))


@router.get("/{data_source_id}")
async def retrieve_database(
    data_source_id: str,
    client: NotionClient = Depends(get_notion_client),
) -> Dict[str, Any]:
    """Retrieve metadata for a data source or legacy database.

    Prefers ``data_sources.retrieve`` and falls back to legacy ``databases.retrieve``.
    """
    try:
        result = client.data_sources.retrieve(data_source_id=data_source_id)  # type: ignore[attr-defined]
        return cast(Dict[str, Any], result)
    except Exception:
        # Fall back to the legacy database endpoint when data source retrieval fails.
        try:
            result = client.databases.retrieve(database_id=data_source_id)  # type: ignore[attr-defined]
            return cast(Dict[str, Any], result)
        except APIResponseError as err:
            raise HTTPException(status_code=err.status, detail=str(err))


@router.post("/{data_source_id}/query")
async def query_database(
    data_source_id: str,
    payload: Dict[str, Any] = Body(default_factory=dict),
    client: NotionClient = Depends(get_notion_client),
) -> Dict[str, Any]:
    """Query a data source or legacy database.

    The ``payload`` body is passed directly to the Notion query endpoint.
    """
    try:
        # Query by data source first.
        result = client.data_sources.query(data_source_id=data_source_id, **payload)  # type: ignore[attr-defined]
        return cast(Dict[str, Any], result)
    except Exception:
        try:
            result = client.databases.query(database_id=data_source_id, **payload)  # type: ignore[attr-defined]
            return cast(Dict[str, Any], result)
        except APIResponseError as err:
            raise HTTPException(status_code=err.status, detail=str(err))
