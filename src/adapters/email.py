import logging
from aiosmtplib.errors import SMTPDataError
from fastapi_mail import FastMail, MessageSchema, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from src.config.email_config import mail_conf

logger = logging.getLogger("uvicorn")

async def send_message_with_template(
    subject: str,
    recipients: list[str],
    template_body: dict[str, str],
    template_name: str,
) -> None:
    """
    The send_message_with_template function sends an email message to the specified recipients.
    It takes in a subject, a list of recipients, and a template body, then creates an instance
    of the MessageSchema class with these parameters.
    """
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        template_body=template_body,
        subtype=MessageType.html,
    )

    fm = FastMail(mail_conf)
    try:
        await fm.send_message(message, template_name=template_name)

    except SMTPDataError as e:
        logger.error("SMTPDataError: %s", e.message)

    except ConnectionErrors as e:
        logger.error("ConnectionError: %s", str(e))


async def send_event_registration_email(
    email: EmailStr,
    event_name: str,
    event_date: str,
    host: str,
) -> None:
    """
    Send Event Registration Email
    """
    await send_message_with_template(
        subject="Event Registration Confirmation",
        recipients=[email],
        template_body={
            "event_name": event_name,
            "event_date": event_date,
            "host": host,
            "email": email,
        },
        template_name="event_registration_template.html",
    )