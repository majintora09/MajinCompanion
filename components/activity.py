import flet as ft

from components.card import card
from themes import colors, spacing
from memory.activity import get_recent_activity


def activity_card():
    activity = get_recent_activity()

    return card(
        ft.Column(
            [
                ft.Text("Latest Activity", size=14, color=colors.EJ6_GREEN),
                *[ft.Text(f"• {item}", size=14, color=colors.TEXT) for item in activity],
            ],
            spacing=spacing.SMALL_GAP,
        )
    )