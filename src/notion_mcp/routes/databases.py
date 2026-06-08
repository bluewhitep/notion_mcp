"""
数据库相关路由。

提供数据源/数据库的列表、详情查询和查询操作。根据 Notion API 2025-09-03 版的规范，
数据库相关操作通常以 data source 为主，而旧版本仍保留 `database` 概念。
"""

from __future__ import annotations

from typing import Any, Dict, cast

from fastapi import APIRouter, Body, Depends, HTTPException

try:
    from notion_client import APIResponseError, Client as NotionClient  # type: ignore
except ImportError:
    # 定义占位符以便测试环境未安装 notion-client 时仍可导入
    APIResponseError = Exception  # type: ignore
    NotionClient = Any  # type: ignore

from ..dependencies import get_notion_client


router = APIRouter(prefix="/databases", tags=["databases"])


@router.get("/")
async def list_databases(
    kind: str = "data_source",
    client: NotionClient = Depends(get_notion_client),
) -> Dict[str, Any]:
    """列出数据库或数据源。

    Args:
        kind: 查询类型，可选值为 ``data_source`` 或 ``database``。默认查询数据源。
        client: 注入的 Notion 客户端。

    Returns:
        Notion 返回的搜索结果。

    Raises:
        HTTPException: 当访问 Notion API 失败时。
    """
    if kind not in {"data_source", "database"}:
        raise HTTPException(status_code=400, detail="kind 参数必须为 data_source 或 database")
    try:
        # 根据对象类型过滤搜索结果
        search_filter = {"value": kind, "property": "object"}
        result = client.search(filter=search_filter)
        return cast(Dict[str, Any], result)  # FastAPI 会自动转为 JSON
    except APIResponseError as err:
        raise HTTPException(status_code=err.status, detail=str(err))


@router.get("/{data_source_id}")
async def retrieve_database(
    data_source_id: str,
    client: NotionClient = Depends(get_notion_client),
) -> Dict[str, Any]:
    """获取特定数据源或数据库的元数据。

    根据 API 版本优先调用 ``data_sources.retrieve``，若发生 404 则退回调用旧版 ``databases.retrieve``。
    """
    try:
        result = client.data_sources.retrieve(data_source_id=data_source_id)  # type: ignore[attr-defined]
        return cast(Dict[str, Any], result)
    except Exception:
        # 如果 data_sources.retrieve 不存在或发生错误，则尝试旧版接口
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
    """查询数据源或数据库。

    请求体 ``payload`` 将直接传递给 Notion API 的查询接口，常用字段包括 ``filter``、``sorts``、``page_size`` 等。
    """
    try:
        # 根据 data source 查询
        result = client.data_sources.query(data_source_id=data_source_id, **payload)  # type: ignore[attr-defined]
        return cast(Dict[str, Any], result)
    except Exception:
        try:
            result = client.databases.query(database_id=data_source_id, **payload)  # type: ignore[attr-defined]
            return cast(Dict[str, Any], result)
        except APIResponseError as err:
            raise HTTPException(status_code=err.status, detail=str(err))
