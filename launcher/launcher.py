from core import screen


def get_screen_for_item(name: str):
    screens = {
        "Dreams": screen.DREAMS,
        "Goals": screen.GOALS,
        "Workshop": screen.PROJECTS,
        "Timeline": screen.TIMELINE,
    }

    return screens.get(name, screen.HOME)