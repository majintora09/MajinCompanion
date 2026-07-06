import flet as ft
from activity.manager import get_recent_activity
from ui.card import card
from ui.buttons import quiet_button
from themes import colors, spacing


class TimelineView:
    def __init__(self, app):
        self.app = app

    def build(self):
        activity = get_recent_activity(limit=20)
        return ft.Column(
            [
                quiet_button("Back to Campfire", icon=ft.Icons.ARROW_BACK, on_click=lambda e: self.app.navigate("home")),
                card(
                    ft.Column(
                        [
                            ft.Text("Timeline", size=24, weight=ft.FontWeight.BOLD),
                            ft.Text("Recent memory trail.", size=14, color=colors.MUTED),
                            *[ft.Text(f"• {item}", size=14, color=colors.TEXT) for item in activity],
                        ],
                        spacing=spacing.SMALL_GAP,
                    ),
                    accent="purple",
                ),
            ],
            spacing=spacing.GAP,
        )
