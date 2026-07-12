import asyncio
from typing import Callable

import flet as ft

from ai.client import OllamaError
from themes import colors, spacing


class ChatPanel:
    def __init__(
        self,
        page: ft.Page,
        worker_name: str,
        panel_title: str,
        panel_subtitle: str,
        intro_message: str,
        input_hint: str,
        ask_callback: Callable[[str], str],
        save_discovery_callback: Callable[[str], None] | None = None,
        add_notes_callback: Callable[[str], None] | None = None,
        update_mission_callback: Callable[[str], None] | None = None,
        show_memory_actions: bool = True,
    ):
        self.page = page
        self.worker_name = worker_name
        self.ask_callback = ask_callback

        self.save_discovery_callback = save_discovery_callback
        self.add_notes_callback = add_notes_callback
        self.update_mission_callback = update_mission_callback
        self.show_memory_actions = show_memory_actions

        self.latest_answer = ""
        self.is_generating = False

        self.messages = ft.Column(
            controls=[
                self.message_bubble(
                    worker_name,
                    intro_message,
                    is_user=False,
                )
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
        )

        self.input = ft.TextField(
            hint_text=input_hint,
            multiline=True,
            min_lines=1,
            max_lines=5,
            border_color=colors.MAJIN_PURPLE,
            focused_border_color=colors.EJ6_GREEN,
            expand=True,
        )

        self.status = ft.Text(
            "Local • qwen3:8b",
            size=11,
            color=colors.MUTED,
        )

        self.memory_actions = ft.Row(
            controls=[],
            visible=False,
            wrap=True,
            spacing=spacing.SMALL_GAP,
        )

        self.send_button = ft.IconButton(
            icon=ft.Icons.SEND,
            tooltip="Send",
            on_click=self.send,
        )

        self.control = ft.Container(
            visible=False,
            width=470,
            padding=20,
            border_radius=18,
            bgcolor=colors.CARD,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        panel_title,
                                        size=22,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(
                                        panel_subtitle,
                                        size=12,
                                        color=colors.MUTED,
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                tooltip="Close panel",
                                on_click=lambda e: self.hide(),
                            ),
                        ]
                    ),
                    ft.Divider(color=colors.BORDER),
                    ft.Container(
                        content=self.messages,
                        height=500,
                    ),
                    ft.Divider(color=colors.BORDER),
                    ft.Row(
                        [
                            self.input,
                            self.send_button,
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.END,
                    ),
                    self.status,
                    self.memory_actions,
                ],
                spacing=12,
            ),
        )

    def show(self):
        self.control.visible = True

        if self.control.page:
            self.control.update()

    def hide(self):
        self.control.visible = False

        if self.control.page:
            self.control.update()

    def toggle(self):
        self.control.visible = not self.control.visible

        if self.control.page:
            self.control.update()

    async def send(self, e):
        if self.is_generating:
            return

        text = (self.input.value or "").strip()

        if not text:
            self.status.value = "Say something first."
            self.status.update()
            return

        self.is_generating = True

        self.input.value = ""
        self.input.disabled = True
        self.send_button.disabled = True
        self.memory_actions.visible = False

        self.messages.controls.append(
            self.message_bubble(
                "You",
                text,
                is_user=True,
            )
        )

        thinking = self.thinking_bubble()
        self.messages.controls.append(thinking)

        self.status.value = f"{self.worker_name} is working..."

        self.input.update()
        self.send_button.update()
        self.memory_actions.update()
        self.messages.update()
        self.status.update()

        await asyncio.sleep(0)

        try:
            answer = await asyncio.to_thread(
                self.ask_callback,
                text,
            )

            self.latest_answer = answer

            if thinking in self.messages.controls:
                self.messages.controls.remove(thinking)

            self.messages.controls.append(
                self.message_bubble(
                    self.worker_name,
                    answer,
                    is_user=False,
                )
            )

            if self.show_memory_actions:
                self.build_memory_actions()
                self.memory_actions.visible = True
                self.status.value = "What should I remember?"
            else:
                self.status.value = "Read-only preview complete."

        except OllamaError as error:
            if thinking in self.messages.controls:
                self.messages.controls.remove(thinking)

            self.messages.controls.append(
                self.message_bubble(
                    self.worker_name,
                    str(error),
                    is_user=False,
                    is_error=True,
                )
            )

            self.status.value = "Couldn't reach Ollama."

        except Exception as error:
            if thinking in self.messages.controls:
                self.messages.controls.remove(thinking)

            self.messages.controls.append(
                self.message_bubble(
                    self.worker_name,
                    f"Something went wrong: {error}",
                    is_user=False,
                    is_error=True,
                )
            )

            self.status.value = "Something went wrong."

        finally:
            self.is_generating = False
            self.input.disabled = False
            self.send_button.disabled = False

            self.messages.update()
            self.memory_actions.update()
            self.status.update()
            self.input.update()
            self.send_button.update()

    def build_memory_actions(self):
        controls = [
            ft.TextButton(
                "Nothing",
                icon=ft.Icons.CLOSE,
                on_click=self.dismiss_memory,
            )
        ]

        if self.save_discovery_callback:
            controls.append(
                ft.TextButton(
                    "Save discovery",
                    icon=ft.Icons.LIGHTBULB,
                    on_click=self.save_discovery,
                )
            )

        if self.add_notes_callback:
            controls.append(
                ft.TextButton(
                    "Add to notes",
                    icon=ft.Icons.NOTE_ADD,
                    on_click=self.add_to_notes,
                )
            )

        if self.update_mission_callback:
            controls.append(
                ft.TextButton(
                    "Update mission",
                    icon=ft.Icons.FLAG,
                    on_click=self.update_mission,
                )
            )

        self.memory_actions.controls = controls

    def dismiss_memory(self, e):
        self.memory_actions.visible = False
        self.status.value = "Nothing saved. That's okay."
        self.memory_actions.update()
        self.status.update()

    def save_discovery(self, e):
        if not self.latest_answer or not self.save_discovery_callback:
            return

        self.save_discovery_callback(self.latest_answer)
        self.status.value = "Saved as a Discovery."
        self.status.update()

    def add_to_notes(self, e):
        if not self.latest_answer or not self.add_notes_callback:
            return

        self.add_notes_callback(self.latest_answer)
        self.status.value = "Added to Notes."
        self.status.update()

    def update_mission(self, e):
        if not self.latest_answer or not self.update_mission_callback:
            return

        mission = self.first_useful_line(self.latest_answer)
        self.update_mission_callback(mission)

        self.status.value = f"Mission updated: {mission}"
        self.status.update()

    def message_bubble(
        self,
        speaker: str,
        text: str,
        is_user: bool,
        is_error: bool = False,
    ):
        if is_error:
            speaker_color = colors.MUTED
        elif is_user:
            speaker_color = colors.EJ6_GREEN
        else:
            speaker_color = colors.MAJIN_PURPLE

        return ft.Container(
            padding=12,
            border_radius=14,
            bgcolor=colors.BG,
            content=ft.Column(
                [
                    ft.Text(
                        speaker,
                        size=11,
                        color=speaker_color,
                    ),
                    ft.Text(
                        text,
                        size=14,
                        color=colors.TEXT,
                        selectable=True,
                    ),
                ],
                spacing=4,
            ),
        )

    def thinking_bubble(self):
        return ft.Container(
            padding=12,
            border_radius=14,
            bgcolor=colors.BG,
            content=ft.Column(
                [
                    ft.Text(
                        self.worker_name,
                        size=11,
                        color=colors.MAJIN_PURPLE,
                    ),
                    ft.Row(
                        [
                            ft.ProgressRing(
                                width=16,
                                height=16,
                                stroke_width=2,
                            ),
                            ft.Text(
                                "Inspecting..." if self.worker_name == "Builder"
                                else "Thinking...",
                                size=14,
                                color=colors.MUTED,
                            ),
                        ],
                        spacing=8,
                    ),
                ],
                spacing=4,
            ),
        )

    @staticmethod
    def first_useful_line(text: str, maximum: int = 140):
        for raw_line in text.splitlines():
            line = raw_line.strip().lstrip("-*# ")

            if line:
                return line[:maximum]

        return text.strip()[:maximum] or "Continue the current work."