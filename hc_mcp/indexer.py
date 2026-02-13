import os
import re
import sqlite3
from pathlib import Path
from typing import Iterable, List, Tuple

import pandas as pd
from docx import Document
from markdown import markdown
from bs4 import BeautifulSoup
from pypdf import PdfReader

SUPPORTED_EXT = {".pdf", ".docx", ".xlsx", ".xls", ".md", ".txt"}


def iter_files(paths: List[Path]) -> Iterable[Path]:
    for base in paths:
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.is_file() and p.suffix.lower() in SUPPORTED_EXT and not p.name.startswith("~"):
                yield p


def read_pdf(path: Path) -> str:
    try:
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception:
        return ""


def read_docx(path: Path) -> str:
    try:
        doc = Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs if p.text)
    except Exception:
        return ""


def read_xlsx(path: Path) -> str:
    try:
        xls = pd.ExcelFile(path)
        parts = []
        for sheet in xls.sheet_names:
            df = xls.parse(sheet)
            parts.append(f"# Sheet: {sheet}\n{df.to_csv(index=False)}")
        return "\n\n".join(parts)
    except Exception:
        return ""


def safe_read_text(path: Path, attempts: int = 3) -> str:
    for _ in range(attempts):
        try:
            return path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
    return ""


def read_md(path: Path) -> str:
    html = markdown(safe_read_text(path))
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text("\n")


def read_txt(path: Path) -> str:
    return safe_read_text(path)


def normalize(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text


def read_file(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".pdf":
        return read_pdf(path)
    if ext == ".docx":
        return read_docx(path)
    if ext in {".xlsx", ".xls"}:
        return read_xlsx(path)
    if ext == ".md":
        return read_md(path)
    if ext == ".txt":
        return read_txt(path)
    return ""


def init_db(db_path: Path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("PRAGMA journal_mode=WAL;")
    c.execute(
        "CREATE VIRTUAL TABLE IF NOT EXISTS docs USING fts5(path, title, content, tokenize='unicode61')"
    )
    conn.commit()
    return conn


def index_docs(source_paths: List[Path], db_path: Path) -> Tuple[int, int]:
    conn = init_db(db_path)
    c = conn.cursor()
    # reset index
    c.execute("DELETE FROM docs")
    conn.commit()

    indexed = 0
    skipped = 0
    for path in iter_files(source_paths):
        text = normalize(read_file(path))
        if not text:
            skipped += 1
            continue
        title = path.stem
        c.execute("INSERT INTO docs(path, title, content) VALUES (?, ?, ?)", (str(path), title, text))
        indexed += 1
    conn.commit()
    conn.close()
    return indexed, skipped


def search(db_path: Path, query: str, max_results: int = 5) -> List[dict]:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        "SELECT path, title, snippet(docs, 2, '<b>', '</b>', '…', 12) AS snippet, bm25(docs) as score "
        "FROM docs WHERE docs MATCH ? ORDER BY score LIMIT ?",
        (query, max_results),
    )
    rows = c.fetchall()
    conn.close()
    return [
        {"path": r[0], "title": r[1], "snippet": r[2], "score": r[3]} for r in rows
    ]


def get_doc(db_path: Path, path: str) -> dict:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT path, title, content FROM docs WHERE path = ?", (path,))
    row = c.fetchone()
    conn.close()
    if not row:
        return {}
    return {"path": row[0], "title": row[1], "content": row[2]}
