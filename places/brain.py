from places.manager import load_brain, save_brain, now


def get_notes(place_id: str):
    brain = load_brain(place_id)
    if not brain:
        return ""

    notes = brain.get("notes", "")
    if isinstance(notes, dict):
        return notes.get("text", "")

    return notes


def set_notes(place_id: str, text: str):
    brain = load_brain(place_id)
    if not brain:
        return

    brain["notes"] = {
        "text": text,
        "updated": now(),
    }

    add_history_entry(brain, "📝 Notes updated")
    save_brain(place_id, brain)


def add_dream(place_id: str, text: str):
    brain = load_brain(place_id)
    if not brain:
        return

    brain.setdefault("dreams", [])
    brain["dreams"].append(
        {
            "time": now(),
            "text": text.strip(),
        }
    )

    add_history_entry(brain, f"🧠 Dream saved: {text.strip()}")
    save_brain(place_id, brain)


def add_discovery(place_id: str, text: str):
    brain = load_brain(place_id)
    if not brain:
        return

    brain.setdefault("discoveries", [])
    brain["discoveries"].append(
        {
            "time": now(),
            "text": text.strip(),
        }
    )

    add_history_entry(brain, f"💡 Discovery: {text.strip()}")
    save_brain(place_id, brain)


def get_recent_dreams(place_id: str, limit=5):
    brain = load_brain(place_id)
    if not brain:
        return []

    return list(reversed(brain.get("dreams", [])[-limit:]))


def get_recent_discoveries(place_id: str, limit=5):
    brain = load_brain(place_id)
    if not brain:
        return []

    return list(reversed(brain.get("discoveries", [])[-limit:]))


def get_history(place_id: str, limit=8):
    brain = load_brain(place_id)
    if not brain:
        return []

    return list(reversed(brain.get("history", [])[-limit:]))


def add_history_entry(brain: dict, text: str):
    brain.setdefault("history", [])
    brain["history"].append(
        {
            "time": now(),
            "text": text,
        }
    )