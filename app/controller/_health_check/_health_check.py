"""
Defines the API control that verifies the app is running.
"""


import os, threading


from flasgger import swag_from
from flask import jsonify, make_response, request


from nephila_logging import ControllerLoggerManager


from app.constants import SWAGGER_FILENAME
from app.env_vars import EnvVars


@swag_from(SWAGGER_FILENAME)
def health_check():

    """
    Verifies the app is running.
    """

    logger = ControllerLoggerManager.get()
    logger.info(f'PID: {os.getpid()}, TID: {threading.get_native_id()} | {request.remote_addr} | {request.method} {request.path}')

    response_body = {'service': EnvVars.APP_NAME}
    return make_response(jsonify(response_body), 200)