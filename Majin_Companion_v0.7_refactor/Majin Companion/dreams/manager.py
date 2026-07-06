from pathlib import Path
from datetime import datetime

from activity.manager import log_activity

ROOT = Path(__file__).resolve().parents[1]
DREAM_FILE = ROOT / "data" / "global" / "dreams.md"


def save_dream(text: str):
    DREAM_FILE.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with DREAM_FILE.open("a", encoding="utf-8") as file:
        file.write(f"\n## {timestamp}\n{text.strip()}\n")
    log_activity("🧠 Saved Dream")
    return True


def count_dreams():
    if not DREAM_FILE.exists():
        return 0
    return DREAM_FILE.read_text(encoding="utf-8").count("## ")


def get_latest_dream():
    if not DREAM_FILE.exists():
        return None
    blocks = [b.strip() for b in DREAM_FILE.read_text(encoding="utf-8").strip().split("## ") if b.strip()]
    if not blocks:
        return None
    lines = blocks[-1].splitlines()
    return lines[1] if len(lines) >= 2 else None
