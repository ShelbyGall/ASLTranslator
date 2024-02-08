# from flask import Flask
#
# app = Flask(__name__)
#
# from JTFrontend.app import routes
# import JTFrontend.webstreaming


# flaskApp.py
#from JTFrontend.app import app
from waitress import serve
from JTFrontend.app import app, socketio
import eventlet
from eventlet import wsgi


if __name__ == '__main__':
    # This allows it to run with the camera on one device (flask.exe)
    #socketio.run(app, debug=True, use_reloader=False,host='0.0.0.0', port=5000) #host='0.0.0.0' port=5000
    # This allows it to run on multiple devices
    # waitress
    #serve(app, host='0.0.0.0', port=5000)
    #socketio.run(app, host='0.0.0.0', port=5000, server='eventlet')
    eventlet_socket = eventlet.listen(('0.0.0.0', 5000))
    wsgi.server(eventlet_socket, app)