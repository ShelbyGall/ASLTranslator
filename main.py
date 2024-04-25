import time
import keyboard


# the current sentence being displayed 
sentence = []

detectionFlag = 0

import PredictLetter as pl
model = pl.model
cv2 = pl.cv2
mp_detection = pl.mp_detection
formatPoints = pl.formatPoints
mp_hands = pl.mp_hands
actions = pl.actions
np = pl.np
threshold = pl.threshold

def ASLdetection(frame):
    with mp_hands.Hands(max_num_hands=2, model_complexity=0, min_detection_confidence=0.5,
                        min_tracking_confidence=0.5) as hands:
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

        return image
pass

# checks if camera connection is on
def camCheck(cap):
    # the time to wait if cap doesnt recognize a camera connection
    if not cap.isOpened():
        # waitTime is our grace period for when camera is not init. detected
        waitTime = 30
        print(
            f"PROGRAM INTERRUPT: no camera detected - program will exit in {waitTime} seconds if no camera is connected")
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
    elif cap.isOpened():
        print("Camera Detected")
pass

def releaseCam():
    # switch second arg of imshow to image or frame
    # frame: no drawing
    # image: drawing
    #cv2.imshow('OpenCV Feed', image)
    # if cv2.waitKey(10) & 0xFF == ord('q'):
    #     break
    cap.release()
    cv2.destroyAllWindows()
    print("")
    print("program exited")
pass

cap = cv2.VideoCapture(0)
camCheck(cap)

while True:
    _, frame = cap.read()
    if keyboard.is_pressed("c"):
        sentence = []
    if detectionFlag == 60:
        detectionFlag = 0
        letter = pl.predict_letter_from_image(frame)
        if letter == 'del':
            sentence.pop()
        elif letter == "space":
            sentence.append(" ")
        elif letter != 'nothing':
            sentence.append(letter)

    # output sentence on the screen
    cv2.flip(frame,1)
    cv2.rectangle(frame, (0, 0), (640, 40), (0, 0, 0), -1)
    if sentence:
        cv2.putText(frame, "".join(sentence), (3, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                    cv2.LINE_AA)
    cv2.imshow("ASL Detector", frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    detectionFlag+=1

releaseCam()


