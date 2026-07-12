import os
import subprocess
import webbrowser

import flet as ft

from ai.builder import BuilderWorker
from ai.chair import ask_future_yuri
from components.button import primary_button, quiet_button
from components.chat_panel import ChatPanel
from components.section import section
from memory.sessions import start_session
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


def workbench_screen(
    page,
    project_id,
    on_back,
    on_message,
    on_open_session,
):
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

    future_conversation = []
    builder_conversation = []
    builder_worker = BuilderWorker()

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

    def save_notes_clicked(e):
        set_notes(project_id, notes_input.value or "")
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

    def ask_from_chair(message):
        answer = ask_future_yuri(
            place_id=project_id,
            user_message=message,
            conversation=future_conversation,
        )

        future_conversation.extend(
            [
                {
                    "role": "user",
                    "content": message,
                },
                {
                    "role": "assistant",
                    "content": answer,
                },
            ]
        )

        return answer

    def ask_builder(message):
        answer = builder_worker.ask(
            place_id=project_id,
            message=message,
            external_history=builder_conversation,
        )

        builder_conversation.extend(
            [
                {
                    "role": "user",
                    "content": message,
                },
                {
                    "role": "assistant",
                    "content": answer,
                },
            ]
        )

        return answer

    def add_chair_answer_to_notes(answer):
        append_notes(project_id, answer)
        notes_input.value = get_notes(project_id)

        if notes_input.page:
            notes_input.update()

    chair = ChatPanel(
        page=page,
        worker_name="Future Yuri",
        panel_title="The Chair",
        panel_subtitle="Future Yuri already has the context.",
        intro_message=future_yuri_message(project_id),
        input_hint="What's blocking us?",
        ask_callback=ask_from_chair,
        save_discovery_callback=lambda answer: add_discovery(
            project_id,
            answer,
        ),
        add_notes_callback=add_chair_answer_to_notes,
        update_mission_callback=lambda mission: set_mission(
            project_id,
            mission,
        ),
        show_memory_actions=True,
    )

    builder = ChatPanel(
        page=page,
        worker_name="Builder",
        panel_title="Builder Preview",
        panel_subtitle="Read-only access to this Place's source files.",
        intro_message=(
            "I can inspect this Place's real files and draft an "
            "implementation plan. I cannot edit anything yet."
        ),
        input_hint="What should Builder inspect or plan?",
        ask_callback=ask_builder,
        show_memory_actions=False,
    )

    def open_chair(e):
        builder.hide()
        chair.toggle()

    def open_builder(e):
        chair.hide()
        builder.toggle()

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
                        on_click=lambda e: open_folder(
                            project,
                            feedback,
                        ),
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
                        on_click=lambda e: open_vscode(
                            project,
                            feedback,
                        ),
                    ),

                    ft.TextButton(
                        "🪑 Take a seat",
                        on_click=open_chair,
                    ),

                    ft.TextButton(
                        "🛠 Builder Preview",
                        on_click=open_builder,
                    ),
                ],
                spacing=spacing.SMALL_GAP,
                wrap=True,
            ),

            feedback,

            ft.Divider(
                height=30,
                color=colors.BORDER,
            ),

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
            chair.control,
            builder.control,
        ],
        spacing=spacing.GAP,
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True,
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
    project_path = project["path"]

    if not os.path.exists(project_path):
        feedback.value = f"Path not found: {project_path}"
        feedback.update()
        return

    executable = next(
        (
            candidate
            for candidate in VS_CODE_PATHS
            if os.path.exists(candidate)
        ),
        None,
    )

    if not executable:
        feedback.value = "VS Code wasn't found."
        feedback.update()
        return

    subprocess.Popen(
        [
            executable,
            project_path,
        ]
    )

    feedback.value = "VS Code opened."
    feedback.update()