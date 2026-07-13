"""
Defines the API control to create a user session and remove the previous ones.
"""


import os, threading


from flasgger import swag_from
from flask import request


from nephila_logging import ControllerLoggerManager


from app import service
from app.api_response import APIResponse
from app.constants import SWAGGER_FILENAME
from app.messages import response_msg_successful_mail
from app.response_codes import response_code_successful_mail
from app.validators import SendMailModel
from app.utils import exception_handler


@exception_handler
@swag_from(SWAGGER_FILENAME)
def send_mail():

    """
    Control to create a user session and remove the previous ones.
    """

    logger = ControllerLoggerManager.get()
    logger.info(f'PID: {os.getpid()}, TID: {threading.get_native_id()} | {request.remote_addr} | {request.method} {request.path}')

    assert isinstance(request.json, dict)
    model = SendMailModel(**request.json)

    session_id = service.send_mail(model)
    response = APIResponse(
        code = response_code_successful_mail,
        message = response_msg_successful_mail,
        data = {'session_id': session_id}
    )
    return response.make_json_response()