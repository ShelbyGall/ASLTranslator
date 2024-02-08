from flask import render_template, send_from_directory
from JTFrontend.app import app
from JTFrontend.app import socketio
from flask import request, jsonify
import base64
from flask_socketio import emit
from main import ASLdetection
import numpy as np
import cv2
import os

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/<selectedNav>')
def selected(selectedNav="home.html"):
    return render_template(f'{selectedNav}')

# this is to clear that one error - 500 for frontend application
@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )

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

@socketio.on("connect")
def test_connect():
    print("Connected")
    emit("my response", {"data": "Connected"})

@socketio.on("image")
def receive_image(image):
    print('received image')
    # Decode the base64-encoded image data (essentially call in the conversion method)
    image = base64_to_image(image)

    # Perform image processing using OpenCV
    # we send the image to our ASLdetection model
    gray = ASLdetection(image)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # the ASL detection model is then resized
    frame_resized = cv2.resize(gray, (640, 360))

    # Now we prep the data to be sent back to the front-end
    # Encode the processed image as a JPEG-encoded base64 string
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, frame_encoded = cv2.imencode(".jpg", frame_resized, encode_param)
    processed_img_data = base64.b64encode(frame_encoded).decode()

    # Prepend the base64-encoded string with the data URL prefix
    b64_src = "data:image/jpg;base64,"
    processed_img_data = b64_src + processed_img_data

    # Send the processed image back to the client-side
    # On the client-side the javascript listener: socket.on("processed_image"...
    # will receive the new processed image
    emit("processed_image", processed_img_data)