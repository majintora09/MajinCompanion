import flet as ft

from components.card import card
from components.button import quiet_button
from launcher.launcher import get_screen_for_item
from themes import colors, spacing


def quick_launch_card(on_navigate):
    def clicked(name):
        on_navigate(get_screen_for_item(name))

    return card(
        ft.Column(
            [
                ft.Text("Quick Launch", size=14, color=colors.EJ6_GREEN),
                ft.Row(
                    [
                        quiet_button("Dreams", icon=ft.Icons.NIGHTLIGHT, on_click=lambda e: clicked("Dreams")),
                        quiet_button("Goals", icon=ft.Icons.FLAG, on_click=lambda e: clicked("Goals")),
                        quiet_button("Workshop", icon=ft.Icons.HANDYMAN, on_click=lambda e: clicked("Workshop")),
                        quiet_button("Timeline", icon=ft.Icons.TIMELINE, on_click=lambda e: clicked("Timeline")),
                    ],
                    spacing=spacing.SMALL_GAP,
                    wrap=True,
                ),
            ],
            spacing=spacing.SMALL_GAP,
        ),
        accent="green",
    )