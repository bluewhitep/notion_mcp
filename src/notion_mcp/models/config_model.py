"""
Pydantic model definitions.

Defines the global configuration model used to store the Notion integration
token and current user ID.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional


class Config(BaseModel):
    """Global configuration model.

    Stores the Notion integration token and user UUID using snake_case JSON fields.
    """

    notion_token: Optional[str] = Field(default=None, description="Notion integration access token")
    user_id: Optional[str] = Field(default=None, description="Current Notion user UUID")
