import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

#splashRoute = '/'

#bp = Blueprint('splash', __name__, url_prefix=splashRoute)
bp = Blueprint('splash', __name__, url_prefix='/splash')

#spashVisited = False

from . import auth

@bp.route('/', methods=('GET', 'POST'))
def splash():
    return render_template('splash.html')
    '''
    global spashVisited
    global splashRoute
    if spashVisited is False:
        spashVisited = True
        splashRoute = '/splash'
        return render_template('splash.html')
    else:
        return redirect(url_for('index'))
    '''