#!/usr/bin/env python3
"""
MCP Server for Hjärtcentrum Halland HC MCP
Local indexer + search + recall
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict

sys.path.append(str(Path(__file__).parent.parent))

from hc_mcp.indexer import search, get_doc

DB_PATH = Path(__file__).parent.parent / "hc_mcp" / "hc_knowledge.db"


class HjartcentrumMCPServer:
    def __init__(self):
        pass

    def search_knowledge(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        try:
            results = search(DB_PATH, query=query, max_results=max_results)
            return {"success": True, "data": results}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_document(self, path: str) -> Dict[str, Any]:
        try:
            doc = get_doc(DB_PATH, path=path)
            if not doc:
                return {"success": False, "error": "Not found"}
            return {"success": True, "data": doc}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        method = request.get("method")
        params = request.get("params", {})

        if method == "search_knowledge":
            return self.search_knowledge(
                query=params.get("query", ""),
                max_results=params.get("max_results", 5),
            )
        elif method == "get_document":
            return self.get_document(path=params.get("path", ""))
        else:
            return {"success": False, "error": f"Unknown method: {method}"}


def main():
    server = HjartcentrumMCPServer()
    try:
        request = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        print(json.dumps({"success": False, "error": "Invalid JSON request"}))
        return

    response = server.handle_request(request)
    print(json.dumps(response, ensure_ascii=False))


if __name__ == "__main__":
    main()
