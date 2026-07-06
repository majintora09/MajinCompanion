import os
import webbrowser
import flet as ft

from workshop.registry import sorted_places
from sessions.manager import start_session
from ui.card import card
from ui.buttons import primary_button, quiet_button
from themes import colors, spacing


class WorkshopView:
    def __init__(self, app):
        self.app = app

    def build(self):
        cards = []
        for place in sorted_places():
            buttons = [
                primary_button("Continue", icon=ft.Icons.PLAY_ARROW, on_click=lambda e, p=place: self.continue_place(p)),
                quiet_button("Brain", icon=ft.Icons.PSYCHOLOGY, on_click=lambda e, p=place: self.open_brain(p)),
                quiet_button("Folder", icon=ft.Icons.FOLDER_OPEN, on_click=lambda e, p=place: self.open_folder(p)),
            ]
            if place.get("url"):
                buttons.append(quiet_button("Website", icon=ft.Icons.LANGUAGE, on_click=lambda e, p=place: self.open_website(p)))

            cards.append(
                card(
                    ft.Column(
                        [
                            ft.Text(f"{place['icon']}  {place['display']}", size=22, weight=ft.FontWeight.BOLD),
                            ft.Text(place["status"], size=14, color=colors.MUTED),
                            ft.Text(f"Priority: {place['priority']:02d}   Momentum: {place['momentum']}", size=12, color=colors.MAJIN_PURPLE),
                            ft.Text(place["path"], size=11, color=colors.MUTED),
                            ft.Row(buttons, spacing=spacing.SMALL_GAP, wrap=True),
                        ],
                        spacing=spacing.SMALL_GAP,
                    ),
                    accent=place["color"],
                )
            )

        return ft.Column(
            [
                quiet_button("Back to Campfire", icon=ft.Icons.ARROW_BACK, on_click=lambda e: self.app.navigate("home")),
                ft.Text("Workshop", size=30, weight=ft.FontWeight.BOLD),
                ft.Text("Places are ideas waiting to be realized.", size=14, color=colors.MUTED),
                *cards,
            ],
            spacing=spacing.GAP,
            scroll=ft.ScrollMode.AUTO,
        )

    def continue_place(self, place):
        start_session(place)
        self.app.toast(f"Continuing {place['display']}.")
        self.app.navigate("session")

    def open_brain(self, place):
        self.app.selected_place_id = place["id"]
        self.app.navigate("brain")

    def open_folder(self, place):
        if not os.path.exists(place["path"]):
            self.app.toast(f"Path not found: {place['path']}")
            return
        os.startfile(place["path"])
        self.app.toast(f"Opened {place['display']} folder.")

    def open_website(self, place):
        if not place.get("url"):
            self.app.toast(f"No website linked for {place['display']}.")
            return
        webbrowser.open(place["url"])
        self.app.toast(f"Opened {place['display']} website.")
