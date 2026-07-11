from memory.sessions import get_active_session
from places.manager import load_brain
from places.momentum import calculate_momentum, momentum_label


def build_place_context(place_id: str) -> str:
    brain = load_brain(place_id)

    if not brain:
        return "No Place context is available."

    identity = brain.get("identity", {})
    mission = brain.get("mission", {})
    notes = brain.get("notes", {})
    session = brain.get("session", {})

    active_session = get_active_session()

    if active_session and active_session.get("project_id") == place_id:
        session_context = {
            "active": True,
            "started": active_session.get("started", ""),
            "goal": active_session.get("goal", ""),
            "notes": active_session.get("notes", ""),
        }
    else:
        session_context = session if isinstance(session, dict) else {}

    mission_title = (
        mission.get("title", "")
        if isinstance(mission, dict)
        else str(mission or "")
    )

    notes_text = (
        notes.get("text", "")
        if isinstance(notes, dict)
        else str(notes or "")
    )

    score = calculate_momentum(place_id)

    discoveries = format_memories(
        brain.get("discoveries", []),
        limit=6,
    )
    dreams = format_memories(
        brain.get("dreams", []),
        limit=6,
    )
    history = format_memories(
        brain.get("history", []),
        limit=8,
    )

    return f"""
CURRENT PLACE

Name:
{identity.get("nickname") or identity.get("name") or place_id}

Full project name:
{identity.get("name", "")}

Status:
{identity.get("status", "")}

Priority:
{identity.get("priority", "Unknown")}

Momentum:
{score}/100 — {momentum_label(score)}

CURRENT MISSION

{mission_title or "No mission has been set."}

CURRENT SESSION

Active:
{bool(session_context.get("active"))}

Started:
{session_context.get("started") or "Unknown"}

Goal:
{session_context.get("goal") or "No session goal has been recorded."}

Session notes:
{session_context.get("notes") or "No session notes have been recorded."}

RECENT DISCOVERIES

{discoveries or "No discoveries have been saved yet."}

RECENT DREAMS

{dreams or "No dreams have been saved yet."}

PLACE NOTES

{trim_text(notes_text, 5000) or "No Place notes have been saved yet."}

RECENT HISTORY

{history or "No meaningful history has been saved yet."}
""".strip()


def format_memories(items: list, limit: int) -> str:
    rows = []

    for item in items[-limit:]:
        if isinstance(item, dict):
            timestamp = item.get("time", "")
            text = item.get("text", "")
        else:
            timestamp = ""
            text = str(item)

        if not text:
            continue

        prefix = f"[{timestamp}] " if timestamp else ""
        rows.append(f"- {prefix}{text}")

    return "\n".join(rows)


def trim_text(text: str, maximum: int) -> str:
    text = text.strip()

    if len(text) <= maximum:
        return text

    return text[:maximum] + "\n[Older text omitted from context.]"