from flask import Flask

from flask_mail import Mail, Message

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

bp = Blueprint('resetrequest', __name__, url_prefix='/resetrequest')

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "username@gmail.com"
app.config['MAIL_PASSWORD'] = "password"
mail = Mail(app)


from . import auth
import os

def send_email(usernameoremail):

    token = auth.get_reset_token()

    msg = Message()
    msg.subject = "Flask App Password Reset"
    msg.sender = os.getenv('MAIL_USERNAME')
    msg.recipients = [usernameoremail]
    msg.html = render_template('reset_email.html', usernameoremail=usernameoremail, token=token)

    mail.send(msg)


'''
from threading import Thread

def send_email(app, msg):
    with app.app_context():
        mail.send(msg)
msg = Message()
msg.subject = "Email Subject"
msg.recipients = ['recipient@gmail.com']
msg.sender = 'username@gmail.com'
msg.body = 'Email body'
Thread(target=send_email, args=(app, msg)).start()

def send_email(user):
    token = get_reset_token()
    msg = Message()
    msg.subject = "Flask App Password Reset"
    msg.sender = os.getenv('MAIL_USERNAME')
    msg.recipients = [user.email]
    msg.html = render_template('reset_email.html',
                                user=user, 
                                token=token)
mail.send(msg)


from . import auth

@bp.route('/resetrequest', methods=('GET', 'POST'))
def starting():
    get_reset_token(request.form['usernameoremail'])
    return render_template('forgotpassword.html')

@bp.route('/resetrequest', methods=('GET', 'POST'))
def reset_password_request():
    return 


import time, os, jwt

def get_reset_token(usernameoremail, expires=500):
    return jwt.encode({'reset_password': usernameoremail, 'exp': time() + expires}, key=os.getenv('SECRET_KEY_FLASK'))

def verify_reset_token(token):
    try:
        usernameoremail = jwt.decode(token, key=os.getenv('SECRET_KEY_FLASK'))['reset_password']
    except Exception as e:
        print(e)
        return
    return User.query.filter_by(usernameoremail=usernameoremail).first()



def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

'''