import flet as ft

from app import screen
from workshop.registry import PLACES
from brains.manager import ensure_all_brains
from activity.manager import log_activity
from ui.background import grid_background
from themes import colors, spacing
from campfire.view import CampfireView
from workshop.view import WorkshopView
from brains.view import BrainView
from sessions.view import SessionView
from activity.view import TimelineView


class Companion:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_screen = screen.HOME
        self.selected_place_id = None
        ensure_all_brains(PLACES)

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
            content=self.screen_content(),
        )

        self.page.add(grid_background(layout))
        self.page.update()

    def navigate(self, new_screen):
        self.current_screen = new_screen
        log_activity(f"🧭 Opened {new_screen}")
        self.render()

    def screen_content(self):
        if self.current_screen == screen.WORKSHOP:
            return WorkshopView(self).build()

        if self.current_screen == screen.BRAIN:
            return BrainView(self, self.selected_place_id).build()

        if self.current_screen == screen.SESSION:
            return SessionView(self).build()

        if self.current_screen == screen.TIMELINE:
            return TimelineView(self).build()

        return CampfireView(self).build()

    def toast(self, message):
        self.page.snack_bar = ft.SnackBar(ft.Text(message))
        self.page.snack_bar.open = True
        self.page.update()
