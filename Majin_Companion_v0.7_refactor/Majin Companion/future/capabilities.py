CAPABILITIES = {
    "can_remember": True,
    "can_restore_context": True,
    "can_reflect": False,
    "can_suggest": False,
    "can_speak": False,
    "can_open_workspaces": False,
}


def capability_status():
    return CAPABILITIES.copy()
