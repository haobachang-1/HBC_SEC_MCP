from typing import Any, Dict

from ..command_executor import execute_command
from .base_tool import BaseTool


class CommandExecTool(BaseTool):
    """Generic command execution tool with unified run() interface."""

    name = "execute_command"
    description = "Execute an arbitrary shell command."
    input_schema = {
        "type": "object",
        "properties": {
            "command": {"type": "string"},
        },
        "required": ["command"],
    }

    def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        command = str(params.get("command", "")).strip()
        if not command:
            return {"error": "command is required", "success": False}
        return execute_command(command)
