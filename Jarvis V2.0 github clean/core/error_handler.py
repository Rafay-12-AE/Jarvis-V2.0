import traceback
from core.logger import write_log


def handle_error(error):

    error_details = traceback.format_exc()

    print("Jarvis Error:")
    print(error_details)

    write_log(f"ERROR: {error}")
    write_log(error_details)


def safe_execute(function, *args, **kwargs):

    try:
        return function(*args, **kwargs)

    except Exception as error:
        handle_error(error)
        return None