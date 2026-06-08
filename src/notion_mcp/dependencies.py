"""
FastAPI 依赖定义。

为了避免循环导入，将获取配置和初始化 Notion 客户端的依赖函数独立放在此模块。
"""

from __future__ import annotations

from fastapi import Depends, HTTPException
from typing import Any

from .config import load_config
from .models import Config

try:
    from notion_client import Client as NotionClient  # type: ignore
except ImportError:
    NotionClient = Any  # type: ignore


def get_config() -> Config:
    """读取并返回当前配置。

    如果配置文件不存在或 token 未设置，则抛出 HTTP 500 异常，提示用户先初始化配置。
    """
    try:
        config = load_config()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="配置文件不存在，请先运行 notion-mcp init")
    if not config.notion_token:
        raise HTTPException(status_code=500, detail="未设置 Notion token，请运行 notion-mcp set-token")
    return config


def get_notion_client(config: Config = Depends(get_config)) -> NotionClient:
    """根据配置初始化并返回 Notion 客户端。"""
    return NotionClient(auth=config.notion_token)  # type: ignore