import flet as ft

from components.card import card
from components.button import quiet_button
from themes import colors, spacing
from core import screen
from memory.dreams import DREAM_FILE
from memory.goals import get_today_goal
from memory.activity import get_recent_activity


def back_button(on_navigate):
    return quiet_button(
        "Back to Campfire",
        icon=ft.Icons.ARROW_BACK,
        on_click=lambda e: on_navigate(screen.HOME),
    )


def dreams_screen(on_navigate):
    if DREAM_FILE.exists():
        content = DREAM_FILE.read_text(encoding="utf-8").strip()
    else:
        content = "No dreams saved yet."

    return ft.Column(
        [
            back_button(on_navigate),
            card(
                ft.Column(
                    [
                        ft.Text("Dreams", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("All saved ideas live here.", size=14, color=colors.MUTED),
                        ft.Text(content, size=14, color=colors.TEXT, selectable=True),
                    ],
                    spacing=spacing.SMALL_GAP,
                ),
                accent="purple",
            ),
        ],
        spacing=spacing.GAP,
    )


def goals_screen(on_navigate):
    goal = get_today_goal() or "No goal set yet."

    return ft.Column(
        [
            back_button(on_navigate),
            card(
                ft.Column(
                    [
                        ft.Text("Goals", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("Current mission.", size=14, color=colors.MUTED),
                        ft.Text(goal, size=18, color=colors.TEXT),
                    ],
                    spacing=spacing.SMALL_GAP,
                ),
                accent="green",
            ),
        ],
        spacing=spacing.GAP,
    )


def timeline_screen(on_navigate):
    activity = get_recent_activity(limit=20)

    return ft.Column(
        [
            back_button(on_navigate),
            card(
                ft.Column(
                    [
                        ft.Text("Timeline", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("Recent memory trail.", size=14, color=colors.MUTED),
                        *[ft.Text(f"• {item}", size=14, color=colors.TEXT) for item in activity],
                    ],
                    spacing=spacing.SMALL_GAP,
                ),
                accent="purple",
            ),
        ],
        spacing=spacing.GAP,
    )


def projects_screen(on_navigate):
    return ft.Column(
        [
            back_button(on_navigate),
            card(
                ft.Column(
                    [
                        ft.Text("Projects", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("Project manager coming next.", size=14, color=colors.MUTED),
                        ft.Text("Majin Rig MK1", size=18, color=colors.TEXT),
                        ft.Text("Majin Companion", size=18, color=colors.TEXT),
                    ],
                    spacing=spacing.SMALL_GAP,
                ),
                accent="green",
            ),
        ],
        spacing=spacing.GAP,
    )