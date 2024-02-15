# import the necessary packages
from JTFrontend.flaskApp import app

# this library will be used to stream from webcam
#from imutils.video import VideoStream
from flask import Response
import threading
#import imutils
#import time
#import cv2

# This is from main.py
import cv2
import numpy as np
import os
import time
import keyboard
from imageProcessing import mp_detection, formatPoints, draw_styled_landmarks, mp_hands
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import TensorBoard

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame = None

# this is to support several clients
lock = threading.Lock()

# initialize the video stream and allow the camera sensor to warmup

# vs = cv2.VideoCapture(0)
# # delay to ensure stability
# time.sleep(2.0)

#### create array to signify the actions for iterating
# actions to be detected by model
actions = np.array(
    ['A', 'B', 'C', 'D', 'del', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'nothing', 'O', 'P', 'Q', 'R',
     'S', 'space', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])

# build the layout for the model so that we can load in the saved weights
model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(1, 126)))
model.add(LSTM(128, return_sequences=True, activation="relu"))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(actions.shape[0], activation='softmax'))

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..', '..')
model_weights_path = os.path.join(project_root, 'asl_Alphabet_Model_v.0.1.h5')

# load the saved model into the model variable

model.load_weights(model_weights_path)

# used for formatting purposes in order to pass our keypoints to our model
sequence = []

# the current sentence being displayed
sentence = []

# the probability threshold of our models output
# this is used to make sure our model is displaying output that is at least 85% accurate
threshold = 0.85

# detect camera connection
cap = cv2.VideoCapture(0)

@app.route("/video_feed")
def video_feed():
    #return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

def generate_frames():
    global cap, sequence, sentence, threshold
    with mp_hands.Hands(max_num_hands=2, model_complexity=0, min_detection_confidence=0.5,
                        min_tracking_confidence=0.5) as hands:
        detectionFlag = 0
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break
            else:
                frame = cv2.flip(frame, 1)
                image, results = mp_detection(frame, hands)

                # reset count to 30 to effectively wait 30 frames for the next detection
                if detectionFlag == 30:
                    detectionFlag = 0

                if detectionFlag == 0:
                    # grab keypoints from the frame and format them
                    keypoints = formatPoints(results)

                    # add the keypoints to our sequence of keypoints and predict them
                    sequence.append(keypoints)
                    sequence = sequence[-1:]
                    res = model.predict(np.expand_dims(sequence, axis=0))[0]

                    # the output of our model decoded into a letter
                    letter = actions[np.argmax(res)]

                    # how confident our model is in its detection result
                    # represented as a probability
                    probability = res[np.argmax(res)]

                    # discerning output of the model to be displayed
                    if probability > threshold and letter != "nothing":
                        if len(sentence) > 0:
                            if letter == "space":
                                sentence.append("_")
                            elif letter == "del":
                                sentence.pop()
                            else:
                                sentence.append(letter)
                        elif not letter in {"space", "del"}:
                            sentence.append(letter)

                detectionFlag += 1

                # if "d" is pressed on the keyboard, delete the current sentence
                if keyboard.is_pressed("d"):
                    sentence = []

                # output sentence on the screen
                cv2.rectangle(image, (0, 0), (640, 40), (245, 117, 16), -1)
                cv2.putText(image, "".join(sentence), (3, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3,
                            cv2.LINE_AA)

                ret, buffer = cv2.imencode('.jpg', image)
                frame = buffer.tobytes()
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                                                    frame + b'\r\n')

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()

    print("")
    print("program exited")
pass
