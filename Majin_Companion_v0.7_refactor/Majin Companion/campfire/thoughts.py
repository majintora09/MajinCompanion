from goals.manager import get_today_goal
from sessions.manager import get_last_session
from workshop.registry import highest_momentum_place


def campfire_thought():
    session = get_last_session()
    if session and (session.get("goal") or session.get("summary")):
        return "You left enough context to continue. That's the point."

    goal = get_today_goal()
    if goal:
        return f"Today's mission is still: {goal}"

    place = highest_momentum_place()
    return f"{place['display']} has the most momentum right now."
