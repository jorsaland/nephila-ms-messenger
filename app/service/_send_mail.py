"""
Defines the function that sends an email.
"""


import smtplib
import ssl


from app.env_vars import EnvVars


from ._build_multipart import build_multipart


def send_mail(
    *,
    sender_name: (str|None) = None,
    subject: (str|None) = None,
    message: (str|None) = None,
    picture_path: (str|None) = None,
    is_html: bool = False,
):

    """
    Sends an email.
    """

    multipart = build_multipart(
        receiver_mail = EnvVars.SENDER_MAIL,
        sender_name = sender_name,
        subject = subject,
        message = message,
        picture_path = picture_path,
        is_html = is_html,
    )

    context = ssl.create_default_context()
    host = EnvVars.SMTP_HOST
    port = int(EnvVars.SMTP_PORT)

    with smtplib.SMTP_SSL(host=host, port=port, context=context) as server:
        server.login(EnvVars.SENDER_MAIL, EnvVars.SENDER_PASSWORD)
        server.send_message(multipart)