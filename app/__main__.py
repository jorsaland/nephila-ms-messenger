"""
Defines and executes the function that runs the app with the default Flask development server.
"""


import os, sys, threading
from pathlib import Path


from dotenv import load_dotenv


from nephila_logging import NotificationLoggerManager


assert \
    Path(__file__).parent.parent == Path.cwd(), \
    "This app must be run from the root directory."

sys.path.insert(0, '.')


from app.builder import build_app, initialize_loggers
from app.constants import LOCALHOST, PID_FILE, SERVER_ENV, SERVER_VALUE_FLASK
from app.env_vars import EnvVars


def main():

    """
    Runs the app with the default Flask development server.
    """

    pid_file_path = Path.cwd() / PID_FILE

    process_id = str(os.getpid())
    thread_id = str(threading.get_native_id())

    os.environ[SERVER_ENV] = SERVER_VALUE_FLASK
    load_dotenv()

    EnvVars.load()
    EnvVars.validate()
    
    port = EnvVars.PORT
    if not port:
        port = None

    initialize_loggers()
    logger = NotificationLoggerManager.get()

    with pid_file_path.open('w') as file:
        file.write(process_id)

    start_message = f'Starting app with FLASK DEV server. PID: {process_id}, TID: {thread_id}'
    logger.info(start_message)

    try:
        build_app().run(host=LOCALHOST, port=port, debug=True, use_reloader=True)
    finally:
        if os.path.exists(pid_file_path):
            os.remove(pid_file_path)
        logger.info('Flask dev server was stopped.')


if __name__ == '__main__':
    main()