from __future__ import annotations

from typing import Any, Dict, List

from ..siyuan_client import SiYuanClient
from .base_tool import BaseTool


_TOOL_SPECS: List[Dict[str, Any]] = [
    # Notebook
    {
        "name": "list_notebooks",
        "description": "列出工作空间中的所有笔记本",
        "api_path": "/api/notebook/lsNotebooks",
        "properties": {},
        "required": [],
    },
    {
        "name": "create_notebook",
        "description": "创建新笔记本",
        "api_path": "/api/notebook/createNotebook",
        "properties": {"name": {"type": "string"}},
        "required": ["name"],
    },
    {
        "name": "open_notebook",
        "description": "打开笔记本",
        "api_path": "/api/notebook/openNotebook",
        "properties": {"notebook": {"type": "string"}},
        "required": ["notebook"],
    },
    {
        "name": "close_notebook",
        "description": "关闭笔记本",
        "api_path": "/api/notebook/closeNotebook",
        "properties": {"notebook": {"type": "string"}},
        "required": ["notebook"],
    },
    {
        "name": "remove_notebook",
        "description": "删除笔记本",
        "api_path": "/api/notebook/removeNotebook",
        "properties": {"notebook": {"type": "string"}},
        "required": ["notebook"],
    },
    {
        "name": "rename_notebook",
        "description": "重命名笔记本",
        "api_path": "/api/notebook/renameNotebook",
        "properties": {
            "notebook": {"type": "string"},
            "name": {"type": "string"},
        },
        "required": ["notebook", "name"],
    },
    {
        "name": "get_notebook_conf",
        "description": "获取笔记本配置",
        "api_path": "/api/notebook/getNotebookConf",
        "properties": {"notebook": {"type": "string"}},
        "required": ["notebook"],
    },
    {
        "name": "set_notebook_conf",
        "description": "设置笔记本配置",
        "api_path": "/api/notebook/setNotebookConf",
        "properties": {
            "notebook": {"type": "string"},
            "conf": {"type": "object"},
        },
        "required": ["notebook", "conf"],
    },
    # Document
    {
        "name": "create_document",
        "description": "创建带 Markdown 内容的新文档",
        "api_path": "/api/filetree/createDocWithMd",
        "properties": {
            "notebook": {"type": "string"},
            "path": {"type": "string"},
            "markdown": {"type": "string"},
        },
        "required": ["notebook", "path", "markdown"],
    },
    {
        "name": "rename_document",
        "description": "通过路径重命名文档",
        "api_path": "/api/filetree/renameDoc",
        "properties": {
            "notebook": {"type": "string"},
            "path": {"type": "string"},
            "title": {"type": "string"},
        },
        "required": ["notebook", "path", "title"],
    },
    {
        "name": "rename_document_by_id",
        "description": "通过 ID 重命名文档",
        "api_path": "/api/filetree/renameDocByID",
        "properties": {
            "id": {"type": "string"},
            "title": {"type": "string"},
        },
        "required": ["id", "title"],
    },
    {
        "name": "remove_document",
        "description": "通过路径删除文档",
        "api_path": "/api/filetree/removeDoc",
        "properties": {
            "notebook": {"type": "string"},
            "path": {"type": "string"},
        },
        "required": ["notebook", "path"],
    },
    {
        "name": "remove_document_by_id",
        "description": "通过 ID 删除文档",
        "api_path": "/api/filetree/removeDocByID",
        "properties": {"id": {"type": "string"}},
        "required": ["id"],
    },
    {
        "name": "move_documents",
        "description": "移动多个文档到新位置",
        "api_path": "/api/filetree/moveDocs",
        "properties": {
            "fromPaths": {"type": "array", "items": {"type": "string"}},
            "toNotebook": {"type": "string"},
            "toPath": {"type": "string"},
        },
        "required": ["fromPaths", "toNotebook", "toPath"],
    },
    {
        "name": "move_documents_by_id",
        "description": "通过 ID 移动多个文档",
        "api_path": "/api/filetree/moveDocsByID",
        "properties": {
            "fromIDs": {"type": "array", "items": {"type": "string"}},
            "toNotebook": {"type": "string"},
            "toPath": {"type": "string"},
        },
        "required": ["fromIDs", "toNotebook", "toPath"],
    },
    {
        "name": "get_document_path",
        "description": "通过文档 ID 获取文件路径",
        "api_path": "/api/filetree/getDocPath",
        "properties": {"id": {"type": "string"}},
        "required": ["id"],
    },
    {
        "name": "get_hpath_by_path",
        "description": "通过文件路径获取层级路径",
        "api_path": "/api/filetree/getHPathByPath",
        "properties": {
            "notebook": {"type": "string"},
            "path": {"type": "string"},
        },
        "required": ["notebook", "path"],
    },
    {
        "name": "get_hpath_by_id",
        "description": "通过文档 ID 获取层级路径",
        "api_path": "/api/filetree/getHPathByID",
        "properties": {"id": {"type": "string"}},
        "required": ["id"],
    },
    {
        "name": "get_ids_by_hpath",
        "description": "通过层级路径获取文档 ID",
        "api_path": "/api/filetree/getIDsByHPath",
        "properties": {
            "notebook": {"type": "string"},
            "path": {"type": "string"},
        },
        "required": ["notebook", "path"],
    },
    # Block
    {
        "name": "insert_block",
        "description": "在指定位置插入新块",
        "api_path": "/api/block/insertBlock",
        "properties": {
            "dataType": {"type": "string"},
            "data": {"type": "string"},
            "nextID": {"type": "string"},
            "previousID": {"type": "string"},
            "parentID": {"type": "string"},
        },
        "required": ["dataType", "data"],
    },
    {
        "name": "prepend_block",
        "description": "在父块开头插入块",
        "api_path": "/api/block/prependBlock",
        "properties": {
            "dataType": {"type": "string"},
            "data": {"type": "string"},
            "parentID": {"type": "string"},
        },
        "required": ["dataType", "data", "parentID"],
    },
    {
        "name": "append_block",
        "description": "在父块末尾插入块",
        "api_path": "/api/block/appendBlock",
        "properties": {
            "dataType": {"type": "string"},
            "data": {"type": "string"},
            "parentID": {"type": "string"},
        },
        "required": ["dataType", "data", "parentID"],
    },
    {
        "name": "update_block",
        "description": "更新块内容",
        "api_path": "/api/block/updateBlock",
        "properties": {
            "id": {"type": "string"},
            "dataType": {"type": "string"},
            "data": {"type": "string"},
        },
        "required": ["id", "dataType", "data"],
    },
    {
        "name": "delete_block",
        "description": "删除块",
        "api_path": "/api/block/deleteBlock",
        "properties": {"id": {"type": "string"}},
        "required": ["id"],
    },
    {
        "name": "move_block",
        "description": "移动块到新位置",
        "api_path": "/api/block/moveBlock",
        "properties": {
            "id": {"type": "string"},
            "parentID": {"type": "string"},
            "previousID": {"type": "string"},
        },
        "required": ["id"],
    },
    {
        "name": "fold_block",
        "description": "折叠块（收起子块）",
        "api_path": "/api/block/foldBlock",
        "properties": {"id": {"type": "string"}},
        "required": ["id"],
    },
    {
        "name": "unfold_block",
        "description": "展开块（显示子块）",
        "api_path": "/api/block/unfoldBlock",
        "properties": {"id": {"type": "string"}},
        "required": ["id"],
    },
    {
        "name": "get_block_kramdown",
        "description": "获取块的 kramdown 格式内容",
        "api_path": "/api/block/getBlockKramdown",
        "properties": {"id": {"type": "string"}},
        "required": ["id"],
    },
    {
        "name": "get_child_blocks",
        "description": "获取父块的所有子块",
        "api_path": "/api/block/getChildBlocks",
        "properties": {"id": {"type": "string"}},
        "required": ["id"],
    },
    {
        "name": "transfer_block_ref",
        "description": "转移块引用",
        "api_path": "/api/block/transferBlockRef",
        "properties": {
            "id": {"type": "string"},
            "fromID": {"type": "string"},
            "toID": {"type": "string"},
        },
        "required": ["id", "fromID", "toID"],
    },
    {
        "name": "set_block_attrs",
        "description": "设置块属性",
        "api_path": "/api/attr/setBlockAttrs",
        "properties": {
            "id": {"type": "string"},
            "attrs": {"type": "object"},
        },
        "required": ["id", "attrs"],
    },
    {
        "name": "get_block_attrs",
        "description": "获取块属性",
        "api_path": "/api/attr/getBlockAttrs",
        "properties": {"id": {"type": "string"}},
        "required": ["id"],
    },
    # File / utility
    {
        "name": "upload_asset",
        "description": "上传文件到资源目录",
        "api_path": "/api/asset/upload",
        "properties": {
            "file_path": {"type": "string", "description": "本地文件路径"},
            "file_name": {"type": "string", "description": "使用 base64 上传时的文件名"},
            "content_base64": {
                "type": "string",
                "description": "使用 base64 上传时的文件内容",
            },
            "assets_dir_path": {"type": "string", "description": "思源资源目录子路径"},
        },
        "required": [],
    },
    {
        "name": "render_template",
        "description": "使用文档上下文渲染模板",
        "api_path": "/api/template/render",
        "properties": {
            "id": {"type": "string"},
            "path": {"type": "string"},
        },
        "required": ["id", "path"],
    },
    {
        "name": "render_sprig",
        "description": "渲染 Sprig 模板",
        "api_path": "/api/template/renderSprig",
        "properties": {"template": {"type": "string"}},
        "required": ["template"],
    },
    {
        "name": "export_md_content",
        "description": "导出文档为 Markdown",
        "api_path": "/api/export/exportMdContent",
        "properties": {"id": {"type": "string"}},
        "required": ["id"],
    },
    {
        "name": "export_resources",
        "description": "导出资源为 ZIP",
        "api_path": "/api/export/exportResources",
        "properties": {
            "paths": {"type": "array", "items": {"type": "string"}},
            "name": {"type": "string"},
        },
        "required": ["paths", "name"],
    },
    {
        "name": "push_msg",
        "description": "推送通知消息",
        "api_path": "/api/notification/pushMsg",
        "properties": {
            "msg": {"type": "string"},
            "timeout": {"type": "integer"},
        },
        "required": ["msg"],
    },
    {
        "name": "push_err_msg",
        "description": "推送错误消息",
        "api_path": "/api/notification/pushErrMsg",
        "properties": {
            "msg": {"type": "string"},
            "timeout": {"type": "integer"},
        },
        "required": ["msg"],
    },
    {
        "name": "get_version",
        "description": "获取思源版本",
        "api_path": "/api/system/version",
        "properties": {},
        "required": [],
    },
    {
        "name": "get_current_time",
        "description": "获取当前系统时间",
        "api_path": "/api/system/currentTime",
        "properties": {},
        "required": [],
    },
]


def _missing_required(params: Dict[str, Any], required: List[str]) -> List[str]:
    missing: List[str] = []
    for key in required:
        value = params.get(key)
        if value is None:
            missing.append(key)
            continue
        if isinstance(value, str) and not value.strip():
            missing.append(key)
    return missing


class _SiYuanBaseTool(BaseTool):
    api_path: str = ""
    required_fields: List[str] = []

    def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        params = params or {}
        missing = _missing_required(params, self.required_fields)
        if missing:
            return {
                "success": False,
                "error": f"missing required params: {', '.join(missing)}",
            }

        client = SiYuanClient()
        if self.name == "upload_asset":
            return client.upload_asset(params)
        return client.call(self.api_path, params)


for spec in _TOOL_SPECS:
    class_name = "SiYuan" + "".join(part.title() for part in spec["name"].split("_")) + "Tool"
    globals()[class_name] = type(
        class_name,
        (_SiYuanBaseTool,),
        {
            "__module__": __name__,
            "name": spec["name"],
            "description": spec["description"],
            "api_path": spec["api_path"],
            "required_fields": list(spec["required"]),
            "input_schema": {
                "type": "object",
                "properties": dict(spec["properties"]),
                "required": list(spec["required"]),
                "additionalProperties": True,
            },
        },
    )
