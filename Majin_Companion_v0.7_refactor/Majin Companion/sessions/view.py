import flet as ft

from ui.card import card
from ui.buttons import primary_button, quiet_button
from themes import colors, spacing
from sessions.manager import get_active_session, update_active_session, end_active_session
from activity.manager import log_activity


class SessionView:
    def __init__(self, app):
        self.app = app

    def build(self):
        session = get_active_session()
        if not session:
            return ft.Column(
                [
                    quiet_button("Back to Campfire", icon=ft.Icons.ARROW_BACK, on_click=lambda e: self.app.navigate("home")),
                    card(
                        ft.Column(
                            [
                                ft.Text("No active session", size=24, weight=ft.FontWeight.BOLD),
                                ft.Text("Start one from the Workshop.", color=colors.MUTED),
                            ],
                            spacing=spacing.SMALL_GAP,
                        ),
                        accent="purple",
                    ),
                ],
                spacing=spacing.GAP,
            )

        feedback = ft.Text("", size=13, color=colors.EJ6_GREEN)
        goal_input = ft.TextField(
            value=session.get("goal", ""),
            hint_text="What are we doing in this session?",
            border_color=colors.EJ6_GREEN,
            focused_border_color=colors.MAJIN_PURPLE,
        )
        notes_input = ft.TextField(
            value=session.get("notes", ""),
            hint_text="Anything Future Yuri should remember?",
            multiline=True,
            min_lines=4,
            max_lines=8,
            border_color=colors.MAJIN_PURPLE,
            focused_border_color=colors.EJ6_GREEN,
        )

        def save_clicked(e):
            update_active_session(goal=goal_input.value, notes=notes_input.value)
            log_activity(f"💾 Saved session: {session['place_name']}")
            feedback.value = "Session saved. I got you."
            feedback.update()

        def end_clicked(e):
            end_active_session(summary=notes_input.value)
            self.app.toast("Session ended. Take that break.")
            self.app.navigate("home")

        return ft.Column(
            [
                quiet_button("Back to Campfire", icon=ft.Icons.ARROW_BACK, on_click=lambda e: self.app.navigate("home")),
                card(
                    ft.Column(
                        [
                            ft.Text(f"{session['place_icon']}  {session['place_name']}", size=26, weight=ft.FontWeight.BOLD),
                            ft.Text(f"Started: {session['started']}", size=13, color=colors.MUTED),
                            ft.Text("Leave enough behind that Future Yuri can continue.", size=14, color=colors.TEXT),
                            goal_input,
                            notes_input,
                            ft.Row(
                                [
                                    primary_button("Save session", icon=ft.Icons.SAVE, on_click=save_clicked),
                                    quiet_button("Take that break", icon=ft.Icons.COFFEE, on_click=end_clicked),
                                ],
                                spacing=spacing.SMALL_GAP,
                                wrap=True,
                            ),
                            feedback,
                        ],
                        spacing=spacing.SMALL_GAP,
                    ),
                    accent="green",
                ),
            ],
            spacing=spacing.GAP,
        )
