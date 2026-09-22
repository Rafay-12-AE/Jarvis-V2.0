import datetime
import os


LOG_FILE = "logs/jarvis.log"


def write_log(message):

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_message = f"[{timestamp}] {message}\n"

    os.makedirs("logs", exist_ok=True)

    with open(LOG_FILE, "a") as file:
        file.write(log_message)