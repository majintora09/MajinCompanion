from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
BRAINS_ROOT = ROOT / "project_brains"


def brain_path(place_id: str):
    return BRAINS_ROOT / place_id


def ensure_place_brain(place):
    folder = brain_path(place["id"])
    folder.mkdir(parents=True, exist_ok=True)

    files = {
        "dreams.md": "# Dreams\n",
        "notes.md": "# Notes\n",
        "activity.md": "# Activity\n",
        "sessions.json": "[]",
        "links.json": "[]",
        "metadata.json": json.dumps(
            {
                "id": place["id"],
                "name": place["name"],
                "display": place["display"],
                "priority": place["priority"],
                "momentum": place["momentum"],
                "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            },
            indent=2,
        ),
    }

    for filename, default in files.items():
        path = folder / filename
        if not path.exists():
            path.write_text(default, encoding="utf-8")


def ensure_all_brains(places):
    for place in places:
        ensure_place_brain(place)


def load_json(path, fallback):
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def save_place_session(place_id: str, session: dict):
    folder = brain_path(place_id)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "sessions.json"
    sessions = load_json(path, [])
    sessions.append(session)
    path.write_text(json.dumps(sessions, indent=2), encoding="utf-8")


def get_place_sessions(place_id: str, limit=5):
    path = brain_path(place_id) / "sessions.json"
    sessions = load_json(path, [])
    return list(reversed(sessions[-limit:]))


def append_place_activity(place_id: str, text: str):
    path = brain_path(place_id) / "activity.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        file.write(f"\n- {text}")


def read_text(place_id: str, filename: str, fallback=""):
    path = brain_path(place_id) / filename
    if not path.exists():
        return fallback
    return path.read_text(encoding="utf-8")


def append_text(place_id: str, filename: str, text: str):
    path = brain_path(place_id) / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        file.write(text)
