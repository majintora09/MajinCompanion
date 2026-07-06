import json
from pathlib import Path
from datetime import datetime

from activity.manager import log_activity
from brains.manager import save_place_session, append_place_activity

ROOT = Path(__file__).resolve().parents[1]
SESSION_FILE = ROOT / "data" / "global" / "active_session.json"
HISTORY_FILE = ROOT / "data" / "global" / "sessions.json"


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def load_json(path, fallback):
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def get_active_session():
    return load_json(SESSION_FILE, None)


def start_session(place):
    active = get_active_session()
    if active:
        return active

    session = {
        "place_id": place["id"],
        "place_name": place["display"],
        "place_icon": place["icon"],
        "started": now(),
        "goal": "",
        "notes": "",
    }

    save_json(SESSION_FILE, session)
    log_activity(f"▶️ Started session: {place['display']}")
    append_place_activity(place["id"], f"▶️ Started session: {now()}")
    return session


def update_active_session(goal=None, notes=None):
    session = get_active_session()
    if not session:
        return None

    if goal is not None:
        session["goal"] = goal.strip()
    if notes is not None:
        session["notes"] = notes.strip()

    save_json(SESSION_FILE, session)
    return session


def end_active_session(summary=""):
    session = get_active_session()
    if not session:
        return None

    session["ended"] = now()
    session["summary"] = summary.strip()

    history = load_json(HISTORY_FILE, [])
    history.append(session)
    save_json(HISTORY_FILE, history)

    place_id = session.get("place_id") or session.get("project_id")
    if place_id:
        save_place_session(place_id, session)
        append_place_activity(place_id, f"⏸️ Ended session: {now()}")

    SESSION_FILE.unlink(missing_ok=True)
    log_activity(f"⏸️ Ended session: {session['place_name']}")
    return session


def get_session_history(limit=5):
    history = load_json(HISTORY_FILE, [])
    return list(reversed(history[-limit:]))


def get_last_session():
    active = get_active_session()
    if active:
        return active
    history = get_session_history(limit=1)
    return history[0] if history else None
