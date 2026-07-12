from abc import ABC, abstractmethod
from pathlib import Path

from ai.shared.client import chat_with_ollama
from ai.shared.conversation import Conversation
from ai.shared.models import DEFAULT_MODEL


class AIWorker(ABC):
    name = "Worker"
    role = "worker"
    model = DEFAULT_MODEL
    capabilities = []

    def __init__(self):
        self.conversations: dict[str, Conversation] = {}

    def conversation_for(self, place_id: str) -> Conversation:
        if place_id not in self.conversations:
            self.conversations[place_id] = Conversation()

        return self.conversations[place_id]

    def read_prompt_file(self, prompt_path: Path) -> str:
        if not prompt_path.exists():
            raise FileNotFoundError(
                f"Worker prompt was not found: {prompt_path}"
            )

        return prompt_path.read_text(encoding="utf-8").strip()

    def ask(
        self,
        place_id: str,
        message: str,
        external_history=None,
    ) -> str:
        conversation = self.conversation_for(place_id)

        if external_history is not None:
            conversation = Conversation(external_history)

        messages = [
            {
                "role": "system",
                "content": self.system_prompt(),
            },
            {
                "role": "system",
                "content": self.build_context(place_id),
            },
            *conversation.export(),
            {
                "role": "user",
                "content": message.strip(),
            },
        ]

        answer = chat_with_ollama(
            messages=messages,
            model=self.model,
        )

        if external_history is None:
            conversation.add_user(message)
            conversation.add_ai(answer)

        return answer

    @abstractmethod
    def system_prompt(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def build_context(self, place_id: str) -> str:
        raise NotImplementedError