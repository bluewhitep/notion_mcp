# File: src/notion_mcp/core/errors.py
# Format: UTF-8
# =============================
# File Description:
# Unified Core error types shared by CLI, REST compatibility code, and MCP tools.
# TAG: core, errors
# =============================

from __future__ import annotations

from typing import Any


class CoreError(Exception):
    default_code = "core_error"

    # --------------------------------
    # Function Description:
    # Initializes a serializable Core error.
    # Inputs/Outputs:
    # Input message/code/details; output is an exception with stable public fields.
    # Usage:
    # CoreError("failed", code="example").to_dict()
    # --------------------------------
    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code or self.default_code
        self.details = details or {}

    # --------------------------------
    # Function Description:
    # Serializes an error for CLI JSON and MCP structured responses.
    # Inputs/Outputs:
    # No input; returns a dictionary with type, code, message, and details.
    # Usage:
    # error.to_dict()
    # --------------------------------
    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.__class__.__name__,
            "code": self.code,
            "message": self.message,
            "details": self.details,
        }


class ConfigNotFoundError(CoreError):
    default_code = "config_not_found"

    # --------------------------------
    # Function Description:
    # Builds an error for a missing local configuration file.
    # Inputs/Outputs:
    # Input path string; output is ConfigNotFoundError with path details.
    # Usage:
    # raise ConfigNotFoundError("/tmp/config.json")
    # --------------------------------
    def __init__(self, path: str) -> None:
        super().__init__(
            f"Configuration file does not exist: {path}",
            details={"path": path},
        )


class ConfigValidationError(CoreError):
    default_code = "config_validation_failed"

    # --------------------------------
    # Function Description:
    # Builds an error for invalid Core configuration data.
    # Inputs/Outputs:
    # Input message/details; output is ConfigValidationError.
    # Usage:
    # raise ConfigValidationError("Invalid user_id")
    # --------------------------------
    def __init__(
        self,
        message: str,
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, details=details)


class NotionAuthError(CoreError):
    default_code = "notion_auth_failed"

    # --------------------------------
    # Function Description:
    # Builds an error for Notion token validation failures.
    # Inputs/Outputs:
    # Input message/details; output is NotionAuthError.
    # Usage:
    # raise NotionAuthError("Invalid token")
    # --------------------------------
    def __init__(
        self,
        message: str,
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message, details=details)


class NotionOperationError(CoreError):
    default_code = "notion_operation_failed"

    # --------------------------------
    # Function Description:
    # Builds an error for a failed Notion SDK operation.
    # Inputs/Outputs:
    # Input operation/message/details; output is NotionOperationError.
    # Usage:
    # raise NotionOperationError("pages.retrieve", "failed")
    # --------------------------------
    def __init__(
        self,
        operation: str,
        message: str,
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        merged_details = {"operation": operation}
        if details:
            merged_details.update(details)
        super().__init__(message, details=merged_details)
