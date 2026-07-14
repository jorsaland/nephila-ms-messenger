"""
Defines the app constants related to the environment variables.
"""


mandatory_env_vars = [
    'APP_NAME',
    'LOGGING_LEVEL',
    'UTC_OFFSET',
    'SMTP_HOST',
    'SMTP_PORT',
    'SENDER_MAIL',
    'SENDER_PASSWORD',
    'RECEIVER_MAIL'
]

gunicorn_env_vars = [
    'PORT',
    'THREADS',
]

waitress_env_vars = [
    'PORT',
    'THREADS',
]

SERVER_ENV = 'SERVER'
SERVER_VALUE_FLASK = 'flask'
SERVER_VALUE_GUNICORN = 'gunicorn'
SERVER_VALUE_WAITRESS = 'waitress'

RUN_MODE_VALUE_DOCKER = 'docker'