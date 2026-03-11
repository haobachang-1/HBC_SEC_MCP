# 好靶场

http://www.loveli.com.cn

好靶场
团队宗旨：我们立志于为所有的网络安全同伴制作出好的靶场，让所有初学者都可以用最低的成本入门网络安全。所以我们团队名称就叫“好靶场”。

我们承诺每天至少更新1-2个新靶场。2026年冲刺1000个。

• 全球第一家以SRC报告为蓝图制作靶场的网络安全靶场平台。
• 全球第一家引入AI靶场助教的网络安全靶场平台。
• 14个不同方向靶场供你选择。
• 代码审计+漏洞修复靶场全新上架。
• 无门槛费，每次开启不扣除积分，不扣除金币，超级会员每天不限次数开启靶场。
• 靶场独立，每个靶场环境完全隔离。

# HBC_SEC_MCP

本项目为好靶场开源的MCP框架，大家可以基于本项目开发自己的安全工具网关，实现自动化安全测试。

本项目是GPL 协议开源，欢迎大家 fork 和贡献。

HBC_SEC_MCP 是一个安全工具网关，将传统命令行安全工具包装为现代化的 MCP 服务。它实现了 MCP JSON-RPC 2.0 协议，让 AI 客户端能够以标准化的方式发现并调用安全测试能力。

思路参考：https://github.com/Wh0am123/MCP-Kali-Server

## 核心技术栈

- **Flask** - Web 服务框架，提供 HTTP API
- **MCP Protocol** - Model Context Protocol 协议实现
- **SQLMap** - 集成 SQL 注入检测工具
- **Python 3** - 主要开发语言

## 功能特性

### 已实现工具

| 工具名称 | 功能描述 | 调用方式 |
|---------|---------|---------|
| `sqlmap_scan` | SQL 注入自动检测 | MCP / HTTP API |
| `execute_command` | 通用命令执行 | MCP / HTTP API |

### API 端点

| 端点 | 方法 | 功能 |
|------|------|------|
| `/` | GET/POST | MCP 主入口 / 服务信息 |
| `/api/tools/sqlmap` | POST | 直接执行 SQLMap 扫描 |
| `/mcp/tools/HBC-Sec_mcp_tools/<tool>` | POST | 统一工具调用入口 |
| `/health` | GET | 健康检查 |
| `/mcp/capabilities` | GET | 服务能力发现 |

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动服务

```bash
# 默认启动
python server.py

# 指定端口和调试模式
python server.py --port 5000 --debug

# 绑定所有 IP
python server.py --ip 0.0.0.0 --port 8080
```

### API 调用示例

#### SQLMap 扫描

```bash
curl -X POST http://localhost:5000/api/tools/sqlmap \
  -H "Content-Type: application/json" \
  -d '{
    "url": "http://example.com/vuln.php?id=1",
    "data": "username=test&password=test",
    "additional_args": "--level=2 --risk=1"
  }'
```

#### 通用命令执行

```bash
curl -X POST http://localhost:5000/mcp/tools/HBC-Sec_mcp_tools/execute_command \
  -H "Content-Type: application/json" \
  -d '{
    "command": "nmap -sV 127.0.0.1"
  }'
```

#### MCP 协议调用

```bash
curl -X POST http://localhost:5000/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "sqlmap_scan",
      "arguments": {
        "url": "http://example.com/test.php?id=1"
      }
    }
  }'
```

## 项目结构

```
HBC_SEC_MCP/
├── server.py              # Flask 服务主入口
├── requirements.txt       # 项目依赖
├── .gitignore            # Git 忽略规则
├── README.md            # 项目说明文档
├── app/
│   ├── __init__.py
│   ├── config.py          # 配置常量
│   ├── mcp_protocol.py    # MCP 协议实现
│   ├── tool_dispatcher.py # 工具调度器
│   ├── command_executor.py # 命令执行封装
│   ├── logging_setup.py   # 日志配置
│   └── tools/
│       ├── __init__.py
│       ├── base_tool.py       # 工具基类
│       ├── sqlmap_tool.py     # SQLMap 集成
│       ├── command_exec_tool.py # 命令执行工具
│       └── _tool_template.py  # 新工具开发模板
└── log/                   # 运行日志目录
```

## 开发新工具

参考 `app/tools/_tool_template.py` 模板，继承 `BaseTool` 基类实现新工具：

```python
from typing import Any, Dict
from .base_tool import BaseTool

class MyNewTool(BaseTool):
    name = "my_new_tool"
    description = "描述工具功能"
    input_schema = {
        "type": "object",
        "properties": {
            "param1": {"type": "string"},
        },
        "required": ["param1"],
    }

    def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        # 实现工具逻辑
        return {"success": True, "result": "执行结果"}
```

## 配置说明

编辑 `app/config.py` 修改服务配置：

- `API_PORT` - 服务监听端口（默认：5000）
- `DEBUG_MODE` - 调试模式开关
- `TOOL_SQLMAP_SCAN` - SQLMap 工具名称常量

## 依赖要求

- Python 3.8+
- Flask >= 3.0.0
- requests >= 2.31.0
- mcp >= 1.0.0

## 使用场景

1. **AI 安全助手** - 让 AI 能够通过 MCP 协议调用安全工具
2. **自动化安全测试** - 集成到 CI/CD 流程
3. **安全工具编排** - 统一管理和调度多个安全工具

## 注意事项

- 生产环境建议使用 `--ip 127.0.0.1` 限制本地访问。
- 命令执行工具存在安全风险，请谨慎使用。
- 确保系统中已安装 sqlmap 命令行工具。

## 开源协议

本项目仅供学习研究使用，请遵守相关法律法规。
