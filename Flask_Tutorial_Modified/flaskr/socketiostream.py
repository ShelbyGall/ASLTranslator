import eventlet
#from Flask_Tutorial_Modified.flaskr import app  # Flask Tutorial - Modified for 491 Experimentation
#from Flask_Tutorial_Modified.flaskr import socketio

from flask import request
import base64
from PredictLetter import predict_letter_from_image
import numpy as np
import cv2
#from Flask_Tutorial_Modified.flaskr import socketio

from flask_socketio import SocketIO

socketio = SocketIO()

# This is used to convert the image from base64url (from the frontend) back to image data
# Essentially it converts like the following:
# base64 -> string -> bytes -> numpyArray -> image
def base64_to_image(base64_string):
    # Extract the base64 encoded binary data from the input string
    base64_data = base64_string.split(",")[1]
    # Decode the base64 data to bytes
    image_bytes = base64.b64decode(base64_data)
    # Convert the bytes to numpy array. The numpy array will contain only ints
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    # Decode the numpy array as an image using OpenCV which takes in a numpy array, and then
    # sets the images output color
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image

# Backend side to know that the Frontend connected to the Backend
@socketio.on("connect")
def test_connect():
    print("Connected")
    # We send a message back to the
    #emit("my response", {"data": "Connected"})

@socketio.on("image")
def receive_image(image):
    print('received image')
    # Decode the base64-encoded image data
    # Since the frontend sends the image data via base64 url, we have to decode it back to its original form
    image = base64_to_image(image)

    # We perform a image processing asynchronously by creating a task which calls/performs process_image
    # and is associated with the session id which is defined by request.sid
    # Every client that we receive an image from will create its own task to process the image
    eventlet.spawn(process_image, image, request.sid) # Pass the request.sid to identify the client

def process_image(image, client_sid):
    # We pass in the image and send it over to Josh's predict_letter... method
    letter = predict_letter_from_image(image)
    # We pause the current execution briefly to allow other clients to schedule their tasks next
    eventlet.sleep(0)
    print('processed and sent image' + str(client_sid))

    # Emit the processed letter back to the client identified by client_sid/request.sid
    # This way, the program knows which client to send the output back to
    socketio.emit("letter", letter, room=client_sid)