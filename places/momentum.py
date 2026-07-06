from places.manager import load_brain


def calculate_momentum(place_id: str):
    brain = load_brain(place_id)

    if not brain:
        return 0

    score = 0

    if brain.get("mission", {}).get("title"):
        score += 25

    if brain.get("session", {}).get("active"):
        score += 30

    score += min(len(brain.get("discoveries", [])) * 10, 30)
    score += min(len(brain.get("history", [])) * 2, 15)

    return min(score, 100)


def momentum_label(score: int):
    if score >= 80:
        return "High momentum"
    if score >= 50:
        return "Good momentum"
    if score >= 25:
        return "Warm"
    return "Quiet"