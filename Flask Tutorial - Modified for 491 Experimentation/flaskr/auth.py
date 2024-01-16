import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from flaskr.db import findUser

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        #username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        country = request.form['country']
        mobilenumber = request.form['mobilenumber']
        db = get_db()
        error = None

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            if findUser(None, email) is not None:
                error = f"Email {email} is already registered."
            else:
                cursor = db.cursor(dictionary=True)
                cursor.execute(
                    "INSERT INTO user (password, firstname, lastname, email, country, mobilenumber) VALUES (%s, %s, %s, %s, %s, %s)",
                    (generate_password_hash(password), firstname, lastname, email, country, mobilenumber)
                )
                g.db.commit()
                cursor.close()

                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        usernameoremail = request.form['usernameoremail']
        password = request.form['password']

        cursor = get_db().cursor(dictionary=True)
        error = None
        cursor.execute(
            "SELECT * FROM user WHERE username = %s OR email = %s",
            (usernameoremail, usernameoremail)
        )
        user = cursor.fetchone()
        cursor.close()

        if user is None:
            error = 'Incorrect username or email.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        cursor = get_db().cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM user WHERE id=%s",
            (user_id, )
        )
        g.user = cursor.fetchone()
        cursor.close()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


'''EMAIL INFORMATION START'''

from . import emailsender

@bp.route('/reset', methods=('GET', 'POST'))
def reset():

    if request.method == 'POST':

        email = request.form['email']
        cursor = get_db().cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM user WHERE email=%s",
            (email, )
        )
        user = cursor.fetchone()
        cursor.close()

        flash("If this email is associated with an account, an email will be sent to it.")

        if user:
            emailsender.send_email(email)

        return redirect(url_for('auth.login'))
    
    return render_template('reset.html')


import jwt

@bp.route('/password_reset_verified/<token>', methods=['GET', 'POST'])
def reset_verified(token):

    usernameoremail = verify_reset_token(token)
    if not usernameoremail:
        print('no email found')
        return redirect(url_for('auth.login'))
    
    password = request.form.get('password')

    print("-------------------")
    print(usernameoremail)
    print(password)
    print("-------------------")

    db = get_db()
    error = None
    if not password:
        error = 'Password is required.'

    if error is None:
        try:
            cursor = db.cursor(dictionary=True)
            cursor.execute(
                "UPDATE user SET password = %s WHERE email = %s",
                (generate_password_hash(password), usernameoremail['email'],)
            )
            db.commit()
            cursor.close()
        except:
            pass

    if error is None:
        return redirect(url_for('auth.login'))

    return render_template('reset_verified.html')

import time
from . import JWT_SECRET_KEY

def get_reset_token(usernameoremail, expires=500):
    return jwt.encode(
        payload={'reset_password': usernameoremail,
                 'exp': time.time() + expires},
        key=JWT_SECRET_KEY,
        algorithm="HS256"
    )

def verify_reset_token(token):
    try:
        usernameoremail = jwt.decode(
            jwt=token,
            key=JWT_SECRET_KEY,
            algorithms=["HS256"]
        )
    except Exception as e:
        print(e)
        return
    else:
        cursor = get_db().cursor(dictionary=True)
        cursor.execute(
            'SELECT * FROM user WHERE email = %s',
            (usernameoremail['reset_password'],)
        )
        user = cursor.fetchone()
        cursor.close()

        return user

'''EMAIL INFORMATION END'''