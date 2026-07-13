"""
Defines the validation model for the operation to send a mail.
"""


from pathlib import Path


from pydantic import Field


from app.constants import (
    SENDER_NAME_MAX_LENGTH,
    SENDER_NAME_MIN_LENGTH,
)


from ._base import BaseValidationModel


class SendMailModel(BaseValidationModel):


    """
    Validation model for the operation to send a mail.
    """

    sender_name: (str|None) = Field(
        default = None,
        min_length = SENDER_NAME_MIN_LENGTH,
        max_length = SENDER_NAME_MAX_LENGTH,
    )

    subject: (str|None) = Field(default=None)

    message: (str|None) = Field(default=None)

    picture_path: (Path|None) = Field(default=None)

    is_html: bool = Field(default=False)