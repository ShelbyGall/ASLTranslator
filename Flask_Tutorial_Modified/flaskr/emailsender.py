from flask_mail import Message

from flask import Blueprint, render_template

bp = Blueprint('resetrequest', __name__, url_prefix='/resetrequest')

from __init__ import mailSender, defaultSenderEmail
import auth
#from auth import get_reset_token

#def send_email(usernameoremail):
def send_email(usernameoremail, htmlInput):

    token = auth.get_reset_token(usernameoremail)
    #token = get_reset_token(usernameoremail)

    msg = Message("ASL App Account - Password Reset",
        sender = defaultSenderEmail,
        recipients = [usernameoremail]
    )
    #msg.html = render_template('reset_email.html', usernameoremail=usernameoremail, token=token)
    msg.html = render_template(htmlInput, usernameoremail=usernameoremail, token=token)
    mailSender.send(msg)