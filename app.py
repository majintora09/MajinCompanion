import flet as ft

from core.companion import Companion


def main(page: ft.Page):
    app = Companion(page)
    app.start()


ft.run(main)