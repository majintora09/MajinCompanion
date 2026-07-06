import flet as ft
from datetime import datetime

from themes import colors, typography
from core.version import VERSION, CODENAME


def get_greeting():
    hour = datetime.now().hour

    if hour < 12:
        return "Morning."
    if hour < 18:
        return "Afternoon."
    return "Evening."


def hero():
    return ft.Column(
        [
            ft.Text("🔥", size=44),
            ft.Text(get_greeting(), size=typography.TITLE, weight=ft.FontWeight.BOLD),
            ft.Text("Where were we?", size=typography.BODY, color=colors.MUTED),
            ft.Text(f"v{VERSION} — {CODENAME}", size=typography.SMALL, color=colors.MAJIN_PURPLE),
        ],
        spacing=8,
    )