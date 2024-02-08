# import the necessary packages
from JTFrontend.app import app
from main import ASLdetection

# this library will be used to stream from webcam
from flask import Response
import threading

# This is from main.py
import cv2

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
# outputFrame = None

# # this is to support several clients
# lock = threading.Lock()
#
# # detect camera connection
# cap = cv2.VideoCapture(0)
#
#
# @app.route("/video_feed")
# def video_feed():
#     #return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")
#     return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")
#
# def generate_frames():
#     #global cap, lock
#     global lock
#     while cap.isOpened():
#         success, frame = cap.read()
#         if not success:
#             break
#         else:
#             with lock:
#                 image = ASLdetection(frame)
#             ret, buffer = cv2.imencode('.jpg', image)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
#                                                 frame + b'\r\n')
#             if cv2.waitKey(10) & 0xFF == ord('q'):
#                 break
# pass
