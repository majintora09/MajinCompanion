from places.manager import load_brain
from places.momentum import calculate_momentum, momentum_label


def future_yuri_message(place_id: str):
    brain = load_brain(place_id)

    if not brain:
        return "I don't know this Place yet."

    nickname = brain.get("identity", {}).get("nickname", "this Place")
    score = calculate_momentum(place_id)
    label = momentum_label(score)

    discoveries = brain.get("discoveries", [])

    if brain.get("session", {}).get("active"):
        return f"{nickname} still has an active session. Let's pick it back up."

    if discoveries:
        latest = discoveries[-1]["text"]
        return f"Last useful discovery here: {latest}"

    if score >= 50:
        return f"{nickname} has {label.lower()}. Should be easy to continue."

    return f"{nickname} is quiet right now. No pressure."