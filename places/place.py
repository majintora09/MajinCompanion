from projects.registry import PROJECTS
from places.manager import load_brain, ensure_brain


def get_place(place_id: str):
    return next((p for p in PROJECTS if p["id"] == place_id), None)


def get_all_places():
    return sorted(PROJECTS, key=lambda p: p.get("priority", 99))


def get_place_brain(place_id: str):
    project = get_place(place_id)

    if not project:
        return None

    ensure_brain(project)
    return load_brain(place_id)