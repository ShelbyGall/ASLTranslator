from JTFrontend.app import app, socketio
import eventlet
from eventlet import wsgi

if __name__ == '__main__':
    # Eventlet is a library that allows asynchronous input and output on a server
    # By using the Eventlet library, we make a socket that is open to all ip addresses on port 5000
    # The socket will listen for any clients that want to connect and communicate to the website
    eventlet_socket = eventlet.listen(('0.0.0.0', 5000))

    # Web Server Gateway Interface (WSGI) is a communication specification between Python applications and web servers
    # WSGI servers support concurrent libraries like Eventlet
    # Essentially, we create a WSGI server that utilizes Eventlet which provides concurrency in our Flask application (app).
    wsgi.server(eventlet_socket, app)