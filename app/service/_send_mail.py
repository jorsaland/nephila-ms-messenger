"""
Defines the function that sends an email.
"""


import smtplib
import ssl


from nephila_logging import DebugLoggerManager


from app.env_vars import EnvVars
from app.validators import SendMailModel


from ._build_multipart import build_multipart


@DebugLoggerManager.trace
def send_mail(model: SendMailModel):

    """
    Sends an email.
    """

    multipart = build_multipart(
        receiver_mail = EnvVars.SENDER_MAIL,
        sender_name = model.sender_name,
        subject = model.subject,
        message = model.message,
        picture_path = str(model.picture_path) if model.picture_path else None,
        is_html = model.is_html,
    )

    context = ssl.create_default_context()
    host = EnvVars.SMTP_HOST
    port = int(EnvVars.SMTP_PORT)

    with smtplib.SMTP_SSL(host=host, port=port, context=context) as server:
        server.login(EnvVars.SENDER_MAIL, EnvVars.SENDER_PASSWORD)
        server.send_message(multipart)