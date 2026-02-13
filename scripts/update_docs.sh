#!/bin/bash
# Update documents for Hjärtcentrum Halland MedCode MCP Server
# This script processes new/changed documents and updates the knowledge base

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🔄 Hjärtcentrum Halland - Document Update Process"
echo "=================================================="

# Check dependencies
if ! python3 -c "import hc_mcp" &> /dev/null; then
    echo "❌ ERROR: hc_mcp not available. Run: python3 -m pip install -r requirements.txt"
    exit 1
fi

# Function to process documents
process_documents() {
    echo "📚 Building index from HC folders..."
    cd "$PROJECT_ROOT"
    bash "$PROJECT_ROOT/scripts/build_index.sh"
    if [ $? -eq 0 ]; then
        echo "✅ Index built successfully"
    else
        echo "❌ ERROR: Index build failed"
        exit 1
    fi
}

# Function to validate search functionality
validate_search() {
    echo "🔍 Validating search functionality..."

    # Test Swedish clinical queries
    test_queries=(
        "Lex Maria anmälan vårdskada"
        "patient med bröstsmärta undersökning"
        "EKG rutin"
        "medicinteknisk utrustning"
        "kvalitetsledning"
    )

    for query in "${test_queries[@]}"; do
        echo "  Testing: $query"
        result=$(medcode search_knowledge "$query" 2>/dev/null)

        if [ $? -eq 0 ]; then
            echo "  ✅ Search working"
        else
            echo "  ❌ Search failed for: $query"
            return 1
        fi
    done

    echo "✅ Search validation complete"
}

# Function to show knowledge base status
show_status() {
    echo "📊 Knowledge Base Status:"
    echo "--------------------------"
    medcode get_knowledge_status
    echo ""
}

# Function to create backup
create_backup() {
    echo "💾 Creating backup..."
    backup_dir="$PROJECT_ROOT/backups/$(date +%Y%m%d_%H%M%S)"

    mkdir -p "$backup_dir"
    cp -r "$PROJECT_ROOT/medcode/knowledge" "$backup_dir/" 2>/dev/null || true

    echo "  Backup created: $backup_dir"
}

# Main execution
main() {
    echo "Starting document update process..."

    # Create backup
    create_backup

    # Process documents
    process_documents

    # Validate functionality
    validate_search

    # Show status
    show_status

    echo ""
    echo "🎉 Update complete!"
    echo "   Knowledge base ready for clinical use"
    echo "   MCP server can be started with: python mcp_server/server.py"
}

# Execute main function
main "$@"