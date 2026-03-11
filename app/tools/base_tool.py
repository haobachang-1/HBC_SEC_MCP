from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseTool(ABC):
    """Base class for all tools discovered by dispatcher."""

    name: str = ""
    description: str = ""
    input_schema: Dict[str, Any] = {"type": "object", "properties": {}, "additionalProperties": True}

    @abstractmethod
    def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tool with input params and return structured result."""

    def mcp_definition(self) -> Dict[str, Any]:
        """Build MCP tool definition from class attributes."""
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema,
        }
