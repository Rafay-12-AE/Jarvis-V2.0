import threading
import time

from core.voice import speak, listen
from core.wake_word import wait_for_wake_word

from core.logger import write_log
from core.error_handler import safe_execute
from core.config import get_setting

from core.ui_state import (
    set_ui_state,
    request_shutdown
)

from brain.command_router import process_command

from ui.jarvis_ui import run_ui


# ============================================================
# JARVIS BACKEND
# ============================================================

def run_jarvis():

    # ---------------- START ----------------

    assistant_name = get_setting(
        "assistant_name"
    )

    if assistant_name:

        startup_message = (
            f"{assistant_name} is online"
        )

    else:

        startup_message = (
            "Jarvis is online"
        )


    write_log(
        "Jarvis started"
    )

    speak(
        startup_message
    )


    # ---------------- STATE ----------------

    jarvis_awake = False

    set_ui_state(
        "SLEEPING"
    )


    # ========================================================
    # MAIN LOOP
    # ========================================================

    while True:

        try:

            # ================================================
            # SLEEPING MODE
            # ================================================

            if not jarvis_awake:

                set_ui_state(
                    "SLEEPING"
                )

                wait_for_wake_word()

                jarvis_awake = True

                write_log(
                    "Jarvis awakened"
                )

                speak(
                    "Yes?"
                )

                set_ui_state(
                    "LISTENING"
                )

                continue


            # ================================================
            # ACTIVE MODE
            # ================================================

            set_ui_state(
                "LISTENING"
            )

            command = listen()

            if not command:

                continue


            command_lower = (
                command
                .lower()
                .strip()
            )


            write_log(
                f"Command received: {command}"
            )


            # ================================================
            # GO TO SLEEP
            # ================================================

            if command_lower in [

                "go to sleep",
                "go back to sleep",
                "sleep",
                "sleep jarvis",
                "jarvis go to sleep",
                "stand by",
                "standby"

            ]:

                speak(
                    "Going to sleep"
                )

                write_log(
                    "Jarvis entered sleep mode"
                )

                jarvis_awake = False

                set_ui_state(
                    "SLEEPING"
                )

                time.sleep(
                    1.5
                )

                continue


            # ================================================
            # PROCESS COMMAND
            # ================================================

            set_ui_state(
                "THINKING"
            )

            result = safe_execute(
                process_command,
                command
            )


            # ================================================
            # FULL SHUTDOWN
            # ================================================

            if result == "exit":

                write_log(
                    "Jarvis shutting down"
                )

                request_shutdown()

                break


            # ================================================
            # READY FOR NEXT COMMAND
            # ================================================

            set_ui_state(
                "LISTENING"
            )


        except Exception as error:

            write_log(
                f"Main loop error: {error}"
            )

            if jarvis_awake:

                set_ui_state(
                    "LISTENING"
                )

            else:

                set_ui_state(
                    "SLEEPING"
                )


# ============================================================
# START JARVIS WORKER THREAD
# ============================================================

jarvis_thread = threading.Thread(
    target=run_jarvis,
    daemon=True
)

jarvis_thread.start()


# ============================================================
# RUN GRAPHICAL UI
# ============================================================

# Pygame stays on the main thread.
# Jarvis voice / AI / wake-word processing runs independently
# in the worker thread above.

run_ui()