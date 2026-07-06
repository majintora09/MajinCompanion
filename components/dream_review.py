import flet as ft

from components.card import card
from themes import colors, spacing
from memory.dreams import get_latest_dream


def dream_review_card():
    latest = get_latest_dream()

    text = latest if latest else "No dreams saved yet."

    return card(
        ft.Column(
            [
                ft.Text("Latest Dream", size=14, color=colors.EJ6_GREEN),
                ft.Text(text, size=14, color=colors.TEXT),
            ],
            spacing=spacing.SMALL_GAP,
        ),
        accent="purple",
    )