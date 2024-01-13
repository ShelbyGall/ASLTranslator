import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from flaskr.db import findUser

bp = Blueprint('auth', __name__, url_prefix='/auth')

#@bp.before_first_request
#@bp.route('/splash')
#def splash():
#    return render_template('splash.html')


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
            '''
            try:
                
                db.execute(
                    #"INSERT INTO user (username, password, firstname, lastname, email, country, mobilenumber) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    "INSERT INTO user (password, firstname, lastname, email, country, mobilenumber) VALUES (?, ?, ?, ?, ?, ?)",
                    (generate_password_hash(password), firstname, lastname, email, country, mobilenumber),
                    #(username, generate_password_hash(password))
                )
                db.commit()
                

            except db.IntegrityError:
                #error = f"User {email} is already registered."
                error = f"Email {email} is already registered."
            else:
                return redirect(url_for("auth.login"))
            '''

        flash(error)

    return render_template('register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        usernameoremail = request.form['usernameoremail']
        password = request.form['password']

        '''
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ? OR email = ?', (usernameoremail, usernameoremail)
        ).fetchone()
        '''

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
        '''
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        '''
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

    if request.method == 'GET':
        return render_template('reset.html')

    if request.method == 'POST':

        email = request.form['email']
        '''
        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()
        '''
        cursor = get_db().cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM user WHERE email=%s",
            (email, )
        )
        user = cursor.fetchone()
        cursor.close()

        flash("If this email is associated with an account, an email will be sent.")

        if user:
            emailsender.send_email(user)

        return redirect(url_for('auth.login'))
    
    return render_template('reset.html')


import jwt, os

@bp.route('/password_reset_verified/<token>', methods=['GET', 'POST'])
def reset_verified(token):

    usernameoremail = verify_reset_token(token)
    if not usernameoremail:
        print('no email found')
        return redirect(url_for('auth.login'))
    
    password = request.form['password']
    db = get_db()
    error = None
    if not password:
        error = 'Password is required.'

    if error is None:
        try:
            '''
            db.execute(
                #"INSERT INTO user (username, password, firstname, lastname, email, country, mobilenumber) VALUES (?, ?, ?, ?, ?, ?, ?)",
                "UPDATE user SET password = ? WHERE email = ?",
                (generate_password_hash(password), usernameoremail,),
                #(username, generate_password_hash(password))
            )
            db.commit()
            '''
            cursor = db.cursor(dictionary=True)
            cursor.execute(
                "UPDATE user SET password = %s WHERE email = %s",
                (generate_password_hash(password), usernameoremail,)
            )
            db.commit()
            cursor.close()
        except:
            pass

    if error is None:
        return redirect(url_for('app_routes.login'))

    return render_template('reset_verified.html')

def verify_reset_token(token):
    try:
        usernameoremail = jwt.decode(token,
            key=os.getenv('SECRET_KEY_FLASK'))['reset_password']
    except Exception as e:
        print(e)
        return
    else:
        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE email = %s',
            (usernameoremail,)
        ).fetchone()
        return user

'''EMAIL INFORMATION END'''

'''
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')
# Creates a Blueprint named 'auth'. Like the application object, the blueprint
# needs to know where it's defined, so __name__ is passed as the second argument.
# The url_prefix will be prepended to all URLs associated with the blueprint.

@bp.route('/register', methods=('GET', 'POST'))     # @bp.route associates the URL /register with the register view function.
                                                    # When Flask receives a request to /auth/register, it will call the
                                                    # register view and use the return value as the response.
def register():
    if request.method == 'POST':                    # If the user submitted the form, request.method will be 'POST'. In this
                                                    # case, start validating the input.
        
        username = request.form['username']         # request.form is a spcial type of dict mapping submitted from keys and
        password = request.form['password']         # values. The user will input their username and password.
        db = get_db()
        error = None

        if not username:                            # Validate that username and password are not empty.
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        
        if error is None:
            try:                                                                # If validation succeeds, insert the new user into the database.

                db.execute(                                                     # db.execute takes a SQL query with ? placeholders for any user
                    "INSERT INTO user (username, password) VALUES (?, ?)",      # input and a tuple of values to replace the placeholders with.
                    (username, generate_password_hash(password)),               # The database library will take care of escaping the values so
                )                                                               # you are not vulnerable to a SQL injection attack.
                
                db.commit()                                                     # For security, passwords should never be stored in the database
                                                                                # directly. Instead, generate_password_hash() is used to securely
                                                                                # hash the password, and that hash is stored. Since this query
                                                                                # modifies data, db.commit() needs to be called afterwards to save
                                                                                # the changes.
                
            except db.IntegrityError:                                           # An sqlite3.IntegrityError will occur if the suername already exists,
                error = f"User {username} is already registered."               # which should be shown to the suer as another validation error.
            else:
                return redirect(url_for("auth.login"))                          # After storing the user, they are redirected to the login page. url_for()
                                                                                # generates the URL for the long view based on its name. This is preferable
                                                                                # to writing the URL directly as it allows you to change the URL later
                                                                                # without changing all code that links to it. redirect() generates a redirect
                                                                                # response to the generated URL.

        flash(error)        # If validation fails, the error is shown to the user. flash() stores
                            # messages that can be retrived when rendering the template.

        # When the user initially natigates to auth/register, or there was a validation error,
        # an HTML page with the registration form should be shown. render_template() will
        # render a template containing the HTML, which you'll write in the next step of the
        # tutorial.
        return render_template('auth/register.html')
    
    @bp.route('/login', methods=('GET', 'POST'))
    def login():
        if request.method == 'POST':                # The user is queried first and stored in a variable for later use.
            username = request.form['username']
            password = request.form['password']
            db = get_db()
            error = None
            user = db.execute(
                'SELECT * FROM user WHERE username = ?',
                (username,)
            ).fetchone()        # fetchone() returns one row from the query. If the query returns no results, it returns None.

            if user is None:
                error = 'Incorrect username.'
            elif not check_password_hash(user['password'], password):       # check_password_hash() hashes the submitted password in the same way
                error = 'Incorrect password.'                               # as the stored hash and securely compares them. If they match, the
                                                                            # password is valid.
            if error is None:
                session.clear()                         # session is a dict that stores data across requests. When validation succeeds, the user's
                session['user_id'] = user['id']         # id is stored in a new session. The data is stored in a cookie that is sent to the
                return redirect(url_for('index'))       # browser, and the browser then sends it back with subsequent requests. Flask securely
                                                        # signs the data so that it can't be tampered with.

            flash(error)

        return render_template('auth/login.html')
    
    @bp.before_app_request                  # bp.before_app_request() registers a function that runs before the view function, no matter what URL
    def load_logged_in_user():              # is requested. load_logged_in_user checks if a user id is stored in the session and gets that user's
        user_id = session.get('user_id')    # data from the database, storing it on g.user, which lasts for the length of the request. If there
                                            # is no user id, or of the id doesn't exist, g.user will be None.
        if user_id is None:
            g.user = None
        else:
            g.user = get_db().execute(
                'SELECT * FROM user WHERE id = ?',
                (user_id,)
            ).fetchone()

    # To log out, you need to remove the user id from the session.
    # Then, load_logged_in_user won't load a user on subsequent
    # requests.
    @bp.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('index'))
    
    # Creating, editing, and deleting blog posts will require a user
    # to be logged in. A decorator can be used to check this for each
    # view it's applied to.
    def login_require(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if g.user is None:
                return redirect(url_for('auth.login'))
            
            return view(**kwargs)

        return wrapped_view
    # This decorator returns a new view function that wraps the original view
    # it's applied to. The new function checks if a user is loaded and redirects
    # to the login page otherwise. If a user is loaded, the original view is
    # called and continues normally. You'll use this decorator when writing the
    # blog views.

    # The url_for() function generates the URL to a view based on a name and arguments.
    # The name associated with a view is also called the endpoint, and by default it's
    # the same as the name of the view function.
'''