"""
Defines the function that initializes all the loggers used by the app.
"""


from nephila_logging import (
    ControllerLoggerManager,
    DebugLoggerManager,
    ExceptionLoggerManager,
    NotificationLoggerManager,
)


from app.env_vars import EnvVars


from ._get_app_timezone import get_app_timezone


def initialize_loggers():

    """
    Initializes all the loggers used by the app.
    """

    app_timezone = get_app_timezone()

    ControllerLoggerManager.initialize(
        logging_level = EnvVars.LOGGING_LEVEL,
        tzone = app_timezone,
    )

    DebugLoggerManager.initialize(
        logging_level = EnvVars.LOGGING_LEVEL,
        tzone = app_timezone,
    )

    ExceptionLoggerManager.initialize(
        logging_level = EnvVars.LOGGING_LEVEL,
        tzone = app_timezone,
    )

    NotificationLoggerManager.initialize(
        logging_level = EnvVars.LOGGING_LEVEL,
        tzone = app_timezone,
    )