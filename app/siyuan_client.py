from __future__ import annotations

import base64
from pathlib import Path
from typing import Any, Dict, Optional

import requests

from .config import SIYUAN_API_TOKEN, SIYUAN_BASE_URL, SIYUAN_TIMEOUT


class SiYuanClient:
    """Simple REST client for SiYuan API."""

    def __init__(
        self,
        base_url: str = SIYUAN_BASE_URL,
        token: str = SIYUAN_API_TOKEN,
        timeout: int = SIYUAN_TIMEOUT,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token.strip()
        self.timeout = timeout

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Token {self.token}"
        return headers

    def _url(self, api_path: str) -> str:
        return f"{self.base_url}/{api_path.lstrip('/')}"

    def call(self, api_path: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        try:
            response = requests.post(
                self._url(api_path),
                json=payload or {},
                headers=self._headers(),
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as exc:
            return {"success": False, "error": f"request failed: {exc}"}
        except ValueError:
            return {"success": False, "error": "invalid JSON response from SiYuan"}

        if isinstance(data, dict) and data.get("code") not in (None, 0):
            message = data.get("msg") or data.get("message") or "SiYuan API returned error"
            return {"success": False, "error": message, "raw": data}

        return {"success": True, "data": data}

    def upload_asset(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        file_path = str(payload.get("file_path", "")).strip()
        file_name = str(payload.get("file_name", "")).strip()
        content_b64 = str(payload.get("content_base64", "")).strip()
        assets_dir_path = str(payload.get("assets_dir_path", "")).strip()

        files = None
        try:
            if file_path:
                path = Path(file_path)
                if not path.exists() or not path.is_file():
                    return {"success": False, "error": f"file_path not found: {file_path}"}
                files = {"file[]": (path.name, path.read_bytes())}
            elif file_name and content_b64:
                try:
                    raw = base64.b64decode(content_b64)
                except Exception as exc:  # noqa: BLE001
                    return {"success": False, "error": f"invalid content_base64: {exc}"}
                files = {"file[]": (file_name, raw)}
            else:
                return {
                    "success": False,
                    "error": "upload_asset requires file_path OR (file_name + content_base64)",
                }

            data = {}
            if assets_dir_path:
                data["assetsDirPath"] = assets_dir_path

            headers = {}
            if self.token:
                headers["Authorization"] = f"Token {self.token}"

            response = requests.post(
                self._url("/api/asset/upload"),
                data=data,
                files=files,
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            result = response.json()
        except requests.RequestException as exc:
            return {"success": False, "error": f"request failed: {exc}"}
        except ValueError:
            return {"success": False, "error": "invalid JSON response from SiYuan"}

        if isinstance(result, dict) and result.get("code") not in (None, 0):
            message = result.get("msg") or result.get("message") or "SiYuan API returned error"
            return {"success": False, "error": message, "raw": result}

        return {"success": True, "data": result}
