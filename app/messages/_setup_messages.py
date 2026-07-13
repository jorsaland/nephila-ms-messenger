"""
Defines the internal app messages to be displayed during the setup.
"""


setup_msg_missing_gunicorn_env_vars = 'The following environment variables for Gunicorn are missing: {}.'
setup_msg_missing_mandatory_env_vars = 'The following environment variables are missing: {}.'
setup_msg_missing_waitress_env_vars = 'The following environment variables for Waitress are missing: {}.'
setup_msg_not_instantiable = "Class '{}' must not be instantiated. Use class attributes directly."

setup_msg_invalid_app_name = 'The app name only accepts lowercase letters and dashes (-).'
setup_msg_invalid_logging_level = "Logging level '{invalid_level}' is not valid. Valid levels: {valid_levels}."
setup_msg_invalid_utc_offset = 'UTC offset must be an integer between -23 and 23.'

setup_msg_user_created_by_admin = "User '{}' was created by the admin."
setup_msg_no_users_found = 'No users were found in the database. At least one is needed.'