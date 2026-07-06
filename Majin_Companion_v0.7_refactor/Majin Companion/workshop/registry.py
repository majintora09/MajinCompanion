PLACES = [
    {
        "id": "companion",
        "name": "Companion",
        "display": "The Companion",
        "icon": "🔥",
        "path": r"D:\Majin Companion",
        "url": None,
        "status": "Building Yuri's personal OS.",
        "color": "purple",
        "priority": 0,
        "momentum": 95,
    },
    {
        "id": "rig",
        "name": "Rig",
        "display": "The Rig",
        "icon": "🛠️",
        "path": r"D:\MAJIN RIG MK-1",
        "url": None,
        "status": "Designing the sim rig platform.",
        "color": "green",
        "priority": 1,
        "momentum": 80,
    },
    {
        "id": "garage",
        "name": "Garage",
        "display": "The Garage",
        "icon": "🚗",
        "path": r"C:\Users\Tora\EJ6-hub\ej6-garage",
        "url": "https://ej6-garage-main-pe5bqi.laravel.cloud/",
        "status": "Maintenance & upgrades.",
        "color": "purple",
        "priority": 2,
        "momentum": 45,
    },
    {
        "id": "riftlab",
        "name": "Lab",
        "display": "The Lab",
        "icon": "🥊",
        "path": r"C:\Users\Tora\Documents\DBFZ TEAM BUILDER",
        "url": "https://riftlab.pages.dev/",
        "status": "FG knowledge system.",
        "color": "green",
        "priority": 3,
        "momentum": 60,
    },
    {
        "id": "portfolio",
        "name": "Portfolio",
        "display": "The Portfolio",
        "icon": "🌐",
        "path": r"C:\Users\Tora\Documents\portfoliooo\MainHub",
        "url": "https://mainhub-5bg.pages.dev/#home",
        "status": "Show the world.",
        "color": "purple",
        "priority": 4,
        "momentum": 35,
    },
    {
        "id": "leaderboard",
        "name": "Leaderboard",
        "display": "The Leaderboard",
        "icon": "🏆",
        "path": r"C:\Users\Tora\leaderboard-hub",
        "url": "https://backfishracers.up.railway.app/",
        "status": "Community racing.",
        "color": "green",
        "priority": 5,
        "momentum": 30,
    },
]


def get_place(place_id):
    return next((place for place in PLACES if place["id"] == place_id), None)


def sorted_places():
    return sorted(PLACES, key=lambda place: place["priority"])


def highest_momentum_place():
    return max(PLACES, key=lambda place: place["momentum"])
