import os
import webbrowser
import flet as ft

from projects.registry import PROJECTS
from components.card import card
from components.button import quiet_button, primary_button
from themes import colors, spacing
from memory.sessions import start_session


def workshop(on_back, on_message, on_continue, on_open_brain):
    project_cards = []

    sorted_projects = sorted(PROJECTS, key=lambda p: p["priority"])

    for project in sorted_projects:
        buttons = [
            primary_button(
                "Open Brain",
                icon=ft.Icons.PSYCHOLOGY,
                on_click=lambda e, p=project: on_open_brain(p["id"]),
            ),
            quiet_button(
                "Continue",
                icon=ft.Icons.PLAY_ARROW,
                on_click=lambda e, p=project: continue_project(p, on_message, on_continue),
            ),
            quiet_button(
                "Folder",
                icon=ft.Icons.FOLDER_OPEN,
                on_click=lambda e, p=project: open_project_folder(p, on_message),
            ),
        ]

        if project.get("url"):
            buttons.append(
                quiet_button(
                    "Website",
                    icon=ft.Icons.LANGUAGE,
                    on_click=lambda e, p=project: open_project_website(p, on_message),
                )
            )

        project_cards.append(
            card(
                ft.Column(
                    [
                        ft.Text(
                            f"{project['icon']}  {project['name']}",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(project["status"], size=14, color=colors.MUTED),
                        ft.Text(f"Priority: {project['priority']:02d}   Momentum: {project['momentum']}", size=12, color=colors.MAJIN_PURPLE),
                        ft.Row(buttons, spacing=spacing.SMALL_GAP, wrap=True),
                    ],
                    spacing=spacing.SMALL_GAP,
                ),
                accent=project["color"],
            )
        )

    return ft.Column(
        [
            quiet_button("Back to Campfire", icon=ft.Icons.ARROW_BACK, on_click=lambda e: on_back()),
            ft.Text("Workshop", size=30, weight=ft.FontWeight.BOLD),
            ft.Text("Choose a Place. Future Yuri remembers the rest.", size=14, color=colors.MUTED),
            *project_cards,
        ],
        spacing=spacing.GAP,
        scroll=ft.ScrollMode.AUTO,
    )


def continue_project(project, on_message, on_continue):
    start_session(project)
    on_message(f"Continuing {project['name']}.")
    on_continue()


def open_project_folder(project, on_message):
    path = project["path"]

    if not os.path.exists(path):
        on_message(f"Path not found: {path}")
        return

    os.startfile(path)
    on_message(f"Opened {project['name']} folder.")


def open_project_website(project, on_message):
    url = project.get("url")

    if not url:
        on_message(f"No website linked for {project['name']}.")
        return

    webbrowser.open(url)
    on_message(f"Opened {project['name']} website.")