#!/usr/bin/env bash
set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DB_PATH="$PROJECT_ROOT/hc_mcp/hc_knowledge.db"

python3 -m hc_mcp.cli \
  --db "$DB_PATH" \
  --src /Users/meditalks/Desktop/HC_local/HC_Ledningssystem \
  --src /Users/meditalks/Desktop/HC_local/HC_Webbportal

echo "Index built at $DB_PATH"
