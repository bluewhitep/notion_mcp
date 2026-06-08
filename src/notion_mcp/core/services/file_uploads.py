# File: src/notion_mcp/core/services/file_uploads.py
# Format: UTF-8
# =============================
# File Description:
# Core service for Notion file upload operations.
# TAG: core, services, file-uploads
# =============================

from __future__ import annotations

from typing import Any

from .base import BaseNotionService


class FileUploadsService(BaseNotionService):
    # --------------------------------
    # Function Description:
    # Lists Notion file upload objects when supported by the SDK.
    # Inputs/Outputs:
    # Input optional paging params; returns Notion list response.
    # Usage:
    # FileUploadsService(client).list(page_size=10)
    # --------------------------------
    def list(self, **params: Any) -> dict[str, Any]:
        return self._call("file_uploads.list", self.client.file_uploads.list, **params)

    # --------------------------------
    # Function Description:
    # Creates a Notion file upload object.
    # Inputs/Outputs:
    # Input raw payload; returns Notion file upload create response.
    # Usage:
    # FileUploadsService(client).create({"mode": "single_part"})
    # --------------------------------
    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._call("file_uploads.create", self.client.file_uploads.create, **payload)

    # --------------------------------
    # Function Description:
    # Retrieves a Notion file upload object.
    # Inputs/Outputs:
    # Input file_upload_id; returns Notion retrieve response.
    # Usage:
    # FileUploadsService(client).retrieve("file-upload-id")
    # --------------------------------
    def retrieve(self, file_upload_id: str) -> dict[str, Any]:
        return self._call(
            "file_uploads.retrieve",
            self.client.file_uploads.retrieve,
            file_upload_id=file_upload_id,
        )

    # --------------------------------
    # Function Description:
    # Sends file content through the SDK file upload object.
    # Inputs/Outputs:
    # Input file_upload_id and raw send payload; returns SDK response.
    # Usage:
    # FileUploadsService(client).send("file-upload-id", {"file": handle})
    # --------------------------------
    def send(self, file_upload_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self._call(
            "file_uploads.send",
            self.client.file_uploads.send,
            file_upload_id=file_upload_id,
            **payload,
        )

    # --------------------------------
    # Function Description:
    # Completes a multipart file upload when supported by the SDK.
    # Inputs/Outputs:
    # Input file_upload_id and raw payload; returns Notion complete response.
    # Usage:
    # FileUploadsService(client).complete("file-upload-id", {})
    # --------------------------------
    def complete(self, file_upload_id: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._call(
            "file_uploads.complete",
            self.client.file_uploads.complete,
            file_upload_id=file_upload_id,
            **(payload or {}),
        )
