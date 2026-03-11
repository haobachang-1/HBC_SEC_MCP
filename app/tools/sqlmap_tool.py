from typing import Any, Dict, Optional, Tuple

from ..command_executor import execute_command
from ..config import TOOL_SQLMAP_SCAN
from .base_tool import BaseTool


PYTHON_PATH = r"E:\saber\bin\python2\python.exe"
SQLMAP_PATH = r"E:\saber\tools\web\sql\sqlmap\sqlmap.py"


class SqlmapTool(BaseTool):
    """SQLMap tool implementation with unified run() interface."""

    name = TOOL_SQLMAP_SCAN
    description = "Run sqlmap scan."
    input_schema = {
        "type": "object",
        "properties": {
            "url": {"type": "string"},
            "data": {"type": "string"},
            "additional_args": {"type": "string"},
        },
        "required": ["url"],
    }

    @staticmethod
    def _parse_params(params: Dict[str, Any]) -> Tuple[Optional[Dict[str, str]], Optional[str]]:
        url = str(params.get("url", "")).strip()
        if not url:
            return None, "url is required"

        normalized = {
            "url": url,
            "data": str(params.get("data", "")).strip(),
            "additional_args": str(params.get("additional_args", "")).strip(),
        }
        return normalized, None

    @staticmethod
    def _build_command(url: str, data: str = "", additional_args: str = "") -> str:
        command = f'"{PYTHON_PATH}" "{SQLMAP_PATH}" -u {url} --batch'
        if data:
            command += f' --data="{data}"'
        if additional_args:
            command += f" {additional_args}"
        return command

    def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        normalized, error = self._parse_params(params)
        if error:
            return {"error": error, "success": False}

        command = self._build_command(
            url=normalized["url"],
            data=normalized["data"],
            additional_args=normalized["additional_args"],
        )
        return execute_command(command)
