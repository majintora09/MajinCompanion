import flet as ft

from app.version import VERSION, CODENAME
from sessions.manager import get_active_session, get_last_session, start_session
from goals.manager import save_today_goal, get_today_goal
from dreams.manager import save_dream, get_latest_dream, count_dreams
from activity.manager import get_recent_activity, log_activity
from workshop.registry import PLACES, get_place, highest_momentum_place
from campfire.thoughts import campfire_thought
from ui.card import card
from ui.buttons import primary_button, quiet_button
from themes import colors, spacing


def greeting():
    return "Where were we?"


class CampfireView:
    def __init__(self, app):
        self.app = app
        self.goal_input = ft.TextField(
            hint_text="Today's mission...",
            border_color=colors.EJ6_GREEN,
            focused_border_color=colors.MAJIN_PURPLE,
        )
        self.dream_input = ft.TextField(
            hint_text="Catch a thought without losing the thread...",
            multiline=True,
            min_lines=2,
            max_lines=4,
            border_color=colors.MAJIN_PURPLE,
            focused_border_color=colors.EJ6_GREEN,
        )

    def build(self):
        return ft.Column(
            [
                self.hero(),
                ft.Divider(height=30, color=colors.BORDER),
                self.continue_card(),
                ft.Row(
                    [
                        ft.Container(self.mission_card(), expand=1),
                        ft.Container(self.thought_card(), expand=1),
                    ],
                    spacing=spacing.GAP,
                ),
                ft.Row(
                    [
                        ft.Container(self.workshop_summary(), expand=1),
                        ft.Container(self.dream_capture(), expand=1),
                    ],
                    spacing=spacing.GAP,
                ),
            ],
            spacing=spacing.GAP,
        )

    def hero(self):
        return ft.Column(
            [
                ft.Text("🔥", size=44),
                ft.Text(greeting(), size=32, weight=ft.FontWeight.BOLD),
                ft.Text("Future Yuri left the tools where we need them.", size=16, color=colors.MUTED),
                ft.Text(f"MJC v{VERSION} — {CODENAME}", size=12, color=colors.MAJIN_PURPLE),
            ],
            spacing=8,
        )

    def continue_card(self):
        session = get_last_session()
        if not session:
            return card(
                ft.Column(
                    [
                        ft.Text("Campfire", size=14, color=colors.EJ6_GREEN),
                        ft.Text("No previous session yet.", size=26, weight=ft.FontWeight.BOLD),
                        ft.Text("Open the Workshop and choose a place when you're ready.", color=colors.MUTED),
                        primary_button("Open Workshop", icon=ft.Icons.HANDYMAN, on_click=lambda e: self.app.navigate("workshop")),
                    ],
                    spacing=spacing.SMALL_GAP,
                ),
                accent="purple",
            )

        is_active = get_active_session() is not None
        title = "Continue session" if is_active else "Continue project"
        place_name = session.get("place_name") or session.get("project_name")
        place_icon = session.get("place_icon") or session.get("project_icon")
        summary = session.get("goal") or session.get("summary") or "Ready to pick it back up."

        return card(
            ft.Column(
                [
                    ft.Text("Last Worked On", size=14, color=colors.EJ6_GREEN),
                    ft.Text(f"{place_icon}  {place_name}", size=28, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Started: {session.get('started', 'Unknown')}", size=13, color=colors.MUTED),
                    ft.Text(summary, size=15, color=colors.TEXT),
                    primary_button(title, icon=ft.Icons.PLAY_ARROW, on_click=lambda e: self.continue_last(session)),
                ],
                spacing=spacing.SMALL_GAP,
            ),
            accent="green",
        )

    def continue_last(self, session):
        if get_active_session():
            self.app.navigate("session")
            return
        place_id = session.get("place_id") or session.get("project_id")
        place = get_place(place_id)
        if not place:
            self.app.toast("Place not found anymore.")
            return
        start_session(place)
        self.app.navigate("session")

    def mission_card(self):
        current_goal = get_today_goal()
        return card(
            ft.Column(
                [
                    ft.Text("Today's Mission", size=14, color=colors.EJ6_GREEN),
                    ft.Text(current_goal or "No mission set yet.", size=15, color=colors.TEXT),
                    self.goal_input,
                    primary_button("Set mission", icon=ft.Icons.FLAG, on_click=self.save_goal),
                ],
                spacing=spacing.SMALL_GAP,
            ),
            accent="green",
        )

    def save_goal(self, e):
        text = self.goal_input.value
        if not text or not text.strip():
            self.app.toast("Give me a mission first.")
            return
        save_today_goal(text)
        log_activity("🎯 Set Today's Mission")
        self.goal_input.value = ""
        self.app.render()
        self.app.toast("Mission saved.")

    def thought_card(self):
        return card(
            ft.Column(
                [
                    ft.Text("Campfire Thought", size=14, color=colors.EJ6_GREEN),
                    ft.Text(campfire_thought(), size=15, color=colors.TEXT),
                ],
                spacing=spacing.SMALL_GAP,
            ),
            accent="purple",
        )

    def workshop_summary(self):
        place = highest_momentum_place()
        return card(
            ft.Column(
                [
                    ft.Text("Workshop", size=14, color=colors.EJ6_GREEN),
                    ft.Text(f"{len(PLACES)} places", size=22, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Most momentum: {place['icon']} {place['display']} ({place['momentum']})", color=colors.TEXT),
                    quiet_button("Enter Workshop", icon=ft.Icons.HANDYMAN, on_click=lambda e: self.app.navigate("workshop")),
                ],
                spacing=spacing.SMALL_GAP,
            ),
            accent="green",
        )

    def dream_capture(self):
        latest = get_latest_dream()
        return card(
            ft.Column(
                [
                    ft.Text("Dream Catcher", size=14, color=colors.EJ6_GREEN),
                    ft.Text(f"{count_dreams()} thoughts saved.", size=14, color=colors.TEXT),
                    ft.Text(latest or "Nothing waiting yet.", size=12, color=colors.MUTED),
                    self.dream_input,
                    primary_button("Catch thought", icon=ft.Icons.AUTO_AWESOME, on_click=self.save_dream),
                ],
                spacing=spacing.SMALL_GAP,
            ),
            accent="purple",
        )

    def save_dream(self, e):
        text = self.dream_input.value
        if not text or not text.strip():
            self.app.toast("Drop the thought first.")
            return
        save_dream(text)
        self.dream_input.value = ""
        self.app.render()
        self.app.toast("Thought saved.")
