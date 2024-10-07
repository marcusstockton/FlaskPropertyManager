from flask_mail import Message
from app.main import mail


def send_email(to: str, subject: str, msg: str):
    """Sends an email"""
    msg = Message(
        subject,
        recipients=[to],
        body=msg,
    )

    try:
        mail.send(msg)
        return "Email sent succesfully!"
    except Exception as e:
        raise Exception(e) from e
