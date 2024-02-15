# JTFrontend/app/__init__.py
from flask import Flask

# Create the Flask application
app = Flask(__name__)

# Import routes
from JTFrontend.app import routes, webstreaming
