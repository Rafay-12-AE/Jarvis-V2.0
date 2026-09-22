import json
import os


CONFIG_FILE = "data/settings.json"


def load_config():

    if not os.path.exists(CONFIG_FILE):
        return {}

    with open(CONFIG_FILE, "r") as file:
        return json.load(file)


config = load_config()


def get_setting(key):

    return config.get(key)