import cv2
import numpy as np
import os
import time
import keyboard
from imageProcessing import mp_detection, formatPoints, draw_styled_landmarks, mp_hands
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import TensorBoard

#### create array to signify the actions for iterating
# actions to be detected by model
actions = np.array(['A', 'B', 'C', 'D', 'del', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'nothing', 'O', 'P', 'Q', 'R', 'S', 'space', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])

# build the layout for the model so that we can load in the saved weights
model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(1,126)))
model.add(LSTM(128, return_sequences=True, activation="relu"))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(actions.shape[0], activation='softmax'))

# load the saved model into the model variable
model.load_weights('.//asl_Alphabet_Model_v.0.1.h5')

# used for formatting purposes in order to pass our keypoints to our model
sequence = []

# the current sentence being displayed 
sentence = []

# the probability threshold of our models output
# this is used to make sure our model is displaying output that is at least 85% accurate
threshold = 0.85

# detect camera connection
cap = cv2.VideoCapture(0)

# the time to wait if cap doesnt recognize a camera connection
if not cap.isOpened():
    # waitTime is our grace period for when camera is not init. detected
    waitTime = 30
    print(f"PROGRAM INTERRUPT: no camera detected - program will exit in {waitTime} seconds if no camera is connected")
    # loop to cleanly print to console during grace period
    for sec in range(waitTime):
        # wait one second 
        time.sleep(1)
        # cleanly print countdown to console 
        print(f"Program exits in: {waitTime - sec} sec ", end="")
        print("\r", end="")
        # check if camera is connected 
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("")
            print(f"camera detected\t\t")
            break

with mp_hands.Hands(max_num_hands=2, model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    detectionFlag = 0
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        image, results = mp_detection(frame, hands)
        
        # # draws the points onto the hand
        # if results.multi_hand_landmarks:
        #     for hand_landmarks in results.multi_hand_landmarks:
        #         # just draws visual on frame so we can display it later
        #         draw_styled_landmarks(image, hand_landmarks)

        # reset count to 30 to effectively wait 30 frames for the next detection
        if detectionFlag == 30:
            detectionFlag = 0
    
        if detectionFlag == 0:
            # grab keypoints from the frame and format them
            keypoints = formatPoints(results)

            # add the keypoints to our sequence of keypoints and predict them
            sequence.append(keypoints)
            sequence = sequence[-1:]
            res = model.predict(np.expand_dims(sequence,axis=0))[0]

            # the output of our model decoded into a letter
            letter = actions[np.argmax(res)] 
            
            # how confident our model is in its detection result
            # represented as a probability
            probability = res[np.argmax(res)]

            
            # discerning output of model to be displayed
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

        # if "d" is pressed on keyboard delete current sentence
        if keyboard.is_pressed("d"):
            sentence = []

        # output sentence on the screen
        cv2.rectangle(image, (0,0), (640,40), (245,117,16),-1)
        cv2.putText(image, "".join(sentence),(3,30), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255), 3, cv2.LINE_AA)

        # switch second arg of imshow to image or frame
        # frame: no drawing
        # image: drawing
        cv2.imshow('OpenCV Feed', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

print("")
print("program exited")