# File: src/nilo/core/auth.py
# Format: UTF-8
# =============================
# File Description:
# Notion authentication validation service for configured bearer tokens.
# TAG: core, auth, notion-sdk
# =============================

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .errors import NotionAuthError


@dataclass(frozen=True)
class AuthValidationResult:
    valid: bool
    user_id: str | None
    name: str | None
    raw: dict[str, Any]


class AuthService:
    # --------------------------------
    # Function Description:
    # Initializes auth validation with a Notion SDK-compatible client.
    # Inputs/Outputs:
    # Input client exposing users.me; output is AuthService.
    # Usage:
    # AuthService(client).validate()
    # --------------------------------
    def __init__(self, client: Any) -> None:
        self.client = client

    # --------------------------------
    # Function Description:
    # Validates a token by retrieving the current Notion bot/user.
    # Inputs/Outputs:
    # Optional expected user UUID; returns AuthValidationResult or raises NotionAuthError.
    # Usage:
    # AuthService(client).validate(expected_user_id=user_uuid)
    # --------------------------------
    def validate(self, *, expected_user_id: str | None = None) -> AuthValidationResult:
        try:
            raw = self.client.users.me()
        except Exception as exc:
            raise NotionAuthError(str(exc)) from exc
        if not isinstance(raw, dict):
            raise NotionAuthError("Notion users.me returned a non-object response")
        user_id = raw.get("id")
        name = raw.get("name")
        if not isinstance(user_id, str):
            raise NotionAuthError("Notion users.me response does not include a user id")
        if expected_user_id and user_id != expected_user_id:
            raise NotionAuthError(
                "Configured user_id does not match the authenticated Notion user",
                details={"expected_user_id": expected_user_id, "actual_user_id": user_id},
            )
        return AuthValidationResult(
            valid=True,
            user_id=user_id,
            name=name if isinstance(name, str) else None,
            raw=raw,
        )


# --------------------------------
# Function Description:
# Validates a Notion client with an optional expected user UUID.
# Inputs/Outputs:
# Input client and optional expected id; returns AuthValidationResult.
# Usage:
# validate_auth(client, expected_user_id=user_uuid)
# --------------------------------
def validate_auth(
    client: Any,
    *,
    expected_user_id: str | None = None,
) -> AuthValidationResult:
    return AuthService(client).validate(expected_user_id=expected_user_id)
