import flet as ft
from themes import colors, spacing


def card(content, on_click=None, accent="purple"):
    accent_color = colors.MAJIN_PURPLE if accent == "purple" else colors.EJ6_GREEN

    return ft.Container(
        padding=spacing.CARD_PADDING,
        border_radius=spacing.CARD_RADIUS,
        bgcolor=colors.CARD,
        content=ft.Column(
            [
                ft.Container(height=3, bgcolor=accent_color, border_radius=10),
                content,
            ],
            spacing=spacing.SMALL_GAP,
        ),
        on_click=on_click,
    )