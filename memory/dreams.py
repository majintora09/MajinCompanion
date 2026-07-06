from pathlib import Path
from datetime import datetime

from memory.activity import log_activity
from memory.sessions import get_active_session
from projects.brains import append_project_dream, append_project_activity

ROOT = Path(__file__).resolve().parents[1]
DREAM_FILE = ROOT / "memory" / "dreams.md"


def save_dream(text: str):
    DREAM_FILE.parent.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    with DREAM_FILE.open("a", encoding="utf-8") as file:
        file.write(f"\n## {timestamp}\n{text.strip()}\n")

    session = get_active_session()

    if session:
        project_id = session["project_id"]
        append_project_dream(project_id, text)
        append_project_activity(project_id, f"🧠 Dream saved: {text.strip()}")

    log_activity("🧠 Saved Dream")
    return True


def count_dreams():
    if not DREAM_FILE.exists():
        return 0

    content = DREAM_FILE.read_text(encoding="utf-8")
    return content.count("## ")


def get_latest_dream():
    if not DREAM_FILE.exists():
        return None

    content = DREAM_FILE.read_text(encoding="utf-8").strip()
    blocks = [b.strip() for b in content.split("## ") if b.strip()]

    if not blocks:
        return None

    latest = blocks[-1]
    lines = latest.splitlines()

    if len(lines) >= 2:
        return lines[1]

    return None