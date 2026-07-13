"""
Defines the function that builds the MIME multipart.
"""


from email import header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import os


from app.exceptions import ServiceError
from app.messages import response_msg_file_not_found
from app.response_codes import response_code_file_not_found


def build_multipart(
    *,
    receiver_mail: (str|None) = None,
    sender_name: (str|None) = None,
    subject: (str|None) = None,
    message: (str|None) = None,
    picture_path: (str|None) = None,
    is_html: bool = False,
):

    """
    Builds the MIME multipart.
    """

    main_part = MIMEMultipart()
    main_part.add_header('To', receiver_mail)

    if sender_name:
        main_part.add_header('From', header.Header(sender_name, 'utf-8').encode())

    if subject:
        main_part.add_header('Subject', subject)

    if message:
        text_part = MIMEText(message, ('html'if is_html else 'plain'), 'utf-8')
        body_part = MIMEMultipart('alternative')
        body_part.attach(text_part)
        main_part.attach(body_part)

    if picture_path:
        if not os.path.exists(picture_path):
            raise ServiceError(
                code = response_code_file_not_found,
                message = response_msg_file_not_found
            )
        with open(picture_path, 'rb') as file:
            image_part = MIMEImage(file.read())
        image_part.add_header('Content-ID', '<image1>')
        image_part.add_header('Content-Disposition', 'inline', filename=picture_path)
        main_part.attach(image_part)

    return main_part