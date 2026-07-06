import flet as ft

from core import screen
from core.thoughts import get_campfire_thought
from memory.goals import save_today_goal, get_today_goal
from memory.dreams import save_dream
from memory.activity import log_activity
from memory.sessions import get_active_session, get_last_session, start_session
from projects.registry import PROJECTS
from themes import colors, spacing
from components.card import card
from components.button import primary_button, quiet_button
from components.hero import hero
from components.background import grid_background
from components.quick_launch import quick_launch_card
from screens.memory_screens import dreams_screen, goals_screen, timeline_screen
from screens.projects import workshop
from screens.session import session_screen


class Companion:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_screen = screen.HOME

        self.goal_input = ft.TextField(
            hint_text="What matters right now?",
            border_color=colors.EJ6_GREEN,
            focused_border_color=colors.MAJIN_PURPLE,
        )

        self.dream_input = ft.TextField(
            hint_text="Catch the thought before it disappears...",
            multiline=True,
            min_lines=2,
            max_lines=4,
            border_color=colors.MAJIN_PURPLE,
            focused_border_color=colors.EJ6_GREEN,
        )

    def start(self):
        log_activity("🔥 Opened Companion")
        self.render()

    def render(self):
        self.page.title = "Majin Companion"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.window.width = 1200
        self.page.window.height = 780
        self.page.bgcolor = colors.BG
        self.page.padding = 0
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.clean()

        layout = ft.Container(
            padding=spacing.PAGE_PADDING,
            content=ft.Column(
                [
                    hero(),
                    ft.Divider(height=30, color=colors.BORDER),
                    self.screen_content(),
                ],
                spacing=spacing.GAP,
                scroll=ft.ScrollMode.AUTO,
            ),
        )

        self.page.add(grid_background(layout))
        self.page.update()

    def navigate(self, new_screen):
        self.current_screen = new_screen
        log_activity(f"🧭 Opened {new_screen}")
        self.render()

    def back_home(self):
        self.current_screen = screen.HOME
        self.render()

    def open_session(self):
        self.current_screen = screen.SESSION
        self.render()

    def screen_content(self):
        if self.current_screen == screen.DREAMS:
            return dreams_screen(self.navigate)

        if self.current_screen == screen.GOALS:
            return goals_screen(self.navigate)

        if self.current_screen == screen.TIMELINE:
            return timeline_screen(self.navigate)

        if self.current_screen == screen.PROJECTS:
            return workshop(self.back_home, self.toast, self.open_session)

        if self.current_screen == screen.SESSION:
            return session_screen(self.back_home, self.toast)

        return self.campfire()

    def campfire(self):
        return ft.Column(
            [
                self.where_were_we_card(),

                ft.Row(
                    [
                        ft.Container(self.mission_card(), expand=1),
                        ft.Container(self.thought_card(), expand=1),
                    ],
                    spacing=spacing.GAP,
                ),

                self.workshop_summary_card(),

                quiet_button(
                    "Open Workshop",
                    icon=ft.Icons.HANDYMAN,
                    on_click=lambda e: self.navigate(screen.PROJECTS),
                ),
            ],
            spacing=spacing.GAP,
        )

    def where_were_we_card(self):
        session = get_last_session()

        if not session:
            return card(
                ft.Column(
                    [
                        ft.Text("Where were we?", size=14, color=colors.EJ6_GREEN),
                        ft.Text("Nothing waiting yet.", size=28, weight=ft.FontWeight.BOLD),
                        ft.Text("Open the Workshop and start from a Place.", color=colors.MUTED),
                    ],
                    spacing=spacing.SMALL_GAP,
                ),
                accent="purple",
            )

        active = get_active_session() is not None
        button_text = "Continue session" if active else "Continue project"

        return card(
            ft.Column(
                [
                    ft.Text("Where were we?", size=14, color=colors.EJ6_GREEN),
                    ft.Text(
                        f"{session['project_icon']}  {session['project_name']}",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(f"Started: {session.get('started', 'Unknown')}", size=13, color=colors.MUTED),
                    ft.Text(
                        session.get("goal")
                        or session.get("summary")
                        or session.get("notes")
                        or "Ready to pick it back up.",
                        size=15,
                        color=colors.TEXT,
                    ),
                    primary_button(
                        button_text,
                        icon=ft.Icons.PLAY_ARROW,
                        on_click=lambda e: self.continue_last(session),
                    ),
                ],
                spacing=spacing.SMALL_GAP,
            ),
            accent="green",
        )

    def mission_card(self):
        goal = get_today_goal()

        return card(
            ft.Column(
                [
                    ft.Text("Current Mission", size=14, color=colors.EJ6_GREEN),
                    ft.Text(goal if goal else "No mission set.", size=16, color=colors.TEXT),
                    self.goal_input,
                    primary_button("Set mission", icon=ft.Icons.FLAG, on_click=self.save_goal_clicked),
                ],
                spacing=spacing.SMALL_GAP,
            ),
            accent="green",
        )

    def thought_card(self):
        return card(
            ft.Column(
                [
                    ft.Text("Campfire Thought", size=14, color=colors.EJ6_GREEN),
                    ft.Text(get_campfire_thought(), size=15, color=colors.TEXT),
                ],
                spacing=spacing.SMALL_GAP,
            ),
            accent="purple",
        )

    def workshop_summary_card(self):
        most_momentum = max(PROJECTS, key=lambda p: p.get("momentum", 0))

        return card(
            ft.Column(
                [
                    ft.Text("Workshop", size=14, color=colors.EJ6_GREEN),
                    ft.Text(f"{len(PROJECTS)} Places waiting.", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        f"Most momentum: {most_momentum['icon']} {most_momentum['name']} "
                        f"({most_momentum.get('momentum', 0)})",
                        size=14,
                        color=colors.TEXT,
                    ),
                    ft.Text("Places are dreams that decided to exist.", size=12, color=colors.MUTED),
                ],
                spacing=spacing.SMALL_GAP,
            ),
            accent="green",
        )

    def continue_last(self, session):
        active = get_active_session()

        if active:
            self.open_session()
            return

        project = next((p for p in PROJECTS if p["id"] == session["project_id"]), None)

        if not project:
            self.toast("Project not found anymore.")
            return

        start_session(project)
        self.open_session()

    def save_goal_clicked(self, e):
        text = self.goal_input.value

        if not text or not text.strip():
            self.toast("Give me a mission first.")
            return

        save_today_goal(text)
        log_activity("🎯 Set Current Mission")
        self.goal_input.value = ""
        self.render()
        self.toast("Mission set.")

    def save_dream_clicked(self, e):
        text = self.dream_input.value

        if not text or not text.strip():
            self.toast("Drop an idea first.")
            return

        save_dream(text)
        self.dream_input.value = ""
        self.render()
        self.toast("Dream saved.")

    def toast(self, message):
        self.page.snack_bar = ft.SnackBar(ft.Text(message))
        self.page.snack_bar.open = True
        self.page.update()