from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_BASE_DIR = BASE_DIR / "log"
LOG_BASE_DIR.mkdir(parents=True, exist_ok=True)

LOG_FORMAT = (
    "%(asctime)s [%(levelname)s] [%(name)s] [%(module)s:%(funcName)s:%(lineno)d] "
    "[pid=%(process)d tid=%(threadName)s] %(message)s"
)

API_PORT = int(os.environ.get("API_PORT", 5000))
DEBUG_MODE = os.environ.get("DEBUG_MODE", "0").lower() in ("1", "true", "yes", "y")
COMMAND_TIMEOUT = 180
MCP_PROTOCOL_VERSION = "2024-11-05"
TOOL_SQLMAP_SCAN = "sqlmap_scan"

SIYUAN_BASE_URL = os.environ.get("SIYUAN_BASE_URL", "http://127.0.0.1:6806")
# 思源笔记的API Token
SIYUAN_API_TOKEN = os.environ.get("SIYUAN_API_TOKEN", "")
SIYUAN_TIMEOUT = int(os.environ.get("SIYUAN_TIMEOUT", 30))