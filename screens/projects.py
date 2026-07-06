import flet as ft

from projects.registry import PROJECTS
from components.button import quiet_button
from themes import colors, spacing


def workshop(on_back, on_message, on_continue, on_open_brain, on_open_workbench):
    sorted_projects = sorted(PROJECTS, key=lambda p: p["priority"])

    place_tiles = [
        place_tile(project, on_open_workbench)
        for project in sorted_projects
    ]

    return ft.Column(
        [
            quiet_button("Back to Campfire", icon=ft.Icons.ARROW_BACK, on_click=lambda e: on_back()),

            ft.Text("Workshop", size=34, weight=ft.FontWeight.BOLD),
            ft.Text("Choose a Place. Future Yuri remembers the rest.", size=14, color=colors.MUTED),

            ft.Container(height=10),

            ft.Row(
                place_tiles,
                spacing=spacing.GAP,
                wrap=True,
            ),
        ],
        spacing=spacing.GAP,
        scroll=ft.ScrollMode.AUTO,
    )


def place_tile(project, on_open_workbench):
    accent = colors.EJ6_GREEN if project["color"] == "green" else colors.MAJIN_PURPLE

    return ft.Container(
        width=310,
        height=170,
        padding=22,
        border_radius=18,
        bgcolor=colors.CARD,
        border=None,
        on_click=lambda e, p=project: on_open_workbench(p["id"]),
        content=ft.Column(
            [
                ft.Text(project["icon"], size=34),
                ft.Text(project.get("nickname", project["name"]), size=24, weight=ft.FontWeight.BOLD),
                ft.Text(project["status"], size=13, color=colors.MUTED),
                ft.Text(
                    f"Priority {project['priority']:02d} • Momentum {project['momentum']}",
                    size=12,
                    color=accent,
                ),
            ],
            spacing=6,
        ),
    )