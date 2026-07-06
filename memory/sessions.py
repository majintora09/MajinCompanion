import json
from pathlib import Path
from datetime import datetime

from memory.activity import log_activity
from projects.brains import save_project_session, append_project_activity

ROOT = Path(__file__).resolve().parents[1]
SESSION_FILE = ROOT / "memory" / "active_session.json"
HISTORY_FILE = ROOT / "memory" / "sessions.json"


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
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def get_active_session():
    return load_json(SESSION_FILE, None)


def start_session(project):
    active = get_active_session()

    if active:
        return active

    session = {
        "project_id": project["id"],
        "project_name": project["name"],
        "project_icon": project["icon"],
        "started": now(),
        "goal": "",
        "notes": "",
    }

    save_json(SESSION_FILE, session)
    log_activity(f"▶️ Started session: {project['name']}")
    append_project_activity(project["id"], f"▶️ Started session: {now()}")

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

    save_project_session(session["project_id"], session)
    append_project_activity(session["project_id"], f"⏸️ Ended session: {now()}")

    SESSION_FILE.unlink(missing_ok=True)

    log_activity(f"⏸️ Ended session: {session['project_name']}")
    return session


def get_session_history(limit=5):
    history = load_json(HISTORY_FILE, [])
    return list(reversed(history[-limit:]))


def get_last_session():
    active = get_active_session()

    if active:
        return active

    history = get_session_history(limit=1)

    if history:
        return history[0]

    return None