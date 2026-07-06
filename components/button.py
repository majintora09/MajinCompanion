import flet as ft
from themes import colors


def primary_button(text, icon=None, on_click=None):
    return ft.ElevatedButton(
        text,
        icon=icon,
        on_click=on_click,
        style=ft.ButtonStyle(
            bgcolor=colors.MAJIN_PURPLE,
            color=colors.TEXT,
        ),
    )


def quiet_button(text, icon=None, on_click=None):
    return ft.OutlinedButton(
        text,
        icon=icon,
        on_click=on_click,
    )