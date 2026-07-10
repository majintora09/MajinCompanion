from memory.sessions import get_active_session, get_last_session


def campfire_message():
    active = get_active_session()
    last = get_last_session()

    if active:
        return f"{active['project_name']} is still open. Let's pick it back up."

    if last:
        return f"We left off in {last['project_name']}."

    return "Nothing waiting yet. The Workshop is ready."