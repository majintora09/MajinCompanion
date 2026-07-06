import flet as ft

from components.card import card
from themes import colors, spacing
from memory.dreams import count_dreams


def stats_card():
    return card(
        ft.Column(
            [
                ft.Text("Status", size=14, color=colors.EJ6_GREEN),
                ft.Text(f"{count_dreams()} dreams saved", size=16, color=colors.TEXT),
                ft.Text("MJC is starting to remember.", size=12, color=colors.MUTED),
            ],
            spacing=spacing.SMALL_GAP,
        )
    )