"""
Defines the function that configures the app with Gunicorn WSGI server.
"""


from logging import Logger
import os, threading


from gunicorn.arbiter import Arbiter


from nephila_logging import NotificationLoggerManager


from app.builder import initialize_loggers
from app.constants import (
    ANYHOST,
    LOCALHOST,
    PID_FILE,
    RUN_MODE_VALUE_DOCKER,
    SERVER_ENV,
    SERVER_VALUE_GUNICORN,
    gunicorn_env_vars
)
from app.env_vars import EnvVars
from app.exceptions import SetupError
from app.messages import setup_msg_missing_gunicorn_env_vars


def run_at_start(logger: Logger, _: Arbiter):

    """
    Is called right before the master process is initialized.
    """

    process_id = str(os.getpid())
    thread_id = str(threading.get_native_id())

    with open(PID_FILE, 'w') as file:
        file.write(process_id)

    start_message = 'Starting app with'
    if EnvVars.RUN_MODE == RUN_MODE_VALUE_DOCKER:
        start_message += ' DOCKER and'
    start_message += f' GUNICORN server. PID: {process_id}, TID: {thread_id}'
    logger.info(start_message)


def run_at_exit(logger: Logger, _: Arbiter):

    """
    Is called right before the master process is terminated. 
    """

    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)
    logger.info('Gunicorn server stopped.')


def main():

    """
    Configures the app with Gunicorn WSGI server.
    """

    os.environ[SERVER_ENV] = SERVER_VALUE_GUNICORN
    EnvVars.load()
    EnvVars.validate()

    missing_vars: list[str] = []
    for var in gunicorn_env_vars:
        if not getattr(EnvVars, var):
            missing_vars.append(var)
    if missing_vars:
        raise SetupError(setup_msg_missing_gunicorn_env_vars.format(', '.join(missing_vars)))

    initialize_loggers()
    logger = NotificationLoggerManager.get()

    host = ANYHOST if EnvVars.RUN_MODE == RUN_MODE_VALUE_DOCKER else LOCALHOST
    gunicorn_setup = {
        'bind': f'{host}:{EnvVars.PORT}',
        'pidfile': PID_FILE,
        'workers': 1,
        'threads': int(EnvVars.THREADS),
        'loglevel': 'debug',
        'on_starting': lambda server: run_at_start(logger, server),
        'on_exit': lambda server: run_at_exit(logger, server),
    }
    globals().update(gunicorn_setup)


if __name__ == '__config__':
    main()