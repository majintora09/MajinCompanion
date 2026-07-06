import os
import subprocess
import webbrowser
import flet as ft

from projects.registry import PROJECTS
from places.brain import (
    get_notes,
    set_notes,
    add_dream,
    add_discovery,
    get_recent_dreams,
    get_recent_discoveries,
    get_history,
)
from places.future import future_yuri_message
from memory.sessions import start_session, get_active_session
from components.card import card
from components.button import primary_button, quiet_button
from themes import colors, spacing


VS_CODE_PATHS = [
    r"C:\Users\Tora\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    r"C:\Program Files\Microsoft VS Code\Code.exe",
    r"C:\Program Files (x86)\Microsoft VS Code\Code.exe",
]


def workbench_screen(project_id, on_back, on_message, on_open_session):
    project = next((p for p in PROJECTS if p["id"] == project_id), None)

    if not project:
        return ft.Column(
            [
                quiet_button("Back", icon=ft.Icons.ARROW_BACK, on_click=lambda e: on_back()),
                ft.Text("Place not found.", size=24),
            ],
            spacing=spacing.GAP,
        )

    notes_input = ft.TextField(
        value=get_notes(project_id),
        multiline=True,
        min_lines=8,
        max_lines=14,
        border_color=colors.EJ6_GREEN,
        focused_border_color=colors.MAJIN_PURPLE,
    )

    dream_input = ft.TextField(
        hint_text="Dream for this Place...",
        multiline=True,
        min_lines=2,
        max_lines=4,
        border_color=colors.MAJIN_PURPLE,
        focused_border_color=colors.EJ6_GREEN,
    )

    discovery_input = ft.TextField(
        hint_text="What did we learn here?",
        multiline=True,
        min_lines=2,
        max_lines=4,
        border_color=colors.EJ6_GREEN,
        focused_border_color=colors.MAJIN_PURPLE,
    )

    feedback = ft.Text("", size=13, color=colors.EJ6_GREEN)

    def save_notes(e):
        set_notes(project_id, notes_input.value)
        feedback.value = "Notes saved. Future Yuri has it."
        feedback.update()

    def save_dream_clicked(e):
        if not dream_input.value or not dream_input.value.strip():
            feedback.value = "Drop an idea first."
            feedback.update()
            return

        add_dream(project_id, dream_input.value)
        dream_input.value = ""
        dream_input.update()
        feedback.value = "Dream saved to this Place."
        feedback.update()

    def save_discovery_clicked(e):
        if not discovery_input.value or not discovery_input.value.strip():
            feedback.value = "Write the discovery first."
            feedback.update()
            return

        add_discovery(project_id, discovery_input.value)
        discovery_input.value = ""
        discovery_input.update()
        feedback.value = "Discovery saved. This one matters."
        feedback.update()

    def continue_place(e):
        start_session(project)
        on_open_session()

    return ft.Column(
        [
            quiet_button("Back to Workshop", icon=ft.Icons.ARROW_BACK, on_click=lambda e: on_back()),

            card(
                ft.Column(
                    [
                        ft.Text(f"{project['icon']}  {project.get('nickname', project['name'])}", size=34, weight=ft.FontWeight.BOLD),
                        ft.Text(project["status"], size=14, color=colors.MUTED),
                        ft.Text("Let's pick it back up.", size=16, color=colors.TEXT),
                        ft.Text(future_yuri_message(project_id), size=14, color=colors.MAJIN_PURPLE),
                        ft.Row(
                            [
                                primary_button("Continue", icon=ft.Icons.PLAY_ARROW, on_click=continue_place),
                                quiet_button("Folder", icon=ft.Icons.FOLDER_OPEN, on_click=lambda e: open_folder(project, feedback)),
                                quiet_button("Website", icon=ft.Icons.LANGUAGE, on_click=lambda e: open_url(project.get("url"), "website", feedback)),
                                quiet_button("GitHub", icon=ft.Icons.CODE, on_click=lambda e: open_url(project.get("github"), "GitHub", feedback)),
                                quiet_button("VS Code", icon=ft.Icons.TERMINAL, on_click=lambda e: open_vscode(project, feedback)),
                            ],
                            spacing=spacing.SMALL_GAP,
                            wrap=True,
                        ),
                        feedback,
                    ],
                    spacing=spacing.SMALL_GAP,
                ),
                accent=project["color"],
            ),

            ft.Row(
                [
                    ft.Container(
                        card(
                            ft.Column(
                                [
                                    ft.Text("Live Notes", size=14, color=colors.EJ6_GREEN),
                                    ft.Text("What should Future Yuri remember here?", size=12, color=colors.MUTED),
                                    notes_input,
                                    primary_button("Save notes", icon=ft.Icons.SAVE, on_click=save_notes),
                                ],
                                spacing=spacing.SMALL_GAP,
                            ),
                            accent="green",
                        ),
                        expand=2,
                    ),
                    ft.Container(
                        ft.Column(
                            [
                                card(
                                    ft.Column(
                                        [
                                            ft.Text("Quick Dream", size=14, color=colors.EJ6_GREEN),
                                            ft.Text("Ideas that are not actionable yet.", size=12, color=colors.MUTED),
                                            dream_input,
                                            primary_button("Save dream", icon=ft.Icons.AUTO_AWESOME, on_click=save_dream_clicked),
                                        ],
                                        spacing=spacing.SMALL_GAP,
                                    ),
                                    accent="purple",
                                ),
                                card(
                                    ft.Column(
                                        [
                                            ft.Text("Discovery", size=14, color=colors.EJ6_GREEN),
                                            ft.Text("What did we learn that Future Yuri will need?", size=12, color=colors.MUTED),
                                            discovery_input,
                                            primary_button("Save discovery", icon=ft.Icons.LIGHTBULB, on_click=save_discovery_clicked),
                                        ],
                                        spacing=spacing.SMALL_GAP,
                                    ),
                                    accent="green",
                                ),
                            ],
                            spacing=spacing.GAP,
                        ),
                        expand=1,
                    ),
                ],
                spacing=spacing.GAP,
            ),

            ft.Row(
                [
                    ft.Container(memory_list_card("Recent Discoveries", get_recent_discoveries(project_id)), expand=1),
                    ft.Container(memory_list_card("Recent Dreams", get_recent_dreams(project_id)), expand=1),
                ],
                spacing=spacing.GAP,
            ),

            memory_list_card("Recent History", get_history(project_id)),
        ],
        spacing=spacing.GAP,
        scroll=ft.ScrollMode.AUTO,
    )


def memory_list_card(title, items):
    if not items:
        rows = [ft.Text("Nothing here yet.", size=13, color=colors.MUTED)]
    else:
        rows = [
            ft.Column(
                [
                    ft.Text(item.get("time", ""), size=11, color=colors.MAJIN_PURPLE),
                    ft.Text(item.get("text", ""), size=13, color=colors.TEXT),
                ],
                spacing=2,
            )
            for item in items
        ]

    return card(
        ft.Column(
            [
                ft.Text(title, size=14, color=colors.EJ6_GREEN),
                *rows,
            ],
            spacing=spacing.SMALL_GAP,
        ),
        accent="purple",
    )


def open_folder(project, feedback):
    path = project["path"]

    if not os.path.exists(path):
        feedback.value = f"Path not found: {path}"
        feedback.update()
        return

    os.startfile(path)
    feedback.value = "Folder opened."
    feedback.update()


def open_url(url, label, feedback):
    if not url:
        feedback.value = f"No {label} linked yet."
        feedback.update()
        return

    webbrowser.open(url)
    feedback.value = f"{label} opened."
    feedback.update()


def open_vscode(project, feedback):
    path = project["path"]

    if not os.path.exists(path):
        feedback.value = f"Path not found: {path}"
        feedback.update()
        return

    exe = next((p for p in VS_CODE_PATHS if os.path.exists(p)), None)

    if not exe:
        feedback.value = "VS Code not found. Install VS Code or add its path."
        feedback.update()
        return

    subprocess.Popen([exe, path])
    feedback.value = "VS Code opened."
    feedback.update()