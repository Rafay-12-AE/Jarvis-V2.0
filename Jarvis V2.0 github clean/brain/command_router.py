from core.voice import speak

from brain.llm import ask_llm
from brain.intent import detect_intent
from brain.web_answer import answer_from_web

from skills.browser import (
    open_youtube,
    open_google,
    open_chrome,
    search_youtube,
    search_google,
    play_on_youtube,
    search_spotify
)

from skills.system import (
    tell_time,
    tell_date,
    open_calculator,
    open_notepad,
    open_file_explorer
)

from skills.apps import (
    open_paint,
    open_settings,
    open_task_manager,
    open_vscode,
    open_application
)


def process_command(command):

    original_command = command.strip()
    command = original_command.lower().strip()

    # ---------------- BASIC RESPONSES ----------------

    if command in [
        "hello",
        "hi",
        "hey",
        "hello jarvis",
        "hi jarvis",
        "hey jarvis"
    ]:
        speak("Hello, I am working properly")

    elif "who are you" in command or "what is your name" in command:
        speak("I am Jarvis, your personal assistant")

    # ---------------- TIME AND DATE ----------------

    elif command in [
        "what time is it",
        "tell me the time",
        "time",
        "current time"
    ]:
        tell_time()

    elif command in [
        "what is the date",
        "what's the date",
        "tell me the date",
        "date",
        "what day is it"
    ]:
        tell_date()

    # ---------------- YOUTUBE SEARCH ----------------

    elif command.startswith("search youtube for "):
        query = original_command[19:].strip()
        search_youtube(query)

    elif command.startswith("search youtube "):
        query = original_command[15:].strip()
        search_youtube(query)

    # ---------------- YOUTUBE PLAY ----------------

    elif command.startswith("play ") and command.endswith(" on youtube"):
        query = original_command[5:-11].strip()
        play_on_youtube(query)

    # ---------------- SPOTIFY SEARCH ----------------

    elif command.startswith("search spotify for "):
        query = original_command[19:].strip()
        search_spotify(query)

    elif command.startswith("search spotify "):
        query = original_command[15:].strip()
        search_spotify(query)

    # ---------------- SPOTIFY PLAY ----------------

    elif command.startswith("play ") and command.endswith(" on spotify"):
        query = original_command[5:-11].strip()
        search_spotify(query)

    # ---------------- GOOGLE SEARCH ----------------

    elif command.startswith("search google for "):
        query = original_command[18:].strip()
        search_google(query)

    elif command.startswith("search google "):
        query = original_command[14:].strip()
        search_google(query)

    elif command.startswith("google "):
        query = original_command[7:].strip()
        search_google(query)

    # ---------------- BROWSER ----------------

    elif command in [
        "open youtube",
        "youtube"
    ]:
        open_youtube()

    elif command in [
        "open google",
        "google"
    ]:
        open_google()

    elif command in [
        "open chrome",
        "chrome"
    ]:
        open_chrome()

    # ---------------- SYSTEM ----------------

    elif command in [
        "open calculator",
        "calculator",
        "calc"
    ]:
        open_calculator()

    elif command in [
        "open notepad",
        "notepad"
    ]:
        open_notepad()

    elif command in [
        "open file explorer",
        "file explorer",
        "open files"
    ]:
        open_file_explorer()

    # ---------------- APPLICATIONS ----------------

    elif command in [
        "open paint",
        "paint"
    ]:
        open_paint()

    elif command in [
        "open settings",
        "settings"
    ]:
        open_settings()

    elif command in [
        "open task manager",
        "task manager"
    ]:
        open_task_manager()

    elif command in [
        "open visual studio code",
        "visual studio code",
        "open vs code",
        "vs code",
        "open vscode",
        "vscode"
    ]:
        open_vscode()

    # ---------------- GENERIC APP LAUNCHER ----------------

    elif command.startswith("open "):

        app_name = command[5:].strip()

        if app_name.endswith(" please"):
            app_name = app_name[:-7].strip()

        if app_name:
            open_application(app_name)

        else:
            speak(
                "Which application would you like me to open?"
            )

    # ---------------- EXIT ----------------

    elif command in [
        "stop",
        "exit",
        "quit",
        "bye",
        "bye jarvis",
        "goodbye",
        "goodbye jarvis",
        "shutdown",
        "shut down",
        "shutdown jarvis",
        "shut down jarvis"
    ]:
        speak("Goodbye")
        return "exit"

    # ---------------- AI INTENT ROUTING ----------------

    else:

        intent_data = detect_intent(
            original_command
        )

        intent = intent_data.get(
            "intent",
            "CHAT"
        )

        query = intent_data.get(
            "query",
            ""
        ).strip()

        print(
            "Detected intent:",
            intent
        )

        print(
            "Detected query:",
            query
        )

        # ---------- OPEN APP ----------

        if intent == "OPEN_APP":

            if query:
                open_application(query)

            else:
                speak(
                    "Which application would you like me to open?"
                )

        # ---------- OPEN YOUTUBE ----------

        elif intent == "OPEN_YOUTUBE":
            open_youtube()

        # ---------- OPEN GOOGLE ----------

        elif intent == "OPEN_GOOGLE":
            open_google()

        # ---------- OPEN CHROME ----------

        elif intent == "OPEN_CHROME":
            open_chrome()

        # ---------- SEARCH YOUTUBE ----------

        elif intent == "SEARCH_YOUTUBE":

            if query:
                search_youtube(query)

            else:
                speak(
                    "What would you like me to search for on YouTube?"
                )

        # ---------- PLAY YOUTUBE ----------

        elif intent == "PLAY_YOUTUBE":

            if query:
                play_on_youtube(query)

            else:
                speak(
                    "What would you like me to play on YouTube?"
                )

        # ---------- SEARCH GOOGLE ----------

        elif intent == "SEARCH_GOOGLE":

            if query:
                search_google(query)

            else:
                speak(
                    "What would you like me to search for?"
                )

        # ---------- SEARCH SPOTIFY ----------

        elif intent == "SEARCH_SPOTIFY":

            if query:
                search_spotify(query)

            else:
                speak(
                    "What would you like me to search for on Spotify?"
                )

        # ---------- TIME ----------

        elif intent == "GET_TIME":
            tell_time()

        # ---------- DATE ----------

        elif intent == "GET_DATE":
            tell_date()

        # ---------- LIVE WEB SEARCH ----------

        elif intent == "WEB_SEARCH":

            search_question = query

            if not search_question:
                search_question = original_command

            response = answer_from_web(
                search_question
            )

            if response:
                speak(response)

            else:
                speak(
                    "I could not retrieve current information."
                )

        # ---------- EXIT ----------

        elif intent == "EXIT":

            speak("Goodbye")
            return "exit"

        # ---------- CHAT ----------

        elif intent == "CHAT":

            response = ask_llm(
                original_command
            )

            if response:
                speak(response)

            else:
                speak(
                    "Sorry, I could not generate a response."
                )

        # ---------- FALLBACK ----------

        else:

            response = ask_llm(
                original_command
            )

            if response:
                speak(response)

            else:
                speak(
                    "Sorry, I could not understand that request."
                )

    return "continue"