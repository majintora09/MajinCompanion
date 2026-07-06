import flet as ft

from workshop.registry import get_place
from sessions.manager import start_session
from brains.manager import get_place_sessions, read_text, append_text
from ui.card import card
from ui.buttons import primary_button, quiet_button
from themes import colors, spacing


class BrainView:
    def __init__(self, app, place_id):
        self.app = app
        self.place = get_place(place_id)
        self.note_input = ft.TextField(
            hint_text="Leave something Future Yuri should know...",
            multiline=True,
            min_lines=3,
            max_lines=6,
            border_color=colors.EJ6_GREEN,
            focused_border_color=colors.MAJIN_PURPLE,
        )
        self.dream_input = ft.TextField(
            hint_text="Idea for this place...",
            multiline=True,
            min_lines=2,
            max_lines=4,
            border_color=colors.MAJIN_PURPLE,
            focused_border_color=colors.EJ6_GREEN,
        )

    def build(self):
        if not self.place:
            return ft.Column([quiet_button("Back", on_click=lambda e: self.app.navigate("workshop")), ft.Text("Place not found.")])

        return ft.Column(
            [
                quiet_button("Back to Workshop", icon=ft.Icons.ARROW_BACK, on_click=lambda e: self.app.navigate("workshop")),
                self.header(),
                ft.Row(
                    [
                        ft.Container(self.sessions_card(), expand=1),
                        ft.Container(self.activity_card(), expand=1),
                    ],
                    spacing=spacing.GAP,
                ),
                ft.Row(
                    [
                        ft.Container(self.notes_card(), expand=1),
                        ft.Container(self.dreams_card(), expand=1),
                    ],
                    spacing=spacing.GAP,
                ),
            ],
            spacing=spacing.GAP,
            scroll=ft.ScrollMode.AUTO,
        )

    def header(self):
        p = self.place
        return card(
            ft.Column(
                [
                    ft.Text(f"{p['icon']}  {p['display']}", size=30, weight=ft.FontWeight.BOLD),
                    ft.Text(p["status"], color=colors.MUTED),
                    ft.Text(f"Priority: {p['priority']:02d}   Momentum: {p['momentum']}", size=13, color=colors.MAJIN_PURPLE),
                    primary_button("Continue", icon=ft.Icons.PLAY_ARROW, on_click=self.continue_place),
                ],
                spacing=spacing.SMALL_GAP,
            ),
            accent=p["color"],
        )

    def continue_place(self, e):
        start_session(self.place)
        self.app.navigate("session")

    def sessions_card(self):
        sessions = get_place_sessions(self.place["id"], limit=5)
        items = []
        if not sessions:
            items.append(ft.Text("No sessions yet.", color=colors.MUTED))
        else:
            for s in sessions:
                items.append(ft.Text(f"• {s.get('started')} — {s.get('summary') or s.get('goal') or 'Session'}", size=14, color=colors.TEXT))

        return card(
            ft.Column([ft.Text("Sessions", size=14, color=colors.EJ6_GREEN), *items], spacing=spacing.SMALL_GAP),
            accent="green",
        )

    def activity_card(self):
        text = read_text(self.place["id"], "activity.md", "# Activity\n")
        lines = [line for line in text.splitlines() if line.startswith("- ")][-8:]
        if not lines:
            lines = ["- No activity yet."]

        return card(
            ft.Column([ft.Text("Activity", size=14, color=colors.EJ6_GREEN), *[ft.Text(line, size=14, color=colors.TEXT) for line in lines]], spacing=spacing.SMALL_GAP),
            accent="purple",
        )

    def notes_card(self):
        notes = read_text(self.place["id"], "notes.md", "# Notes\n")
        preview = "\n".join(notes.splitlines()[-6:]) or "No notes yet."
        return card(
            ft.Column(
                [
                    ft.Text("Notes", size=14, color=colors.EJ6_GREEN),
                    ft.Text(preview, size=13, color=colors.MUTED, selectable=True),
                    self.note_input,
                    primary_button("Add note", icon=ft.Icons.NOTE_ADD, on_click=self.add_note),
                ],
                spacing=spacing.SMALL_GAP,
            ),
            accent="green",
        )

    def add_note(self, e):
        text = self.note_input.value
        if not text or not text.strip():
            self.app.toast("Write the note first.")
            return
        append_text(self.place["id"], "notes.md", f"\n## Note\n{text.strip()}\n")
        self.note_input.value = ""
        self.app.render()
        self.app.toast("Note saved.")

    def dreams_card(self):
        dreams = read_text(self.place["id"], "dreams.md", "# Dreams\n")
        preview = "\n".join(dreams.splitlines()[-6:]) or "No dreams yet."
        return card(
            ft.Column(
                [
                    ft.Text("Dreams", size=14, color=colors.EJ6_GREEN),
                    ft.Text(preview, size=13, color=colors.MUTED, selectable=True),
                    self.dream_input,
                    primary_button("Add dream", icon=ft.Icons.AUTO_AWESOME, on_click=self.add_dream),
                ],
                spacing=spacing.SMALL_GAP,
            ),
            accent="purple",
        )

    def add_dream(self, e):
        text = self.dream_input.value
        if not text or not text.strip():
            self.app.toast("Drop the dream first.")
            return
        append_text(self.place["id"], "dreams.md", f"\n## Dream\n{text.strip()}\n")
        self.dream_input.value = ""
        self.app.render()
        self.app.toast("Dream saved to this place.")
