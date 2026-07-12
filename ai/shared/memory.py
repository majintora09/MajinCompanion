from ai.context import build_place_context


def get_place_memory(place_id: str) -> str:
    return build_place_context(place_id)