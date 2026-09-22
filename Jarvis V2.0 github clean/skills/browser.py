import os
import webbrowser
import pywhatkit

from urllib.parse import quote_plus, quote

from core.voice import speak


def open_youtube():
    speak("Opening YouTube")
    webbrowser.open("https://youtube.com")


def open_google():
    speak("Opening Google")
    webbrowser.open("https://google.com")


def open_chrome():
    speak("Opening Chrome")
    os.system("start chrome")


def search_youtube(query):
    if not query:
        speak("What would you like me to search for on YouTube?")
        return False

    encoded_query = quote_plus(query)

    speak(f"Searching YouTube for {query}")

    webbrowser.open(
        f"https://www.youtube.com/results?search_query={encoded_query}"
    )

    return True


def search_google(query):
    if not query:
        speak("What would you like me to search for?")
        return False

    encoded_query = quote_plus(query)

    speak(f"Searching Google for {query}")

    webbrowser.open(
        f"https://www.google.com/search?q={encoded_query}"
    )

    return True


def play_on_youtube(query):
    if not query:
        speak("What would you like me to play on YouTube?")
        return False

    try:
        speak(f"Playing {query} on YouTube")

        pywhatkit.playonyt(query)

        return True

    except Exception as error:
        print("YouTube playback error:", error)

        speak("I could not start that video")

        return False


def search_spotify(query):
    if not query:
        speak("What would you like me to search for on Spotify?")
        return False

    try:
        encoded_query = quote(query, safe="")

        speak(f"Searching Spotify for {query}")

        spotify_uri = f"spotify:search:{encoded_query}"

        os.system(
            f'start "" "{spotify_uri}"'
        )

        return True

    except Exception as error:
        print("Spotify search error:", error)

        speak("I could not search Spotify")

        return False