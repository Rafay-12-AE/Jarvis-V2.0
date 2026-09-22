import os
import json
import subprocess

from core.voice import speak


# ---------------- COMMON DIRECT COMMANDS ----------------

APP_COMMANDS = {
    "paint": "mspaint",
    "settings": "ms-settings:",
    "task manager": "taskmgr",
    "visual studio code": "code",
    "vs code": "code",
    "vscode": "code",
    "notepad": "notepad",
    "calculator": "calc",
    "file explorer": "explorer",
    "chrome": "chrome",
    "spotify": "spotify",
    "steam": "steam",
}


# ---------------- NAME CLEANING ----------------

def normalize_app_name(name):
    return (
        name.lower()
        .replace("-", " ")
        .replace("_", " ")
        .strip()
    )


# ---------------- START MENU SHORTCUT SEARCH ----------------

def find_start_menu_app(app_name):
    app_name = normalize_app_name(app_name)

    start_menu_locations = [
        os.path.join(
            os.environ.get("APPDATA", ""),
            "Microsoft",
            "Windows",
            "Start Menu",
            "Programs"
        ),

        os.path.join(
            os.environ.get("PROGRAMDATA", ""),
            "Microsoft",
            "Windows",
            "Start Menu",
            "Programs"
        )
    ]

    possible_matches = []

    for location in start_menu_locations:

        if not os.path.isdir(location):
            continue

        for root, folders, files in os.walk(location):

            for file in files:

                if not file.lower().endswith(".lnk"):
                    continue

                shortcut_name = os.path.splitext(file)[0]
                normalized_shortcut = normalize_app_name(shortcut_name)

                shortcut_path = os.path.join(root, file)

                if normalized_shortcut == app_name:
                    return shortcut_path

                if app_name in normalized_shortcut:
                    possible_matches.append(shortcut_path)

    if possible_matches:
        return possible_matches[0]

    return None


# ---------------- WINDOWS REGISTERED APP SEARCH ----------------

def find_windows_app(app_name):
    app_name = normalize_app_name(app_name)

    try:
        command = [
            "powershell",
            "-NoProfile",
            "-Command",
            "Get-StartApps | Select-Object Name,AppID | ConvertTo-Json -Compress"
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            return None

        output = result.stdout.strip()

        if not output:
            return None

        apps = json.loads(output)

        # PowerShell returns a dictionary instead of a list
        # when only one result exists.
        if isinstance(apps, dict):
            apps = [apps]

        partial_matches = []

        for app in apps:
            name = app.get("Name")
            app_id = app.get("AppID")

            if not name or not app_id:
                continue

            normalized_name = normalize_app_name(name)

            # Best result: exact app name
            if normalized_name == app_name:
                return app_id

            # Fallback: partial name
            if app_name in normalized_name:
                partial_matches.append(app_id)

        if partial_matches:
            return partial_matches[0]

    except Exception as error:
        print("Windows app search error:", error)

    return None


# ---------------- DISCORD FALLBACK ----------------

def find_discord():
    local_app_data = os.environ.get("LOCALAPPDATA")

    if not local_app_data:
        return None

    discord_folder = os.path.join(
        local_app_data,
        "Discord"
    )

    if not os.path.isdir(discord_folder):
        return None

    for folder in os.listdir(discord_folder):

        if folder.startswith("app-"):

            discord_exe = os.path.join(
                discord_folder,
                folder,
                "Discord.exe"
            )

            if os.path.isfile(discord_exe):
                return discord_exe

    return None


# ---------------- GENERIC APP LAUNCHER ----------------

def open_application(app_name):
    app_name = normalize_app_name(app_name)

    try:

        # ---------- DIRECT WINDOWS COMMAND ----------

        if app_name in APP_COMMANDS:

            command = APP_COMMANDS[app_name]

            speak(f"Opening {app_name}")

            if command.endswith(":"):

                os.system(
                    f'start "" "{command}"'
                )

            else:

                subprocess.Popen(
                    f'start "" "{command}"',
                    shell=True
                )

            return True


        # ---------- NORMAL START MENU SHORTCUT ----------

        shortcut = find_start_menu_app(app_name)

        if shortcut:

            speak(f"Opening {app_name}")

            os.startfile(shortcut)

            return True


        # ---------- WINDOWS / MICROSOFT STORE APP ----------

        app_id = find_windows_app(app_name)

        if app_id:

            speak(f"Opening {app_name}")

            subprocess.Popen([
                "explorer.exe",
                f"shell:AppsFolder\\{app_id}"
            ])

            return True


        # ---------- DISCORD FALLBACK ----------

        if app_name == "discord":

            discord_path = find_discord()

            if discord_path:

                speak("Opening Discord")

                subprocess.Popen(
                    [discord_path]
                )

                return True


        # ---------- NOT FOUND ----------

        print(f"Application not found: {app_name}")

        speak(
            f"I could not find {app_name} "
            "in your installed applications"
        )

        return False


    except Exception as error:

        print("App launch error:", error)

        speak(f"I could not open {app_name}")

        return False


# ---------------- EXISTING FUNCTIONS ----------------

def open_paint():
    open_application("paint")


def open_settings():
    open_application("settings")


def open_task_manager():
    open_application("task manager")


def open_vscode():
    open_application("vs code")