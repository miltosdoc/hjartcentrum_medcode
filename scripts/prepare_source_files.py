#!/usr/bin/env python3
"""
Prepare source PDFs for MedCode by ingesting all files from HC_Ledningssystem and HC_Webbportal.
- Copies PDFs directly
- Extracts text from DOCX/XLSX/MD/TXT and renders simple PDFs
"""

import os
import re
import shutil
from pathlib import Path
from typing import Iterable

import pandas as pd
from docx import Document
from markdown import markdown
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

SOURCE_DIRS = [
    Path("/Users/meditalks/Desktop/Code/HC/HC_Ledningssystem"),
    Path("/Users/meditalks/Desktop/Code/HC/HC_Webbportal"),
]
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "source_pdfs"

SUPPORTED_TEXT_EXT = {".docx", ".xlsx", ".xls", ".md", ".txt"}


def safe_name(path: Path) -> str:
    rel = "_".join(path.parts[-4:])
    rel = re.sub(r"[^a-zA-Z0-9_\-\.]+", "_", rel)
    return rel[:180]


def render_text_to_pdf(text: str, output_pdf: Path) -> None:
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(output_pdf), pagesize=A4)
    width, height = A4
    x, y = 40, height - 40
    line_height = 14
    for line in text.splitlines():
        if y < 50:
            c.showPage()
            y = height - 40
        c.drawString(x, y, line[:200])
        y -= line_height
    c.save()


def extract_docx(path: Path) -> str:
    doc = Document(str(path))
    return "\n".join(p.text for p in doc.paragraphs if p.text)


def extract_xlsx(path: Path) -> str:
    try:
        xls = pd.ExcelFile(path)
        parts = []
        for sheet in xls.sheet_names:
            df = xls.parse(sheet)
            parts.append(f"# Sheet: {sheet}\n{df.to_csv(index=False)}")
        return "\n\n".join(parts)
    except Exception:
        return ""


def extract_md(path: Path) -> str:
    html = markdown(path.read_text(encoding="utf-8", errors="ignore"))
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text("\n")


def extract_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def iter_files(base: Path) -> Iterable[Path]:
    for p in base.rglob("*"):
        if p.is_file() and not p.name.startswith("~"):
            yield p


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    copied, rendered = 0, 0

    for base in SOURCE_DIRS:
        if not base.exists():
            print(f"Skipping missing source: {base}")
            continue
        for path in iter_files(base):
            ext = path.suffix.lower()
            if ext == ".pdf":
                out = OUTPUT_DIR / f"{safe_name(path)}.pdf"
                shutil.copy2(path, out)
                copied += 1
                continue
            if ext in SUPPORTED_TEXT_EXT:
                if ext == ".docx":
                    text = extract_docx(path)
                elif ext in {".xlsx", ".xls"}:
                    text = extract_xlsx(path)
                elif ext == ".md":
                    text = extract_md(path)
                else:
                    text = extract_txt(path)
                if text.strip():
                    out = OUTPUT_DIR / f"{safe_name(path)}.pdf"
                    render_text_to_pdf(text, out)
                    rendered += 1

    print(f"Prepared PDFs: copied={copied}, rendered={rendered}, output={OUTPUT_DIR}")


if __name__ == "__main__":
    main()
