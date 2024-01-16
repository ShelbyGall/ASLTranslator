from flask_mail import Message

from flask import Blueprint, render_template

bp = Blueprint('resetrequest', __name__, url_prefix='/resetrequest')

from . import mailSender, defaultSenderEmail
from . import auth

def send_email(usernameoremail):

    token = auth.get_reset_token(usernameoremail)

    msg = Message("ASL App Account - Password Reset",
        sender = defaultSenderEmail,
        recipients = [usernameoremail]
    )
    msg.html = render_template('reset_email.html', usernameoremail=usernameoremail, token=token)
    mailSender.send(msg)