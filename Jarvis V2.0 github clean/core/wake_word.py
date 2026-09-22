import openwakeword
from openwakeword.model import Model
import pyaudio
import numpy as np


# ---------------- CONFIG ----------------

SAMPLE_RATE = 16000
CHUNK_SIZE = 1280
WAKE_THRESHOLD = 0.5


# ---------------- MODEL SETUP ----------------

openwakeword.utils.download_models()

model = Model(
    wakeword_models=[
        "hey_jarvis"
    ]
)


# ---------------- WAKE WORD FUNCTION ----------------

def wait_for_wake_word():

    # Clear any audio/features left over from the previous
    # wake-word session before we begin listening again.
    model.reset()

    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE
    )

    print(
        "Waiting for wake word..."
    )

    try:

        while True:

            audio_data = stream.read(
                CHUNK_SIZE,
                exception_on_overflow=False
            )

            audio_array = np.frombuffer(
                audio_data,
                dtype=np.int16
            )

            prediction = model.predict(
                audio_array
            )

            score = prediction.get(
                "hey_jarvis",
                0
            )

            if score > WAKE_THRESHOLD:

                print(
                    "Wake word detected!"
                )

                # Reset immediately after detection so the
                # same wake phrase cannot survive into the
                # next sleep session.
                model.reset()

                return True

    finally:

        stream.stop_stream()
        stream.close()
        audio.terminate()


# ---------------- TEST MODE ----------------

if __name__ == "__main__":

    wait_for_wake_word()