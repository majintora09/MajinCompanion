import flet as ft

from components.card import card
from components.button import quiet_button
from themes import colors, spacing
from memory.activity import get_recent_activity, clear_activity


def activity_card(on_refresh=None):
    activity = get_recent_activity()

    def clear_clicked(e):
        clear_activity()
        if on_refresh:
            on_refresh()

    return card(
        ft.Column(
            [
                ft.Text("Latest Activity", size=14, color=colors.EJ6_GREEN),
                *[ft.Text(f"• {item}", size=14, color=colors.TEXT) for item in activity],
                quiet_button("Clear activity", icon=ft.Icons.CHECK, on_click=clear_clicked),
            ],
            spacing=spacing.SMALL_GAP,
        ),
        accent="purple",
    )