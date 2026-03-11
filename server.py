#!/usr/bin/env python3

# 该脚本用于启动一个面向 SQLMap 的 MCP + HTTP API 服务。

# 导入命令行参数解析模块。
import argparse
# 导入日志模块。
import logging
# 导入操作系统能力模块（用于环境变量和平台判断）。
import os
# 导入异常堆栈格式化模块。
import traceback
# 导入类型注解所需类型。
from typing import Any, Dict

# 从 Flask 导入应用、JSON 响应与请求对象。
from flask import Flask, jsonify, request

# 导入命令执行入口函数。
from app.command_executor import execute_command
# 导入基础配置常量（端口、调试开关、工具名常量）。
from app.config import API_PORT, DEBUG_MODE, TOOL_SQLMAP_SCAN
# 导入日志初始化函数。
from app.logging_setup import configure_logging
# 导入 MCP 方法分发与错误响应构造函数。
from app.mcp_protocol import handle_mcp_method, mcp_error_response
# 导入工具调度与工具目录函数。
from app.tool_dispatcher import execute_named_tool, mcp_tools_catalog


# 初始化日志器（使用统一日志配置）。
logger = configure_logging()
# 初始化 Flask 应用实例。
app = Flask(__name__)


# 读取并规范化请求体 JSON，保证返回 dict。
def _get_request_json() -> Dict[str, Any]:
    # 以静默模式解析 JSON，解析失败时返回 None。
    payload = request.get_json(silent=True)
    # 若解析结果是字典则返回，否则返回空字典。
    return payload if isinstance(payload, dict) else {}


# 统一构造错误响应（JSON + 状态码）。
def _json_error(message: str, status_code: int = 400):
    # 返回标准错误结构和对应 HTTP 状态码。
    return jsonify({"error": message}), status_code


# 检查指定命令行工具是否可用。
def _tool_exists(tool: str) -> bool:
    # Windows 使用 where，其他平台使用 which。
    lookup_cmd = f"where {tool}" if os.name == "nt" else f"which {tool}"
    # 调用统一命令执行器执行检测命令。
    result = execute_command(lookup_cmd)
    # 根据执行结果中的 success 字段返回布尔值。
    return bool(result.get("success"))


# 根路径同时提供 GET 说明与 POST 的 MCP JSON-RPC 入口。
@app.route("/", methods=["GET", "POST"])
def mcp_root():
    """MCP JSON-RPC endpoint for clients using HTTP transport at root path."""  # MCP 根入口说明。
    # 若为 GET 请求，返回服务说明信息。
    if request.method == "GET":
        # 返回可供调用方查看的服务元数据。
        return jsonify(
            {
                # 服务名称。
                "name": "HBC-Sec-mcp-http",
                # 调用提示信息。
                "message": "Use POST / with MCP JSON-RPC.",
                # 健康检查地址。
                "health": "/health",
                # 能力发现地址。
                "capabilities": "/mcp/capabilities",
            }
        )

    # 获取 POST 请求体中的 MCP JSON 内容。
    payload = _get_request_json()
    # 读取请求 id（用于 JSON-RPC 响应对应）。
    req_id = payload.get("id")
    # 读取方法名。
    method = payload.get("method", "")
    # 读取参数对象，若为空则置空字典。
    params = payload.get("params", {}) or {}

    # 若没有方法名，返回 JSON-RPC Invalid Request 错误。
    if not method:
        return jsonify(mcp_error_response(req_id, -32600, "Invalid Request")), 400

    # 交给 MCP 协议层处理，返回结构化结果与状态码。
    response, status_code = handle_mcp_method(
        # 传入请求 id。
        req_id=req_id,
        # 传入方法名。
        method=method,
        # 传入参数对象。
        params=params,
        # 传入工具执行分发函数。
        execute_named_tool=execute_named_tool,
        # 传入工具目录查询函数。
        tools_catalog=mcp_tools_catalog,
    )
    # 对 notifications/initialized 等无响应体场景直接返回空体。
    if response is None:
        return "", status_code
    # 其余场景返回 JSON 响应体和状态码。
    return jsonify(response), status_code


# SQLMap 的 HTTP 直连路由。
@app.route("/api/tools/sqlmap", methods=["POST"])
def sqlmap():
    """Execute sqlmap with the provided parameters."""  # SQLMap 执行接口说明。
    # 进入异常保护，避免异常直接中断请求。
    try:
        # 读取请求参数。
        params = _get_request_json()
        # 通过工具名动态分发到对应工具类 run 方法。
        result = execute_named_tool(TOOL_SQLMAP_SCAN, params)
        # 若工具层返回 error 字段，则按 400 返回。
        if result.get("error"):
            return _json_error(result["error"], 400)
        # 正常返回工具执行结果。
        return jsonify(result)
    # 捕获所有异常并返回统一错误结构。
    except Exception as e:
        # 记录简要异常信息。
        logger.error(f"Error in sqlmap endpoint: {str(e)}")
        # 记录完整堆栈，便于定位问题。
        logger.error(traceback.format_exc())
        # 返回 500 错误响应。
        return _json_error(f"Server error: {str(e)}", 500)


# 健康检查路由。
@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""  # 健康检查接口说明。
    # 检测 sqlmap 命令是否存在并记录状态。
    tools_status = {"sqlmap": _tool_exists("sqlmap")}
    # 汇总所有关键工具状态。
    all_essential_tools_available = all(tools_status.values())

    # 返回健康检查结果。
    return jsonify(
        {
            # 服务状态。
            "status": "healthy",
            # 服务说明信息。
            "message": "API Server is running",
            # 工具状态详情。
            "tools_status": tools_status,
            # 关键工具是否都可用。
            "all_essential_tools_available": all_essential_tools_available,
        }
    )


# MCP 能力发现路由。
@app.route("/mcp/capabilities", methods=["GET"])
def get_capabilities():
    # 在这里配置服务器的能力和工具信息，供 MCP 客户端查询。
    # 将 tools/list 定义转换为 capabilities 所需的简化结构。
    tools = []
    # 遍历当前已注册工具目录。
    for tool in mcp_tools_catalog():
        # 读取工具名。
        tool_name = tool.get("name")
        # 读取 inputSchema.required 作为必填参数列表。
        required = ((tool.get("inputSchema") or {}).get("required") or [])
        # 追加到 capabilities 输出结构。
        tools.append({"name": tool_name, "required": required})

    # 返回服务能力与工具列表。
    return jsonify(
        {
            # 服务标识名称。
            "server": "HBC-Sec-mcp-http",
            # 服务版本号。
            "version": "1.0",
            # 统一工具调用入口。
            "execute_endpoint": "/mcp/tools/HBC-Sec_mcp_tools/<tool_name>",
            # 对外暴露工具列表。
            "tools": tools,
        }
    )


# HTTP 风格的统一工具调用入口。
@app.route("/mcp/tools/HBC-Sec_mcp_tools/<tool_name>", methods=["POST"])
def execute_tool(tool_name):
    # 进入异常保护，防止执行错误导致服务崩溃。
    try:
        # 读取请求参数。
        params = _get_request_json()
        # 按工具名动态分发执行。
        result = execute_named_tool(tool_name, params)
        # 若包含 error 字段则返回 400，否则返回 200。
        status_code = 400 if result.get("error") else 200
        # 返回工具执行结果。
        return jsonify(result), status_code
    # 捕获所有异常并记录日志。
    except Exception as e:
        # 记录简要错误信息。
        logger.error(f"Error executing tool {tool_name}: {str(e)}")
        # 记录完整异常堆栈。
        logger.error(traceback.format_exc())
        # 返回统一 500 错误响应。
        return jsonify({"error": f"Server error: {str(e)}", "success": False}), 500


# 解析命令行启动参数。
def parse_args():
    """Parse command line arguments."""  # 命令行参数解析函数说明。
    # 创建参数解析器。 
    parser = argparse.ArgumentParser(description="Run the HBC-SecMCP API Server")
    # 是否开启调试模式。
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    # 指定监听端口。
    parser.add_argument("--port", type=int, default=API_PORT, help=f"Port for the API server (default: {API_PORT})")
    # 指定监听 IP。
    parser.add_argument(
        # 参数名。
        "--ip",
        # 参数类型。
        type=str,
        # 默认值。
        default="127.0.0.1",
        # 参数帮助文本。
        help="IP address to bind the server to (default: 127.0.0.1 for localhost only)",
    )
    # 返回解析后的参数对象。
    return parser.parse_args()


# 主入口：直接运行该文件时启动服务。
if __name__ == "__main__":
    # 解析启动参数。
    args = parse_args()
    # 运行时调试开关初值来自配置。
    runtime_debug = DEBUG_MODE
    # 运行时端口初值来自配置。
    runtime_port = API_PORT

    # 若命令行指定 --debug，则强制开启调试。
    if args.debug:
        # 更新运行时调试标志。
        runtime_debug = True
        # 同步写入环境变量，供其他模块读取。
        os.environ["DEBUG_MODE"] = "1"
        # 提升 logger 级别到 DEBUG。
        logger.setLevel(logging.DEBUG)

    # 若命令行端口与默认端口不同，则覆盖运行时端口。
    if args.port != runtime_port:
        runtime_port = args.port

    # 输出启动日志。
    logger.info(f"Starting HBC-SecMCP API Server on {args.ip}:{runtime_port}")
    # 启动 Flask 服务。
    app.run(host=args.ip, port=runtime_port, debug=runtime_debug)
