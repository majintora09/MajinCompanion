class Conversation:
    def __init__(self, messages=None):
        self.messages = list(messages or [])

    def add_user(self, text: str):
        self.messages.append(
            {
                "role": "user",
                "content": text.strip(),
            }
        )

    def add_ai(self, text: str):
        self.messages.append(
            {
                "role": "assistant",
                "content": text.strip(),
            }
        )

    def export(self):
        return list(self.messages)