from memory.goals import get_today_goal


def get_campfire_thought():
    goal = get_today_goal()

    if not goal:
        return "Set a goal first. Then I'll help keep us pointed at it."

    return f"Today's mission is still: {goal}"