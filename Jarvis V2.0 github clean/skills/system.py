import os
from datetime import datetime
from core.voice import speak


def tell_time():
    now = datetime.now().strftime("%H:%M")
    speak(f"The time is {now}")


def tell_date():
    today = datetime.now().strftime("%A, %B %d, %Y")
    speak(f"Today is {today}")


def open_calculator():
    speak("Opening calculator")
    os.system("start calc")


def open_notepad():
    speak("Opening Notepad")
    os.system("start notepad")


def open_file_explorer():
    speak("Opening File Explorer")
    os.system("start explorer")