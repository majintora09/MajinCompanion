from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
BRAINS_ROOT = ROOT / "project_brains"


def brain_path(project_id: str):
    return BRAINS_ROOT / project_id


def ensure_project_brain(project):
    folder = brain_path(project["id"])
    folder.mkdir(parents=True, exist_ok=True)

    files = {
        "dreams.md": "# Dreams\n",
        "notes.md": "# Notes\n",
        "activity.md": "# Activity\n",
        "sessions.json": "[]",
        "metadata.json": "{}",
    }

    for filename, default in files.items():
        path = folder / filename
        if not path.exists():
            path.write_text(default, encoding="utf-8")


def ensure_all_project_brains(projects):
    for project in projects:
        ensure_project_brain(project)


def read_text_file(project_id: str, filename: str, fallback=""):
    path = brain_path(project_id) / filename

    if not path.exists():
        return fallback

    return path.read_text(encoding="utf-8")


def write_text_file(project_id: str, filename: str, content: str):
    path = brain_path(project_id) / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def load_json_file(project_id: str, filename: str, fallback):
    path = brain_path(project_id) / filename

    if not path.exists():
        return fallback

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def save_json_file(project_id: str, filename: str, data):
    path = brain_path(project_id) / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def save_project_session(project_id: str, session: dict):
    sessions = load_json_file(project_id, "sessions.json", [])
    sessions.append(session)
    save_json_file(project_id, "sessions.json", sessions)

    metadata = get_project_metadata(project_id)
    metadata["last_session"] = session
    metadata["total_sessions"] = len(sessions)
    metadata["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    save_json_file(project_id, "metadata.json", metadata)


def append_project_activity(project_id: str, text: str):
    path = brain_path(project_id) / "activity.md"
    path.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    with path.open("a", encoding="utf-8") as file:
        file.write(f"\n## {timestamp}\n{text.strip()}\n")


def append_project_dream(project_id: str, text: str):
    path = brain_path(project_id) / "dreams.md"
    path.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    with path.open("a", encoding="utf-8") as file:
        file.write(f"\n## {timestamp}\n{text.strip()}\n")


def get_project_sessions(project_id: str, limit=5):
    sessions = load_json_file(project_id, "sessions.json", [])
    return list(reversed(sessions[-limit:]))


def get_project_metadata(project_id: str):
    return load_json_file(project_id, "metadata.json", {})


def get_project_stats(project_id: str):
    sessions = load_json_file(project_id, "sessions.json", [])
    dreams = read_text_file(project_id, "dreams.md", "")
    activity = read_text_file(project_id, "activity.md", "")

    return {
        "sessions": len(sessions),
        "dreams": dreams.count("## "),
        "activity_entries": activity.count("## "),
    }