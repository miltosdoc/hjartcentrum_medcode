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

## 📚 Knowledge Base Coverage

**Total Guidelines:** 186  
**Total Chapters:** 1,458

### Key Sections:
- **01_Ledning** - Management & Leadership
- **02_Patientsakerhet** - Patient Safety 
- **03_Kvalitet** - Quality Management
- **04_Miljö** - Environmental Management
- **05_Arbetsmiljö** - Work Environment
- **06_Informationssäkerhet** - Information Security
- **07_Medicinteknik** - Medical Technology
- **08_Processkartor** - Process Maps
- **09_Avvikelse_Risk** - Deviation & Risk
- **10_Mål_Uppföljning** - Goals & Follow-up
- **11_Rapporter** - Reports
- **12_Leverantorer_Inköp** - Suppliers & Procurement
- **13_HR_Kompetens** - HR & Competence
- **14_Beredskap_Nödläge** - Emergency Preparedness
- **15_Dokumentstyrning** - Document Control
- **16_Marknad_Kommunikation** - Marketing & Communication

### Essential Documents:
- Handbook - Management System (HC-HB-001)
- Quality & Safety Policies (HC-POL-001 to HC-POL-009)
- Patient Flow Processes (HC-PROC-001)
- Clinical Routines (HC-RUT series)
- Medical Equipment Procedures (HC-RUT-071+)
- Emergency Protocols (HC-RUT-141+)
- Lex Maria Reporting (HC-RUT-007)
- Risk Management (HC-RISK-001)
- Environmental Aspects (HC-REG-041)

## 🔧 Maintenance

### Update Documents
```bash
# Run document update script
./scripts/update_docs.sh

# This will:
# 1. Process new/changed PDFs
# 2. Update knowledge index
# 3. Validate search functionality
```

### Knowledge Base Status
```bash
# Check current knowledge base status
medcode get_knowledge_status
```

## 🐛 Troubleshooting

### Common Issues:

**No search results:**
- Check if documents are processed: `medcode get_knowledge_status`
- Verify PDF files are in `source_pdfs/`
- Re-process documents: `medcode process_documents`

**Import errors:**
- Install missing dependencies: `pip install -r requirements.txt`
- Verify MedCode installation: `pip show medcode`

**Performance issues:**
- Limit search results with `max_results` parameter
- Consider document categorization for faster searches
- Monitor system resources

## 📞 Support

For technical support or questions:

1. **Clinical Support:** Contact Hjärtcentrum Halland medical staff
2. **Technical Support:** Create issue in GitHub repository
3. **Documentation:** See `/docs/` directory for detailed guides

## 📜 License & Version

- **Version:** 1.0.0
- **License:** MIT
- **Repository:** https://github.com/miltosdoc/hjartcentrum_medcode
- **Last Updated:** 2025-01-15

---

*This MCP server transforms Hjärtcentrum Halland's comprehensive FR2000 management system into an AI-powered clinical decision support tool, enabling healthcare professionals to instantly access evidence-based guidelines, procedures, and regulatory requirements.*