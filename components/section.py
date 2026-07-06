import flet as ft

from themes import colors, spacing


def section(title, content, subtitle=None, accent="green"):
    accent_color = colors.EJ6_GREEN if accent == "green" else colors.MAJIN_PURPLE

    header = [
        ft.Container(height=2, bgcolor=accent_color, border_radius=8),
        ft.Text(title, size=15, color=accent_color),
    ]

    if subtitle:
        header.append(ft.Text(subtitle, size=12, color=colors.MUTED))

    return ft.Container(
        padding=spacing.CARD_PADDING,
        border_radius=spacing.CARD_RADIUS,
        bgcolor=colors.CARD,
        content=ft.Column(
            [
                *header,
                content,
            ],
            spacing=spacing.SMALL_GAP,
        ),
    )