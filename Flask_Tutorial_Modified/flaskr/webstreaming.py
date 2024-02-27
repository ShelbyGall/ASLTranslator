from flask import render_template, send_from_directory
from flask import Blueprint
#from Flask_Tutorial_Modified.flaskr import app  # Flask Tutorial - Modified for 491 Experimentation

bp = Blueprint('stream', __name__, url_prefix='/stream')

#@app.route('/')
#@app.route('/stream')
#@bp.route('/stream')
@bp.route('/', methods=('GET', 'POST'))
def stream():
    return render_template('stream.html')

# # this is to clear that one error - 500 for frontend application
# @app.route("/favicon.ico")
# def favicon():
#     return send_from_directory(
#         os.path.join(app.root_path, "static"),
#         "favicon.ico",
#         mimetype="image/vnd.microsoft.icon",
#     )