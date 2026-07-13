"""
Defines the decorator that runs a controller function and converts exceptions to API responses.
"""


from collections.abc import Callable
from functools import wraps
from traceback import format_exc


from flask.wrappers import Response
from pydantic import ValidationError


from nephila_logging import ExceptionLoggerManager


from app.api_response import APIResponse
from app.exceptions import ServiceError
from app.messages import response_msg_unexpected
from app.response_codes import response_code_unexpected, response_code_bad_request


def exception_handler(controller_function: Callable[..., Response]):

    """
    Runs a controller function and converts exceptions into API responses.
    """

    @wraps(controller_function)
    def wrapper(*args, **kwargs):

        exception_logger = ExceptionLoggerManager.get()

        try:
            return controller_function(*args, **kwargs)

        except ValidationError as exception:
            error_messages = [
                f'{".".join(str(key) for key in error["loc"])}: {error["msg"].lower()}'
                for error in exception.errors()
            ]
            response = APIResponse(
                code = response_code_bad_request,
                message = ' | '.join(error_messages),
            )
            return response.make_json_response()

        except ServiceError as exception:
            code, message = exception.args
            response = APIResponse(
                code = code,
                message = message,
            )
            return response.make_json_response()

        except Exception:
            exception_logger.error(format_exc())
            response = APIResponse(
                code = response_code_unexpected,
                message = response_msg_unexpected,
            )
            return response.make_json_response()

    return wrapper