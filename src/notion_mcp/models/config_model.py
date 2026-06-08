"""
Pydantic 模型定义。

此处定义全局配置模型，用于存储 Notion 集成 token 和当前用户 ID。我们使用 Pydantic 的
`BaseModel` 提供类型校验、默认值和 JSON 序列化/反序列化功能。
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional


class Config(BaseModel):
    """全局配置模型。

    本模型用于保存 Notion 集成 token 和用户 UUID。字段直接以蛇形命名序列化到 JSON 文件，不做别名转换，以避免兼容性问题。
    """

    notion_token: Optional[str] = Field(default=None, description="Notion 集成访问令牌")
    user_id: Optional[str] = Field(default=None, description="当前用户的 Notion UUID")