import cv2
import numpy as np
import os
from imageProcessing import mp_detection, formatPoints, draw_styled_landmarks, mp_hands
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import TensorBoard




#### create array to signify the actions for iterating

# actions to be detected by model
actions = np.array(['A', 'B', 'C', 'D', 'del', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'nothing', 'O', 'P', 'Q', 'R', 'S', 'space', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])



log_dir = os.path.join('Logs')
tb_callback = TensorBoard(log_dir=log_dir)

model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(1,126)))
model.add(LSTM(128, return_sequences=True, activation="relu"))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(actions.shape[0], activation='softmax'))


model.load_weights('.//asl_Alphabet_Model_v.0.1.h5')

sequence = []
sentence = []
threshold = 0.7

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("no camera")
    
with mp_hands.Hands(max_num_hands=2, model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        image, results = mp_detection(frame, hands)
        
        # # draws the points onto the hand
        # if results.multi_hand_landmarks:
        #     for hand_landmarks in results.multi_hand_landmarks:
        #         # just draws visual on frame so we can display it later
        #         draw_styled_landmarks(image, hand_landmarks)
        
        # get hand landmark points and format them 
        keypoints = formatPoints(results)
        sequence.insert(0, keypoints)
        sequence= sequence[:1]
        res = model.predict(np.expand_dims(sequence,axis=0))[0]
    
        if res[np.argmax(res)] > threshold and actions[np.argmax(res)] != "nothing":
            if len(sentence) > 1 and actions[np.argmax(res)] != sentence[-1]:
                sentence.append(actions[np.argmax(res)])
            else:
                sentence.append(actions[np.argmax(res)])

        if len(sentence) > 5:
            sentence = sentence[-5:]

        cv2.rectangle(image, (0,0), (640,40), (245,117,16),-1)
        cv2.putText(image, " ".join(sentence),(3,30), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255), 3, cv2.LINE_AA)

        # switch second arg of imshow to image or frame
        # frame: no drawing
        # image: drawing
        cv2.imshow('OpenCV Feed', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()