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
        "mission": {
            "title": "",
            "updated": "",
        },
        "session": {
            "active": False,
            "started": "",
            "goal": "",
        },
        "notes": {
            "text": "",
            "updated": "",
        },
        "dreams": [],
        "discoveries": [],
        "history": [],
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
    place_folder(project["id"]).mkdir(parents=True, exist_ok=True)
    path = brain_file(project["id"])

    if not path.exists():
        save_brain(project["id"], default_brain(project))
        return

    migrate_brain(project)


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
    brain.setdefault("metadata", {})
    brain["metadata"]["last_updated"] = now()
    brain_file(place_id).write_text(json.dumps(brain, indent=2), encoding="utf-8")


def migrate_brain(project: dict):
    brain = load_brain(project["id"])

    if not brain:
        save_brain(project["id"], default_brain(project))
        return

    base = default_brain(project)

    old_mission = brain.get("mission", "")
    old_notes = brain.get("notes", "")

    if isinstance(old_mission, str):
        base["mission"] = {
            "title": old_mission,
            "updated": brain.get("metadata", {}).get("last_updated", ""),
        }
    else:
        base["mission"] = old_mission

    if isinstance(old_notes, str):
        base["notes"] = {
            "text": old_notes,
            "updated": brain.get("metadata", {}).get("last_updated", ""),
        }
    else:
        base["notes"] = old_notes

    base["dreams"] = normalize_list(brain.get("dreams", []))
    base["discoveries"] = normalize_list(brain.get("discoveries", []))
    base["history"] = normalize_list(brain.get("history", []))
    base["sessions"] = brain.get("sessions", [])

    base["metadata"]["created"] = brain.get("metadata", {}).get("created", now())
    base["metadata"]["last_updated"] = now()

    save_brain(project["id"], base)


def normalize_list(items):
    normalized = []

    for item in items:
        if isinstance(item, dict):
            normalized.append(item)
        else:
            normalized.append(
                {
                    "time": "",
                    "text": str(item),
                }
            )

    return normalized


def add_history(place_id: str, text: str):
    brain = load_brain(place_id)

    if not brain:
        return

    brain.setdefault("history", [])
    brain["history"].append({"time": now(), "text": text})
    save_brain(place_id, brain)