# Hjärtcentrum Halland HC MCP Server

Local clinical knowledge MCP for Hjärtcentrum Halland (HC_Ledningssystem + HC_Webbportal). Indexes all files and provides search + document recall.

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/miltosdoc/hjartcentrum_medcode
cd hjartcentrum_medcode

# Install dependencies
python3 -m pip install -r requirements.txt
```

### Configuration

1. Build index from HC folders:
```bash
bash scripts/build_index.sh
```

2. Start MCP server:
```bash
python mcp_server/server.py
```

## 📋 Available Functions

### `search_knowledge`
Search across Hjärtcentrum Halland sources (Ledningssystem + Webbportal).

**Parameters:**
- `query` (string, required): Clinical question or topic
- `max_results` (int, optional): Maximum results (default: 5)

**Example:**
```json
{
  "method": "search_knowledge",
  "params": {
    "query": "patient med bröstsmärta undersökning",
    "max_results": 5
  }
}
```

### `get_document`
Retrieve a document by path returned from search.

**Parameters:**
- `path` (string, required): Absolute path from search result

**Example:**
```json
{
  "method": "get_document",
  "params": {
    "path": "/Users/meditalks/Desktop/Code/HC/HC_Ledningssystem/.../document.pdf"
  }
}
```

## 🏥‍⚕️ Clinical Use Cases

### Patient Safety & Lex Maria
```json
{
  "method": "search_knowledge",
  "params": {
    "query": "Lex Maria anmälan vårdskada"
  }
}
```

### Cardiac Examination Procedures
```json
{
  "method": "search_knowledge", 
  "params": {
    "query": "EKGundersökning rutin"
  }
}
```

### Equipment Maintenance
```json
{
  "method": "search_knowledge",
  "params": {
    "query": "medicinteknisk utrustning service"
  }
}
```

### FR2000 Quality Management
```json
{
  "method": "search_knowledge",
  "params": {
    "query": "kvalitetsledning internrevision"
  }
}
```

## 🔧 Maintenance

### Update Documents
```bash
# Run document update script
./scripts/update_docs.sh
```

### Notes
- The knowledge index is local and rebuildable.
- If files are locked, sync/copy them to a local folder first.

## 📜 License

- **License:** MIT
- **Repository:** https://github.com/miltosdoc/hjartcentrum_medcode
