#!/bin/bash
# Update documents for Hjärtcentrum Halland MedCode MCP Server
# This script processes new/changed documents and updates the knowledge base

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🔄 Hjärtcentrum Halland - Document Update Process"
echo "=================================================="

# Check dependencies
if ! command -v medcode &> /dev/null; then
    echo "❌ ERROR: MedCode not installed. Run: pip install medcode"
    exit 1
fi

# Function to process documents
process_documents() {
    echo "📚 Processing documents in source_pdfs/..."
    cd "$PROJECT_ROOT"
    
    # Process all PDFs
    medcode process_documents
    
    if [ $? -eq 0 ]; then
        echo "✅ Documents processed successfully"
    else
        echo "❌ ERROR: Document processing failed"
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
    
    # Check if source directory has PDFs
    if [ ! -d "$PROJECT_ROOT/source_pdfs" ]; then
        echo "❌ ERROR: source_pdfs directory not found"
        exit 1
    fi
    
    pdf_count=$(find "$PROJECT_ROOT/source_pdfs" -name "*.pdf" | wc -l | tr -d ' ')
    echo "  Found $pdf_count PDF documents"
    
    if [ "$pdf_count" -eq 0 ]; then
        echo "❌ ERROR: No PDF files found in source_pdfs/"
        exit 1
    fi
    
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