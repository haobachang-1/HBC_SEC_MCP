from typing import Any, Dict, Optional, Tuple

from .base_tool import BaseTool


class XxxTool(BaseTool):
    """Template tool: copy this file and rename class/module for a new tool."""

    # Tool unique name used by MCP tools/call and HTTP dispatcher.
    name = "xxx_tool"

    # Tool description shown in tools/list.
    description = "Run xxx tool."

    # MCP input schema for this tool.
    input_schema = {
        "type": "object",
        "properties": {
            "target": {"type": "string"},
            "additional_args": {"type": "string"},
        },
        "required": ["target"],
    }

    @staticmethod
    def _parse_params(params: Dict[str, Any]) -> Tuple[Optional[Dict[str, str]], Optional[str]]:
        target = str(params.get("target", "")).strip()
        if not target:
            return None, "target is required"

        normalized = {
            "target": target,
            "additional_args": str(params.get("additional_args", "")).strip(),
        }
        return normalized, None

    @staticmethod
    def _build_command(target: str, additional_args: str = "") -> str:
        command = f"echo running xxx for {target}"
        if additional_args:
            command += f" {additional_args}"
        return command

    def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        normalized, error = self._parse_params(params)
        if error:
            return {"error": error, "success": False}

        command = self._build_command(
            target=normalized["target"],
            additional_args=normalized["additional_args"],
        )

        # Replace this mock response with real execution logic.
        return {
            "success": True,
            "message": "Template tool executed",
            "command": command,
        }
