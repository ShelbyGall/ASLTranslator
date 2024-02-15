# JTFrontend/app/__init__.py
# from gevent import monkey
# monkey.patch_all()

from flask import Flask
from flask_socketio import SocketIO

# We are creating a flask application
app = Flask(__name__, template_folder = 'templates', static_folder='static')

# we set the secret_key for the application
app.config["SECRET_KEY"] = "secret"

# we are using socketio to communicate with the backend/frontend
# additionally, we are using eventlet, which will handle requests to the wsgi server concurrently
socketio = SocketIO(app, async_mode = 'eventlet')

# Import routes
from JTFrontend.app import routes