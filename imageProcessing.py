import cv2
import numpy as np
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# ================================================================================================================================
# mp_detection(image, model)
#     Input:     image - the image from openCV of our webcam
#                model - the hands mediapipe model
#     Output:    image - the image from openCV of our webcam
#                results - the output results from the hands model from our current image
# ================================================================================================================================
def mp_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = model.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results



# ================================================================================================================================
# draw_styled_landmarks(image, handLandmarks)
#     Input:     image - the image from openCV of our webcam
#                handLandmarks - all of the landmark data from results.multi_hand_landmarks[i].landmark
#     Output:    None - draws the keypoints to the hand to be displayed on 
#                       on the screen
# ================================================================================================================================
def draw_styled_landmarks(image, handLandmarks):
    mp_drawing.draw_landmarks(image, 
                              handLandmarks, 
                              mp_hands.HAND_CONNECTIONS, 
                              mp_drawing_styles.get_default_hand_landmarks_style(),
                              mp_drawing_styles.get_default_hand_connections_style()
                             )



# ================================================================================================================================
# extractPoints(results)
#     Input:     results - all of the landmark data outputted from the hands model
#     Output:    array - formatted numpy array for both the left and right hand landmark points 
#                        to be passed to our model for detecting asl letters
# ================================================================================================================================
def formatPoints(results):
    left = []
    right = []
    # check if last fram has hands included in it
    if results.multi_hand_landmarks:
        # check the number of hands
        if len(results.multi_handedness) == 2:
            # -----2 hands------
            # print("two hands!")
            left = np.array([[lLand.x, lLand.y, lLand.z] for lLand in results.multi_hand_landmarks[0].landmark]).flatten()
            right = np.array([[rLand.x, rLand.y, rLand.z] for rLand in results.multi_hand_landmarks[1].landmark]).flatten()
            
        else:
            # -----1 hand------
            # print("one hand!")
            # check if the one hand is right or left
            if results.multi_handedness[0].classification[0].label == "Right":
                right = np.array([[rLand.x, rLand.y, rLand.z] for rLand in results.multi_hand_landmarks[0].landmark]).flatten()
                left = np.zeros(21*3)
            else:
                left = np.array([[lLand.x, lLand.y, lLand.z] for lLand in results.multi_hand_landmarks[0].landmark]).flatten()
                right = np.zeros(21*3)
    else:
        # -----no hands------
        # print("Last frame included no hands")
        left = np.zeros(21*3)
        right = np.zeros(21*3)
        
    return np.concatenate([left, right])
