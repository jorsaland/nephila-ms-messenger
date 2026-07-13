"""
Defines the class that represents API responses.
"""


from flask import jsonify, make_response
from pydantic import JsonValue


class APIResponse:


    """
    Represents API responses.
    """


    def __init__(
        self,
        *,
        code: tuple[int, str],
        message: str,
        data: JsonValue = None
    ):

        self.status_code = code[0]
        self.internal_code = code[1]
        self.message = message
        self.data = data


    def make_json_response(self):
        
        """
        Generates a Flask JSON response.
        """

        response = {
            'code': self.internal_code,
            'message': self.message,
        }
        if self.data is not None:
            response['data'] = self.data

        return make_response(jsonify(response), self.status_code)