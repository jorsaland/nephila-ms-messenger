"""
Defines the namespace class containing all the environment variables.
"""


import os, re


from app.constants import mandatory_env_vars, valid_loggin_levels
from app.exceptions import SetupError
from app.messages import (
    setup_msg_invalid_app_name,
    setup_msg_invalid_logging_level,
    setup_msg_invalid_utc_offset,
    setup_msg_missing_mandatory_env_vars,
    setup_msg_not_instantiable,
)


class EnvVars:

    """
    Namespace class containing all the environment variables.
    """


    APP_NAME: str = ''

    PORT: str = ''
    THREADS: str = ''

    SERVER: str = ''
    RUN_MODE: str = ''

    LOGGING_LEVEL: str = ''
    UTC_OFFSET: str = ''

    SMTP_HOST: str = ''
    SMTP_PORT: str = ''
    SENDER_MAIL: str = ''
    SENDER_PASSWORD: str = ''
    RECEIVER_MAIL: str = ''


    def __new__(cls, *args, **kwargs):
        raise SetupError(setup_msg_not_instantiable.format(cls.__name__))
    

    @classmethod
    def load(cls):

        """
        Searches for the env variables if have not been set.
        """

        for attr, value in cls.__dict__.items():
            if not attr.startswith('__') and value == '':
                setattr(cls, attr, os.getenv(attr, ''))


    @classmethod
    def validate(cls):

        """
        Validates the environment variables are correctly set.
        """

        # Missing variables
        missing_vars: list[str] = []
        for var in mandatory_env_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        if missing_vars:
            raise SetupError(setup_msg_missing_mandatory_env_vars.format(', '.join(missing_vars)))
        
        # Invalid app name
        if not re.fullmatch(r"^[a-z-]+$", EnvVars.APP_NAME):
            raise SetupError(setup_msg_invalid_app_name)

        # Invalid logging level
        if cls.LOGGING_LEVEL.upper() not in valid_loggin_levels:
            error_msg = setup_msg_invalid_logging_level.format(
                invalid_level = EnvVars.LOGGING_LEVEL,
                valid_levels = ', '.join(valid_loggin_levels),
            )
            raise SetupError(error_msg)

        # Invalid UTC offset
        try:
            assert -23 <= int(cls.UTC_OFFSET) <= 23
        except (ValueError, AssertionError):
            raise SetupError(setup_msg_invalid_utc_offset)