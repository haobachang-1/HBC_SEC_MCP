import json
from typing import Any, Dict

from .config import MCP_PROTOCOL_VERSION


def mcp_success_response(req_id: Any, result: Dict[str, Any]) -> Dict[str, Any]:
    return {"jsonrpc": "2.0", "id": req_id, "result": result}


def mcp_error_response(req_id: Any, code: int, message: str) -> Dict[str, Any]:
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}


def handle_mcp_method(req_id: Any, method: str, params: Dict[str, Any], execute_named_tool, tools_catalog):
    if method == "initialize":
        return mcp_success_response(
            req_id,
            {
                "protocolVersion": MCP_PROTOCOL_VERSION,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "kali-mcp-http", "version": "1.0.0"},
            },
        ), 200

    if method == "notifications/initialized":
        return None, 204

    if method == "ping":
        return mcp_success_response(req_id, {}), 200

    if method == "tools/list":
        return mcp_success_response(req_id, {"tools": tools_catalog()}), 200

    if method == "tools/call":
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {}) or {}
        if not tool_name:
            return mcp_error_response(req_id, -32602, "Missing tool name"), 400

        tool_result = execute_named_tool(tool_name, arguments)
        is_error = bool(tool_result.get("error"))
        text_result = json.dumps(tool_result, ensure_ascii=False)
        return (
            mcp_success_response(
                req_id,
                {
                    "content": [{"type": "text", "text": text_result}],
                    "isError": is_error,
                },
            ),
            200,
        )

    return mcp_error_response(req_id, -32601, f"Method not found: {method}"), 404
