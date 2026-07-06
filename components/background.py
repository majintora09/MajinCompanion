import flet as ft
from themes import colors


def grid_background(content):
    return ft.Stack(
        [
            ft.Container(bgcolor=colors.BG, expand=True),
            ft.Container(
                opacity=0.18,
                content=ft.Column(
                    [
                        ft.Text(
                            "╋ " * 120,
                            color=colors.BG_GRID,
                            size=10,
                        )
                        for _ in range(70)
                    ],
                    spacing=0,
                ),
            ),
            content,
        ],
        expand=True,
    )