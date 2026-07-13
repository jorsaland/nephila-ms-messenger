"""
Defines and executes the function that runs the app with Waitress WSGI server.
"""


from logging import Logger
import os, threading


import waitress


from nephila_logging import NotificationLoggerManager


from app.builder import build_app, initialize_loggers
from app.constants import (
    ANYHOST,
    LOCALHOST,
    PID_FILE,
    RUN_MODE_VALUE_DOCKER,
    SERVER_ENV,
    SERVER_VALUE_WAITRESS,
    waitress_env_vars
)
from app.env_vars import EnvVars
from app.exceptions import SetupError
from app.messages import setup_msg_missing_waitress_env_vars


def run_at_start(logger: Logger):

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
    start_message += f' WAITRESS server. PID: {process_id}, TID: {thread_id}'
    logger.info(start_message)


def run_at_exit(logger: Logger):

    """
    Is called right after the master process is terminated. 
    """

    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)
    logger.info('Waitress server stopped.')


def main():

    """
    Runs the app with Waitress WSGI server.
    """

    os.environ[SERVER_ENV] = SERVER_VALUE_WAITRESS
    EnvVars.load()
    EnvVars.validate()

    missing_vars: list[str] = []
    for var in waitress_env_vars:
        if not getattr(EnvVars, var):
            missing_vars.append(var)
    if missing_vars:
        raise SetupError(setup_msg_missing_waitress_env_vars.format(', '.join(missing_vars)))

    initialize_loggers()
    logger = NotificationLoggerManager.get()

    if EnvVars.RUN_MODE == RUN_MODE_VALUE_DOCKER:
        host = ANYHOST
        trusted_proxy = '*'
    else:
        host = LOCALHOST
        trusted_proxy = LOCALHOST

    run_at_start(logger)
    try:
        waitress.serve(
            app = build_app(),
            listen = f'{host}:{EnvVars.PORT}',
            threads = int(EnvVars.THREADS),
            trusted_proxy=trusted_proxy,
            trusted_proxy_headers=['X-Forwarded-For'],
        )
    finally:
        run_at_exit(logger)


if __name__ == '__main__':
    main()