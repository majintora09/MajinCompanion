from pathlib import Path

from ai.builder.repository import build_repository_context
from ai.shared.capabilities import Capability
from ai.shared.memory import get_place_memory
from ai.shared.worker import AIWorker


HERE = Path(__file__).resolve().parent
PROMPT_FILE = HERE / "prompt.md"


class BuilderWorker(AIWorker):
    name = "Builder"
    role = "read_only_builder"

    capabilities = [
        Capability.REASON,
        Capability.PLAN,
        Capability.READ_FILES,
        Capability.GENERATE_CODE,
    ]

    def system_prompt(self) -> str:
        return self.read_prompt_file(PROMPT_FILE)

    def build_context(self, place_id: str) -> str:
        return get_place_memory(place_id)

    def ask(
        self,
        place_id: str,
        message: str,
        external_history=None,
    ) -> str:
        place_memory = get_place_memory(place_id)

        repository_context = build_repository_context(
            project_id=place_id,
            request=message,
        )

        conversation = self.conversation_for(place_id)

        if external_history is not None:
            from ai.shared.conversation import Conversation

            conversation = Conversation(external_history)

        messages = [
            {
                "role": "system",
                "content": self.system_prompt(),
            },
            {
                "role": "system",
                "content": (
                    "PLACE MEMORY\n\n"
                    f"{place_memory}"
                ),
            },
            {
                "role": "system",
                "content": (
                    "READ-ONLY REPOSITORY CONTEXT\n\n"
                    f"{repository_context}"
                ),
            },
            *conversation.export(),
            {
                "role": "user",
                "content": message.strip(),
            },
        ]

        from ai.shared.client import chat_with_ollama

        answer = chat_with_ollama(
            messages=messages,
            model=self.model,
        )

        if external_history is None:
            conversation.add_user(message)
            conversation.add_ai(answer)

        return answer