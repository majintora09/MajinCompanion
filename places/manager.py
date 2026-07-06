import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "places" / "data"


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def place_folder(place_id: str):
    return DATA_ROOT / place_id


def brain_file(place_id: str):
    return place_folder(place_id) / "brain.json"


def default_brain(project: dict):
    return {
        "identity": {
            "id": project["id"],
            "name": project["name"],
            "nickname": project.get("nickname", project["name"]),
            "icon": project["icon"],
            "priority": project.get("priority", 99),
            "momentum": project.get("momentum", 0),
            "status": project.get("status", ""),
            "color": project.get("color", "green"),
        },
        "mission": "",
        "notes": "",
        "dreams": [],
        "discoveries": [],
        "history": [],
        "sessions": [],
        "links": {
            "folder": project.get("path"),
            "website": project.get("url"),
            "github": project.get("github"),
        },
        "metadata": {
            "created": now(),
            "last_updated": now(),
        },
    }


def ensure_brain(project: dict):
    folder = place_folder(project["id"])
    folder.mkdir(parents=True, exist_ok=True)

    path = brain_file(project["id"])

    if not path.exists():
        save_brain(project["id"], default_brain(project))


def ensure_all_brains(projects):
    for project in projects:
        ensure_brain(project)


def load_brain(place_id: str):
    path = brain_file(place_id)

    if not path.exists():
        return None

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def save_brain(place_id: str, brain: dict):
    place_folder(place_id).mkdir(parents=True, exist_ok=True)
    brain["metadata"]["last_updated"] = now()
    brain_file(place_id).write_text(json.dumps(brain, indent=2), encoding="utf-8")


def add_history(place_id: str, text: str):
    brain = load_brain(place_id)

    if not brain:
        return

    brain["history"].append(
        {
            "time": now(),
            "text": text,
        }
    )

    save_brain(place_id, brain)