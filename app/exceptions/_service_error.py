"""
Defines the exception raised to force error responses
"""


class ServiceError(Exception):

    """
    Exception raised to force error responses.
    """

    def __init__(self, *, code: tuple[int, str], message: str):
        self.args: tuple[tuple[int, str], str]
        super().__init__(code, message)