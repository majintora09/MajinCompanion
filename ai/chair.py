from ai.future_yuri import FutureYuriWorker


_future_yuri = FutureYuriWorker()


def ask_future_yuri(
    place_id: str,
    user_message: str,
    conversation: list[dict[str, str]],
) -> str:
    return _future_yuri.ask(
        place_id=place_id,
        message=user_message,
        external_history=conversation,
    )