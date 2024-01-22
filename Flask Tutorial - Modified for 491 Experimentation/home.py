from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('home', __name__)

@bp.route('/')
@login_required
def index():
    #if request.method == 'POST':
        #cursor = get_db().cursor(dictionary=True)
        #cursor.execute(
        #    'SELECT p.id, title, body, created, author_id, username'
        #    ' FROM post p JOIN user u ON p.author_id = u.id'
        #    ' ORDER BY created DESC'
        #)
        #posts = cursor.fetchall()
        #cursor.close()

    #    return redirect(url_for('home'))
    
    return render_template('index.html')

@bp.route('/accountsettings', methods=('GET', 'POST'))
@login_required
def accountsettings():
    user_id = session.get('user_id')
    emailString = ""
    if user_id is not None:
        cursor = get_db().cursor(dictionary=True)
        cursor.execute(
            "SELECT email FROM user WHERE id=%s",
            (user_id, )
        )
        emailString = cursor.fetchone()
        cursor.close()
    
    if request.method == 'POST':

        newpassword = request.form['newpasswordinput']
        confirmnewpassword = request.form['confirmnewpasswordinput']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        country = request.form['country']
        mobilenumber = request.form['mobilenumber']
        error = None

        if newpassword != confirmnewpassword:
            error = 'Passwords do not match.'

        if error is None:
            db = get_db()
            cursor = db.cursor(dictionary=True)
            cursor.execute(
                "UPDATE user SET password=%s, firstname=%s, lastname=%s, country=%s, mobilenumber=%s WHERE email=%s",
                (generate_password_hash(newpassword), firstname, lastname, country, mobilenumber, emailString)
            )
            g.db.commit()
            cursor.close()

            return render_template('account_settings.html', emailString=emailString)

        flash(error)

    return render_template('account_settings.html')