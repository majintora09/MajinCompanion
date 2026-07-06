from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
GOAL_FILE = ROOT / "data" / "global" / "today_goal.md"


def save_today_goal(text: str):
    GOAL_FILE.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    GOAL_FILE.write_text(
        f"# Today's Goal\n\nSaved: {timestamp}\n\n{text.strip()}\n",
        encoding="utf-8",
    )


def get_today_goal():
    if not GOAL_FILE.exists():
        return None

    lines = GOAL_FILE.read_text(encoding="utf-8").splitlines()
    if len(lines) >= 5:
        return lines[4]
    return None
