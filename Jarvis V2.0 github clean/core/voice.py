import speech_recognition as sr
import pyttsx3

from core.ui_state import (
    get_ui_state,
    set_ui_state
)


# ---------------- SPEECH RECOGNIZER ----------------

# Keep one recognizer alive for the whole Jarvis session.
# This allows its dynamic energy threshold to adapt over time.

recognizer = sr.Recognizer()

recognizer.pause_threshold = 1.0
recognizer.non_speaking_duration = 0.5

recognizer.dynamic_energy_threshold = True

# Prevent the adaptive threshold from becoming too sluggish.

recognizer.dynamic_energy_adjustment_damping = 0.15
recognizer.dynamic_energy_ratio = 1.5

# Prevent network recognition from hanging forever.

recognizer.operation_timeout = 10


# Only perform full ambient-noise calibration once.

microphone_calibrated = False


# ============================================================
# VOICE ENGINE
# ============================================================

def speak(text):

    print(
        "Jarvis:",
        text
    )

    # Remember what Jarvis was doing before speech started.
    previous_state = get_ui_state()

    # Every spoken response automatically activates
    # the speaking animation.

    set_ui_state(
        "SPEAKING"
    )

    try:

        # Initialize fresh every time to prevent
        # silent output issues.

        engine = pyttsx3.init()

        engine.setProperty(
            "rate",
            170
        )

        engine.setProperty(
            "volume",
            1.0
        )

        voices = engine.getProperty(
            "voices"
        )

        if voices:

            engine.setProperty(
                "voice",
                voices[0].id
            )

        engine.say(
            text
        )

        engine.runAndWait()

        engine.stop()

    finally:

        # Restore whatever state Jarvis was in before speaking.
        #
        # Example:
        # THINKING -> SPEAKING -> THINKING
        #
        # main.py will then move Jarvis to LISTENING
        # once command processing has completely finished.

        set_ui_state(
            previous_state
        )


# ============================================================
# LISTENING
# ============================================================

def listen():

    global microphone_calibrated

    with sr.Microphone() as source:

        print(
            "Listening..."
        )

        # Calibrate once at the start of the Jarvis session.
        #
        # After this, dynamic energy adjustment continues
        # adapting automatically instead of starting from zero
        # every command.

        if not microphone_calibrated:

            print(
                "Calibrating microphone..."
            )

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.8
            )

            microphone_calibrated = True

            print(
                "Microphone calibrated."
            )

        try:

            audio = recognizer.listen(
                source,
                timeout=8,
                phrase_time_limit=20
            )

        except sr.WaitTimeoutError:

            return ""

    try:

        command = recognizer.recognize_google(
            audio,
            language="en-US"
        )

        print(
            "You:",
            command
        )

        return command.strip()

    except sr.UnknownValueError:

        print(
            "Jarvis could not understand the audio."
        )

        return ""

    except sr.RequestError as error:

        print(
            "Speech recognition service error:",
            error
        )

        return ""

    except Exception as error:

        print(
            "Speech recognition unexpected error:",
            error
        )

        return ""