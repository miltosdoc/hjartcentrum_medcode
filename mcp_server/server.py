#!/usr/bin/env python3
"""
MCP Server for Hjärtcentrum Halland HC MCP (stdio JSON-RPC)
"""
import json
import sys
from pathlib import Path
from typing import Any, Dict

sys.path.append(str(Path(__file__).parent.parent))

from hc_mcp.indexer import search, get_doc

DB_PATH = Path(__file__).parent.parent / "hc_mcp" / "hc_knowledge.db"


def rpc_result(_id, result):
    return json.dumps({"jsonrpc": "2.0", "id": _id, "result": result}, ensure_ascii=False)


def rpc_error(_id, code, message):
    return json.dumps({"jsonrpc": "2.0", "id": _id, "error": {"code": code, "message": message}}, ensure_ascii=False)


def handle_initialize(params: Dict[str, Any]):
    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {"tools": {}},
        "serverInfo": {"name": "hjartcentrum-hc", "version": "1.0.0"},
    }


def handle_tools_list():
    return {
        "tools": [
            {
                "name": "search_knowledge",
                "description": "Search across Hjärtcentrum Halland sources (Ledningssystem + Webbportal)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "max_results": {"type": "integer", "default": 5},
                    },
                    "required": ["query"],
                },
            },
            {
                "name": "get_document",
                "description": "Retrieve a document by path returned from search",
                "inputSchema": {
                    "type": "object",
                    "properties": {"path": {"type": "string"}},
                    "required": ["path"],
                },
            },
        ]
    }


def handle_tools_call(params: Dict[str, Any]):
    name = params.get("name")
    args = params.get("arguments", {})
    if name == "search_knowledge":
        query = args.get("query", "")
        max_results = int(args.get("max_results", 5))
        data = search(DB_PATH, query=query, max_results=max_results)
        return {"content": [{"type": "text", "text": json.dumps(data, ensure_ascii=False)}]}
    if name == "get_document":
        path = args.get("path", "")
        data = get_doc(DB_PATH, path=path)
        return {"content": [{"type": "text", "text": json.dumps(data, ensure_ascii=False)}]}
    raise ValueError(f"Unknown tool: {name}")


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue
        _id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        try:
            if method == "initialize":
                res = handle_initialize(params)
                sys.stdout.write(rpc_result(_id, res) + "\n")
            elif method == "tools/list":
                res = handle_tools_list()
                sys.stdout.write(rpc_result(_id, res) + "\n")
            elif method == "tools/call":
                res = handle_tools_call(params)
                sys.stdout.write(rpc_result(_id, res) + "\n")
            else:
                sys.stdout.write(rpc_error(_id, -32601, "Method not found") + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(rpc_error(_id, -32000, str(e)) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
