import threading


VALID_STATES = {
    "SLEEPING",
    "LISTENING",
    "THINKING",
    "SPEAKING",
}


_current_state = "SLEEPING"
_shutdown_requested = False

_state_lock = threading.Lock()


# ============================================================
# UI STATE
# ============================================================

def set_ui_state(state):

    global _current_state

    state = state.upper().strip()

    if state not in VALID_STATES:
        return

    with _state_lock:
        _current_state = state


def get_ui_state():

    with _state_lock:
        return _current_state


# ============================================================
# SHUTDOWN SIGNAL
# ============================================================

def request_shutdown():

    global _shutdown_requested

    with _state_lock:
        _shutdown_requested = True


def shutdown_requested():

    with _state_lock:
        return _shutdown_requested