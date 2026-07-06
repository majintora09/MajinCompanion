from pathlib import Path
import json

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
    }

    for filename, default in files.items():
        path = folder / filename
        if not path.exists():
            path.write_text(default, encoding="utf-8")


def ensure_all_project_brains(projects):
    for project in projects:
        ensure_project_brain(project)


def save_project_session(project_id: str, session: dict):
    folder = brain_path(project_id)
    folder.mkdir(parents=True, exist_ok=True)

    path = folder / "sessions.json"

    if path.exists():
        try:
            sessions = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            sessions = []
    else:
        sessions = []

    sessions.append(session)

    path.write_text(json.dumps(sessions, indent=2), encoding="utf-8")


def append_project_activity(project_id: str, text: str):
    path = brain_path(project_id) / "activity.md"
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("a", encoding="utf-8") as file:
        file.write(f"\n- {text}")