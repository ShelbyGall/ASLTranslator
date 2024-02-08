# JTFrontend/app/__init__.py
#from gevent import monkey
#monkey.patch_all()

from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS


# Create the Flask application
app = Flask(__name__, template_folder = 'templates', static_folder='static')
app.config["SECRET_KEY"] = "secret"
MAX_BUFFER_SIZE = 100000
# This is to initialize an instance of socektio which
# is used to dynamically get input and output when it comes to the
# web browser
# CORS(app, resources={r"/socket.io/*": {"origins": "*"}})
#socketio = SocketIO(app, async_mode='gevent')
socketio = SocketIO(app)
# socketio = SocketIO(
#     app,
#     cors_allowed_origins="*",
#     manage_session=False,
#     message_queue=None, #'redis://'
#     max_http_buffer_size=MAX_BUFFER_SIZE
# )

# # Import routes
from JTFrontend.app import routes  #, webstreaming