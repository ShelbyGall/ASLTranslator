from flask import Blueprint, render_template


bp = Blueprint('splash', __name__, url_prefix='/splash')

@bp.route('/', methods=('GET', 'POST'))
def splash():
    return render_template('splash.html')