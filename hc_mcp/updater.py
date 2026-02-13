import json
from pathlib import Path
from datetime import datetime

UPDATES_DIR = Path(__file__).parent.parent / "updates"
UPDATES_DIR.mkdir(parents=True, exist_ok=True)


def save_update(title: str, body: str, tags=None) -> dict:
    tags = tags or []
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    safe = "_".join(title.strip().split())[:80]
    path = UPDATES_DIR / f"{ts}__{safe}.md"
    content = "\n".join([
        f"# {title}",
        f"- timestamp: {ts} UTC",
        f"- tags: {', '.join(tags)}",
        "",
        body.strip(),
        ""
    ])
    path.write_text(content, encoding="utf-8")
    return {"path": str(path), "saved": True}
