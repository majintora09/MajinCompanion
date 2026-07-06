import flet as ft

from app.companion import Companion


def main(page: ft.Page):
    companion = Companion(page)
    companion.start()


ft.run(main)
