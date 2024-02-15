from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

from auth import login_required
from db import get_db
#from auth import *
#from db import *

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
    outputString = ""
    if user_id is not None:
        cursor = get_db().cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM user WHERE id=%s",
            (user_id, )
        )
        outputString = cursor.fetchone()
        print(outputString)
        cursor.close()
    
    if request.method == 'POST':

        newpassword = request.form['newpasswordinput']
        print(newpassword)
        confirmnewpassword = request.form['confirmnewpasswordinput']
        print(confirmnewpassword)
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        country = request.form['country']
        mobilenumber = request.form['mobilenumber']

        if (firstname is None) or (firstname == ""): firstname = outputString['firstname']
        if (lastname is None) or (lastname == ""): lastname = outputString['lastname']
        if (country is None) or (country == ""): country = outputString['country']
        if (mobilenumber is None) or (mobilenumber == ""): mobilenumber = outputString['mobilenumber']

        error = None

        if newpassword != confirmnewpassword:
            error = 'Passwords do not match.'

        if error is None:
            email = outputString['email']
            
            db = get_db()
            cursor = db.cursor(dictionary=True)
            if (newpassword is None) or (newpassword == ""):
                cursor.execute(
                    "UPDATE user SET firstname=%s, lastname=%s, country=%s, mobilenumber=%s WHERE email=%s AND id=%s",
                    (firstname, lastname, country, mobilenumber, email, user_id)
                )
            else:
                cursor.execute(
                    "UPDATE user SET password=%s, firstname=%s, lastname=%s, country=%s, mobilenumber=%s WHERE email=%s AND id=%s",
                    (generate_password_hash(newpassword), firstname, lastname, country, mobilenumber, email, user_id)
                )
            g.db.commit()
            cursor.close()
            
            return render_template('account_settings.html', outputString=outputString)

    return render_template('account_settings.html', outputString=outputString)

@login_required
def enterchange(email):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "UPDATE user SET password=%s, firstname=%s, lastname=%s, country=%s, mobilenumber=%s WHERE email=%s",
        (generate_password_hash(newpassword), firstname, lastname, country, mobilenumber, email)
    )
    g.db.commit()
    cursor.close()