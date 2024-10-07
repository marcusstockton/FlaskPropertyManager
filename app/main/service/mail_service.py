from flask import render_template
from flask_mail import Message
from app.main import mail


def send_email(
    to: str, subject: str, msg: str, html_template: str | None = None, **kwargs
):
    """Sends an email"""
    msg = Message(subject=subject, recipients=[to], body=msg)
    if html_template:
        msg.html = render_template(html_template, **kwargs)
    try:
        mail.send(msg)
        return "Email sent succesfully!"
    except Exception as e:
        raise Exception(e) from e
