import os
import webbrowser
import flet as ft

from projects.registry import PROJECTS
from projects.brains import (
    read_text_file,
    write_text_file,
    get_project_sessions,
    get_project_stats,
)
from memory.sessions import start_session
from components.card import card
from components.button import primary_button, quiet_button
from themes import colors, spacing


def brain_screen(project_id, on_back, on_message, on_continue):
    project = next((p for p in PROJECTS if p["id"] == project_id), None)

    if not project:
        return ft.Column(
            [
                quiet_button("Back to Workshop", icon=ft.Icons.ARROW_BACK, on_click=lambda e: on_back()),
                card(
                    ft.Column(
                        [
                            ft.Text("Place not found", size=24, weight=ft.FontWeight.BOLD),
                            ft.Text("This brain has no linked Place.", color=colors.MUTED),
                        ],
                        spacing=spacing.SMALL_GAP,
                    ),
                    accent="purple",
                ),
            ],
            spacing=spacing.GAP,
        )

    notes = read_text_file(project_id, "notes.md", "# Notes\n")
    dreams = read_text_file(project_id, "dreams.md", "# Dreams\n")
    activity = read_text_file(project_id, "activity.md", "# Activity\n")
    sessions = get_project_sessions(project_id, limit=5)
    stats = get_project_stats(project_id)

    feedback = ft.Text("", size=13, color=colors.EJ6_GREEN)

    notes_input = ft.TextField(
        value=notes,
        multiline=True,
        min_lines=6,
        max_lines=12,
        border_color=colors.EJ6_GREEN,
        focused_border_color=colors.MAJIN_PURPLE,
    )

    def save_notes(e):
        write_text_file(project_id, "notes.md", notes_input.value)
        feedback.value = "Notes saved. Future Yuri has it."
        feedback.update()
        on_message("Notes saved.")

    def continue_place(e):
        start_session(project)
        on_continue()

    return ft.Column(
        [
            quiet_button("Back to Workshop", icon=ft.Icons.ARROW_BACK, on_click=lambda e: on_back()),

            card(
                ft.Column(
                    [
                        ft.Text(f"{project['icon']}  {project['name']}", size=30, weight=ft.FontWeight.BOLD),
                        ft.Text(project["status"], size=14, color=colors.MUTED),
                        ft.Text(f"Priority {project['priority']:02d} • Momentum {project['momentum']}", size=13, color=colors.MAJIN_PURPLE),
                        primary_button("Continue this Place", icon=ft.Icons.PLAY_ARROW, on_click=continue_place),
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
                                    ft.Text("Brain Stats", size=14, color=colors.EJ6_GREEN),
                                    ft.Text(f"{stats['sessions']} sessions", size=15),
                                    ft.Text(f"{stats['dreams']} dreams", size=15),
                                    ft.Text(f"{stats['activity_entries']} activity entries", size=15),
                                ],
                                spacing=spacing.SMALL_GAP,
                            ),
                            accent="green",
                        ),
                        expand=1,
                    ),
                    ft.Container(
                        card(
                            ft.Column(
                                [
                                    ft.Text("Links", size=14, color=colors.EJ6_GREEN),
                                    ft.Row(
                                        [
                                            quiet_button("Folder", icon=ft.Icons.FOLDER_OPEN, on_click=lambda e: open_folder(project, on_message)),
                                            quiet_button("Website", icon=ft.Icons.LANGUAGE, on_click=lambda e: open_website(project, on_message)),
                                        ],
                                        spacing=spacing.SMALL_GAP,
                                        wrap=True,
                                    ),
                                ],
                                spacing=spacing.SMALL_GAP,
                            ),
                            accent="purple",
                        ),
                        expand=1,
                    ),
                ],
                spacing=spacing.GAP,
            ),

            card(
                ft.Column(
                    [
                        ft.Text("Notes", size=14, color=colors.EJ6_GREEN),
                        ft.Text("What should Future Yuri remember about this Place?", size=12, color=colors.MUTED),
                        notes_input,
                        primary_button("Save notes", icon=ft.Icons.SAVE, on_click=save_notes),
                        feedback,
                    ],
                    spacing=spacing.SMALL_GAP,
                ),
                accent="green",
            ),

            ft.Row(
                [
                    ft.Container(
                        card(
                            ft.Column(
                                [
                                    ft.Text("Recent Sessions", size=14, color=colors.EJ6_GREEN),
                                    *session_items(sessions),
                                ],
                                spacing=spacing.SMALL_GAP,
                            ),
                            accent="purple",
                        ),
                        expand=1,
                    ),
                    ft.Container(
                        card(
                            ft.Column(
                                [
                                    ft.Text("Dreams", size=14, color=colors.EJ6_GREEN),
                                    ft.Text(trim_md(dreams), size=13, color=colors.TEXT, selectable=True),
                                ],
                                spacing=spacing.SMALL_GAP,
                            ),
                            accent="green",
                        ),
                        expand=1,
                    ),
                ],
                spacing=spacing.GAP,
            ),

            card(
                ft.Column(
                    [
                        ft.Text("Activity", size=14, color=colors.EJ6_GREEN),
                        ft.Text(trim_md(activity), size=13, color=colors.TEXT, selectable=True),
                    ],
                    spacing=spacing.SMALL_GAP,
                ),
                accent="purple",
            ),
        ],
        spacing=spacing.GAP,
        scroll=ft.ScrollMode.AUTO,
    )


def session_items(sessions):
    if not sessions:
        return [ft.Text("No sessions yet.", size=13, color=colors.MUTED)]

    items = []

    for session in sessions:
        items.append(
            ft.Column(
                [
                    ft.Text(session.get("started", "Unknown"), size=12, color=colors.MAJIN_PURPLE),
                    ft.Text(
                        session.get("goal")
                        or session.get("summary")
                        or session.get("notes")
                        or "Session captured.",
                        size=13,
                        color=colors.TEXT,
                    ),
                ],
                spacing=2,
            )
        )

    return items


def trim_md(text, max_chars=900):
    if not text.strip():
        return "Nothing here yet."

    cleaned = text.replace("# Dreams", "").replace("# Notes", "").replace("# Activity", "").strip()

    if not cleaned:
        return "Nothing here yet."

    if len(cleaned) > max_chars:
        return cleaned[:max_chars] + "..."

    return cleaned


def open_folder(project, on_message):
    path = project["path"]

    if not os.path.exists(path):
        on_message(f"Path not found: {path}")
        return

    os.startfile(path)
    on_message(f"Opened {project['name']} folder.")


def open_website(project, on_message):
    url = project.get("url")

    if not url:
        on_message(f"No website linked for {project['name']}.")
        return

    webbrowser.open(url)
    on_message(f"Opened {project['name']} website.")