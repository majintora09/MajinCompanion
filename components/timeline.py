import flet as ft

from components.card import card
from themes import colors, spacing


TIMELINE = [
    ("Today", "Started Embers"),
    ("Today", "Added Dream Mode"),
    ("Earlier", "Completed First Light"),
]


def timeline_card():
    return card(
        ft.Column(
            [
                ft.Text("Timeline", size=14, color=colors.EJ6_GREEN),
                *[
                    ft.Column(
                        [
                            ft.Text(date, size=12, color=colors.MAJIN_PURPLE),
                            ft.Text(event, size=14, color=colors.TEXT),
                        ],
                        spacing=2,
                    )
                    for date, event in TIMELINE
                ],
            ],
            spacing=spacing.SMALL_GAP,
        )
    )