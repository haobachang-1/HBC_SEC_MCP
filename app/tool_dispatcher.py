import importlib
import inspect
import pkgutil
from typing import Any, Callable, Dict

from .tools import __path__ as tools_path
from .tools.base_tool import BaseTool

ToolHandler = Callable[[Dict[str, Any]], Dict[str, Any]]

_TOOL_HANDLERS: Dict[str, ToolHandler] = {}
_TOOL_DEFINITIONS: Dict[str, Dict[str, Any]] = {}


def register_tool(tool_name: str, handler: ToolHandler, definition: Dict[str, Any]) -> None:
    _TOOL_HANDLERS[tool_name] = handler
    _TOOL_DEFINITIONS[tool_name] = definition


def execute_named_tool(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    handler = _TOOL_HANDLERS.get(tool_name)
    if not handler:
        return {"error": f"Unsupported tool: {tool_name}", "success": False}
    return handler(params)


def mcp_tools_catalog() -> list[Dict[str, Any]]:
    return list(_TOOL_DEFINITIONS.values())


def _discover_tool_classes() -> list[type[BaseTool]]:
    discovered: list[type[BaseTool]] = []

    for module_info in pkgutil.iter_modules(tools_path):
        module_name = module_info.name
        if module_name.startswith("_") or module_name == "base_tool":
            continue

        module = importlib.import_module(f"app.tools.{module_name}")
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if not issubclass(obj, BaseTool) or obj is BaseTool:
                continue
            if obj.__module__ != module.__name__:
                continue
            discovered.append(obj)

    return discovered


def _register_discovered_tools() -> None:
    for tool_cls in _discover_tool_classes():
        tool = tool_cls()
        if not tool.name:
            continue
        register_tool(tool.name, tool.run, tool.mcp_definition())


_register_discovered_tools()
