import os
import subprocess
import webbrowser

import flet as ft

from ai.chair import ask_future_yuri
from ai.client import OllamaError
from components.button import primary_button, quiet_button
from components.section import section
from memory.sessions import get_active_session, start_session
from places.brain import (
    add_discovery,
    add_dream,
    append_notes,
    get_history,
    get_notes,
    get_recent_discoveries,
    get_recent_dreams,
    set_mission,
    set_notes,
)
from places.future import future_yuri_message
from projects.registry import PROJECTS
from themes import colors, spacing


VS_CODE_PATHS = [
    r"C:\Users\Tora\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    r"C:\Program Files\Microsoft VS Code\Code.exe",
    r"C:\Program Files (x86)\Microsoft VS Code\Code.exe",
]


def workbench_screen(project_id, on_back, on_message, on_open_session):
    project = next(
        (item for item in PROJECTS if item["id"] == project_id),
        None,
    )

    if not project:
        return ft.Column(
            [
                quiet_button(
                    "Back",
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda e: on_back(),
                ),
                ft.Text("Place not found.", size=24),
            ],
            spacing=spacing.GAP,
        )

    conversation: list[dict[str, str]] = []
    latest_answer = {"text": ""}

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

    feedback = ft.Text(
        "",
        size=13,
        color=colors.EJ6_GREEN,
    )

    chair_messages = ft.Column(
        [
            message_bubble(
                "Future Yuri",
                future_yuri_message(project_id),
                is_user=False,
            )
        ],
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
    )

    chair_input = ft.TextField(
        hint_text="What's blocking us?",
        multiline=True,
        min_lines=1,
        max_lines=5,
        border_color=colors.MAJIN_PURPLE,
        focused_border_color=colors.EJ6_GREEN,
        expand=True,
    )

    chair_status = ft.Text(
        "Local • qwen3:8b",
        size=11,
        color=colors.MUTED,
    )

    memory_actions = ft.Row(
        visible=False,
        wrap=True,
        spacing=spacing.SMALL_GAP,
    )

    chair_panel = ft.Container(
        visible=False,
        width=470,
        padding=20,
        border_radius=18,
        bgcolor=colors.CARD,
    )

    chair_toggle_text = ft.Text("🪑 Take a seat")

    def save_notes_clicked(e):
        set_notes(project_id, notes_input.value)
        feedback.value = "Notes saved. Future Yuri has it."
        feedback.update()

    def save_dream_clicked(e):
        text = dream_input.value or ""

        if not text.strip():
            feedback.value = "Drop an idea first."
            feedback.update()
            return

        add_dream(project_id, text)
        dream_input.value = ""
        dream_input.update()

        feedback.value = "Dream saved to this Place."
        feedback.update()

    def save_discovery_clicked(e):
        text = discovery_input.value or ""

        if not text.strip():
            feedback.value = "Write the discovery first."
            feedback.update()
            return

        add_discovery(project_id, text)
        discovery_input.value = ""
        discovery_input.update()

        feedback.value = "Discovery saved. This one matters."
        feedback.update()

    def continue_place(e):
        start_session(project)
        on_open_session()

    def toggle_chair(e):
        chair_panel.visible = not chair_panel.visible
        chair_toggle_text.value = (
            "Leave the chair"
            if chair_panel.visible
            else "🪑 Take a seat"
        )
        chair_toggle_text.update()
        chair_panel.update()

    def send_to_future_yuri(e):
        user_text = chair_input.value or ""

        if not user_text.strip():
            chair_status.value = "Say something first."
            chair_status.update()
            return

        clean_text = user_text.strip()

        chair_messages.controls.append(
            message_bubble("You", clean_text, is_user=True)
        )
        chair_input.value = ""
        chair_input.update()

        chair_status.value = "Thinking with this Place's context..."
        chair_status.update()
        chair_messages.update()

        try:
            answer = ask_future_yuri(
                place_id=project_id,
                user_message=clean_text,
                conversation=conversation,
            )

        except OllamaError as error:
            chair_messages.controls.append(
                message_bubble(
                    "Future Yuri",
                    str(error),
                    is_user=False,
                    is_error=True,
                )
            )
            chair_status.value = "Connection failed."
            chair_messages.update()
            chair_status.update()
            return

        conversation.extend(
            [
                {
                    "role": "user",
                    "content": clean_text,
                },
                {
                    "role": "assistant",
                    "content": answer,
                },
            ]
        )

        latest_answer["text"] = answer

        chair_messages.controls.append(
            message_bubble(
                "Future Yuri",
                answer,
                is_user=False,
            )
        )

        memory_actions.controls = build_memory_actions()
        memory_actions.visible = True

        chair_status.value = "What should I remember?"
        chair_messages.update()
        memory_actions.update()
        chair_status.update()

    def save_answer_as_discovery(e):
        answer = latest_answer["text"]

        if not answer:
            return

        add_discovery(project_id, answer)
        chair_status.value = "Saved as a Discovery."
        chair_status.update()

    def add_answer_to_notes(e):
        answer = latest_answer["text"]

        if not answer:
            return

        append_notes(project_id, answer)
        notes_input.value = get_notes(project_id)
        notes_input.update()

        chair_status.value = "Added to Notes."
        chair_status.update()

    def use_answer_as_mission(e):
        answer = latest_answer["text"]

        if not answer:
            return

        mission = first_useful_line(answer)
        set_mission(project_id, mission)

        chair_status.value = f"Mission updated: {mission}"
        chair_status.update()

    def dismiss_memory_actions(e):
        memory_actions.visible = False
        memory_actions.update()

        chair_status.value = "Nothing saved. That's okay."
        chair_status.update()

    def build_memory_actions():
        return [
            quiet_button(
                "Nothing",
                icon=ft.Icons.CLOSE,
                on_click=dismiss_memory_actions,
            ),
            quiet_button(
                "Save discovery",
                icon=ft.Icons.LIGHTBULB,
                on_click=save_answer_as_discovery,
            ),
            quiet_button(
                "Add to notes",
                icon=ft.Icons.NOTE_ADD,
                on_click=add_answer_to_notes,
            ),
            quiet_button(
                "Update mission",
                icon=ft.Icons.FLAG,
                on_click=use_answer_as_mission,
            ),
        ]

    chair_panel.content = ft.Column(
        [
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(
                                "The Chair",
                                size=22,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Future Yuri already has the context.",
                                size=12,
                                color=colors.MUTED,
                            ),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        tooltip="Leave the chair",
                        on_click=toggle_chair,
                    ),
                ]
            ),
            ft.Divider(color=colors.BORDER),
            ft.Container(
                content=chair_messages,
                height=500,
            ),
            ft.Divider(color=colors.BORDER),
            ft.Row(
                [
                    chair_input,
                    ft.IconButton(
                        icon=ft.Icons.SEND,
                        tooltip="Send",
                        on_click=send_to_future_yuri,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.END,
            ),
            chair_status,
            memory_actions,
        ],
        spacing=12,
    )

    workbench_content = ft.Column(
        [
            quiet_button(
                "Back to Workshop",
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda e: on_back(),
            ),
            ft.Text(
                f"{project['icon']}  "
                f"{project.get('nickname', project['name'])}",
                size=38,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Text(
                project["status"],
                size=14,
                color=colors.MUTED,
            ),
            ft.Text(
                "Let's pick it back up.",
                size=17,
                color=colors.TEXT,
            ),
            ft.Text(
                future_yuri_message(project_id),
                size=14,
                color=colors.MAJIN_PURPLE,
            ),
            ft.Row(
                [
                    primary_button(
                        "Continue",
                        icon=ft.Icons.PLAY_ARROW,
                        on_click=continue_place,
                    ),
                    quiet_button(
                        "Folder",
                        icon=ft.Icons.FOLDER_OPEN,
                        on_click=lambda e: open_folder(project, feedback),
                    ),
                    quiet_button(
                        "Website",
                        icon=ft.Icons.LANGUAGE,
                        on_click=lambda e: open_url(
                            project.get("url"),
                            "website",
                            feedback,
                        ),
                    ),
                    quiet_button(
                        "GitHub",
                        icon=ft.Icons.CODE,
                        on_click=lambda e: open_url(
                            project.get("github"),
                            "GitHub",
                            feedback,
                        ),
                    ),
                    quiet_button(
                        "VS Code",
                        icon=ft.Icons.TERMINAL,
                        on_click=lambda e: open_vscode(project, feedback),
                    ),
                    ft.TextButton(
                        content=chair_toggle_text,
                        on_click=toggle_chair,
                    ),
                ],
                spacing=spacing.SMALL_GAP,
                wrap=True,
            ),
            feedback,
            ft.Divider(height=30, color=colors.BORDER),
            ft.Row(
                [
                    ft.Container(
                        section(
                            "Live Notes",
                            ft.Column(
                                [
                                    notes_input,
                                    primary_button(
                                        "Save notes",
                                        icon=ft.Icons.SAVE,
                                        on_click=save_notes_clicked,
                                    ),
                                ],
                                spacing=spacing.SMALL_GAP,
                            ),
                            subtitle=(
                                "What should Future Yuri remember here?"
                            ),
                            accent="green",
                        ),
                        expand=2,
                    ),
                    ft.Container(
                        ft.Column(
                            [
                                section(
                                    "Quick Dream",
                                    ft.Column(
                                        [
                                            dream_input,
                                            primary_button(
                                                "Save dream",
                                                icon=ft.Icons.AUTO_AWESOME,
                                                on_click=save_dream_clicked,
                                            ),
                                        ],
                                        spacing=spacing.SMALL_GAP,
                                    ),
                                    subtitle=(
                                        "Ideas that are not actionable yet."
                                    ),
                                    accent="purple",
                                ),
                                section(
                                    "Discovery",
                                    ft.Column(
                                        [
                                            discovery_input,
                                            primary_button(
                                                "Save discovery",
                                                icon=ft.Icons.LIGHTBULB,
                                                on_click=save_discovery_clicked,
                                            ),
                                        ],
                                        spacing=spacing.SMALL_GAP,
                                    ),
                                    subtitle=(
                                        "What did we learn that "
                                        "Future Yuri will need?"
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
                    ft.Container(
                        memory_section(
                            "Recent Discoveries",
                            get_recent_discoveries(project_id),
                            "purple",
                        ),
                        expand=1,
                    ),
                    ft.Container(
                        memory_section(
                            "Recent Dreams",
                            get_recent_dreams(project_id),
                            "green",
                        ),
                        expand=1,
                    ),
                ],
                spacing=spacing.GAP,
            ),
            memory_section(
                "Recent History",
                get_history(project_id),
                "purple",
            ),
        ],
        spacing=spacing.GAP,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    return ft.Row(
        [
            ft.Container(
                content=workbench_content,
                expand=True,
            ),
            chair_panel,
        ],
        spacing=spacing.GAP,
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True,
    )


def message_bubble(
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


def memory_section(title, items, accent):
    if not items:
        rows = [
            ft.Text(
                "Nothing here yet.",
                size=13,
                color=colors.MUTED,
            )
        ]
    else:
        rows = [
            ft.Column(
                [
                    ft.Text(
                        item.get("time", ""),
                        size=11,
                        color=colors.MAJIN_PURPLE,
                    ),
                    ft.Text(
                        item.get("text", ""),
                        size=13,
                        color=colors.TEXT,
                    ),
                ],
                spacing=2,
            )
            for item in items
        ]

    return section(
        title,
        ft.Column(
            rows,
            spacing=spacing.SMALL_GAP,
        ),
        accent=accent,
    )


def first_useful_line(text: str, maximum: int = 140) -> str:
    for raw_line in text.splitlines():
        line = raw_line.strip().lstrip("-*# ")

        if line:
            return line[:maximum]

    return text.strip()[:maximum] or "Continue the current work."


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

    executable = next(
        (path for path in VS_CODE_PATHS if os.path.exists(path)),
        None,
    )

    if not executable:
        feedback.value = "VS Code wasn't found."
        feedback.update()
        return

    subprocess.Popen([executable, path])
    feedback.value = "VS Code opened."
    feedback.update()