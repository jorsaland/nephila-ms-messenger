"""
Defines the function that generates the timezone for the app offset.
"""


from datetime import timezone, timedelta


from app.env_vars import EnvVars


def get_app_timezone():

    """
    Generates the timezone for the app offset.
    """

    return timezone(timedelta(hours=int(EnvVars.UTC_OFFSET)))