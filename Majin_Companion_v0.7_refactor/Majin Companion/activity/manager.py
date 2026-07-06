from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
ACTIVITY_FILE = ROOT / "data" / "global" / "activity.md"


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def log_activity(text: str):
    ACTIVITY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with ACTIVITY_FILE.open("a", encoding="utf-8") as file:
        file.write(f"\n## {timestamp()}\n{text.strip()}\n")


def get_recent_activity(limit=5):
    if not ACTIVITY_FILE.exists():
        return ["🔥 Started Companion"]

    content = ACTIVITY_FILE.read_text(encoding="utf-8").strip()
    blocks = [b.strip() for b in content.split("## ") if b.strip()]
    recent = blocks[-limit:]

    results = []
    for block in reversed(recent):
        lines = block.splitlines()
        if len(lines) >= 2:
            results.append(lines[1])

    return results or ["🔥 Started Companion"]
