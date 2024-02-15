# from flask import Flask
#
# app = Flask(__name__)
#
# from JTFrontend.app import routes
# import JTFrontend.webstreaming


# flaskApp.py
from JTFrontend.app import app

if __name__ == '__main__':
    app.run(debug=True)