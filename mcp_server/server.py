#!/usr/bin/env python3
"""
MCP Server for Hjärtcentrum Halland MedCode
Clinical Decision Support System
"""

import json
import sys
from typing import Any, Dict, List, Optional
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    from medcode import medcode_search_knowledge, medcode_get_chapter, medcode_list_chapters
except ImportError:
    print("Error: MedCode not available. Please install dependencies.", file=sys.stderr)
    sys.exit(1)

class HjartcentrumMedCodeServer:
    def __init__(self):
        self.server_info = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        config_path = Path(__file__).parent / "config.json"
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def search_knowledge(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """Search across Hjärtcentrum Halland guidelines"""
        try:
            result = medcode_search_knowledge(query=query, max_results=str(max_results))
            return {
                "success": True,
                "data": result,
                "server": self.server_info["mcp"]["server"]["name"]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "server": self.server_info["mcp"]["server"]["name"]
            }
    
    def get_chapter(self, guideline_slug: str, chapter_title: str) -> Dict[str, Any]:
        """Retrieve specific document chapter"""
        try:
            result = medcode_get_chapter(guideline_slug=guideline_slug, chapter_title=chapter_title)
            return {
                "success": True,
                "data": result,
                "server": self.server_info["mcp"]["server"]["name"]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "server": self.server_info["mcp"]["server"]["name"]
            }
    
    def list_chapters(self, guideline_slug: str) -> Dict[str, Any]:
        """List all chapters in a document"""
        try:
            result = medcode_list_chapters(guideline_slug=guideline_slug)
            return {
                "success": True,
                "data": result,
                "server": self.server_info["mcp"]["server"]["name"]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "server": self.server_info["mcp"]["server"]["name"]
            }
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Main request handler"""
        method = request.get("method")
        params = request.get("params", {})
        
        if method == "search_knowledge":
            return self.search_knowledge(
                query=params.get("query", ""),
                max_results=params.get("max_results", 5)
            )
        elif method == "get_chapter":
            return self.get_chapter(
                guideline_slug=params.get("guideline_slug", ""),
                chapter_title=params.get("chapter_title", "")
            )
        elif method == "list_chapters":
            return self.list_chapters(
                guideline_slug=params.get("guideline_slug", "")
            )
        else:
            return {
                "success": False,
                "error": f"Unknown method: {method}",
                "server": self.server_info["mcp"]["server"]["name"]
            }

def main():
    """Main MCP server loop"""
    server = HjartcentrumMedCodeServer()
    
    # Read MCP request from stdin
    try:
        request = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        error_response = {
            "success": False,
            "error": "Invalid JSON request",
            "server": "hjartcentrum-medcode"
        }
        print(json.dumps(error_response))
        return
    
    # Process request
    response = server.handle_request(request)
    print(json.dumps(response, ensure_ascii=False))

if __name__ == "__main__":
    main()