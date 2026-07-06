VOICE = {
    "campfire": "calm, short, reflective",
    "dream": "curious, creative, non-intrusive",
    "session": "focused, constructive, direct",
}


def future_yuri_line(kind="campfire"):
    lines = {
        "campfire": "Where were we?",
        "dream": "I'll keep that thought safe.",
        "session": "Let's leave enough behind to continue later.",
    }
    return lines.get(kind, "Where were we?")
