"""
Defines the function that configures the app with Gunicorn WSGI server.
"""


import os, threading


from gunicorn.arbiter import Arbiter
from gunicorn.workers.gthread import ThreadWorker


from nephila_logging import (
    ControllerLoggerManager,
    DebugLoggerManager,
    ExceptionLoggerManager,
    NotificationLoggerManager,
)


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


def run_at_start(_: Arbiter):

    """
    Is called right before the master process is initialized.
    """

    initialize_loggers()
    logger = NotificationLoggerManager.get()

    process_id = str(os.getpid())
    thread_id = str(threading.get_native_id())

    with open(PID_FILE, 'w') as file:
        file.write(process_id)

    start_message = 'Starting app with'
    if EnvVars.RUN_MODE == RUN_MODE_VALUE_DOCKER:
        start_message += ' DOCKER and'
    start_message += f' GUNICORN server. PID: {process_id}, TID: {thread_id}'
    logger.info(start_message)


def run_at_fork(_: Arbiter, __: ThreadWorker):

    """
    Is called inside the worker's process, right after it is forked from the master process.
    """

    ControllerLoggerManager.fork()
    DebugLoggerManager.fork()
    ExceptionLoggerManager.fork()
    NotificationLoggerManager.fork()


def run_at_exit(_: Arbiter):

    """
    Is called right before the master process is terminated. 
    """

    NotificationLoggerManager.stop() # stops the listener shared by all loggers
    logger = NotificationLoggerManager.get()

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

    host = ANYHOST if EnvVars.RUN_MODE == RUN_MODE_VALUE_DOCKER else LOCALHOST
    gunicorn_setup = {
        'bind': f'{host}:{EnvVars.PORT}',
        'pidfile': PID_FILE,
        'workers': 1,
        'threads': int(EnvVars.THREADS),
        'loglevel': 'debug',
        'when_ready': lambda server: run_at_start(server),
        'post_fork': lambda server, worker: run_at_fork(server, worker),
        'on_exit': lambda server: run_at_exit(server),
    }
    globals().update(gunicorn_setup)


if __name__ == '__config__':
    main()