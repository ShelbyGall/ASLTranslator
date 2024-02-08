import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import TensorBoard

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

# Load the trained model
model.load_weights('.//asl_Alphabet_Model_v.0.1.h5')

# this is used to make sure our model is displaying output that is at least 85% accurate
threshold = 0.85

# used for drawing landmarks on hand in real time
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


# Josh's method that we need to implement
# ================================================================================================================================
# predict_letter_from_image(image)
#     Input:     image - image to be translated
#     Output:    String     - letter that model predicts from image
# ================================================================================================================================
def predict_letter_from_image(image):
    with mp_hands.Hands(max_num_hands=2, model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:

        # Process the image to get keypoints
        _, results = mp_detection(image, hands)
        keypoints = formatPoints(results)

        # Predict the letter
        if keypoints.size > 0:
            sequence = [keypoints]
            res = model.predict(np.expand_dims(sequence, axis=0))[0]
            letter = actions[np.argmax(res)]
            probability = res[np.argmax(res)]

            # Return the letter if confidence is above threshold
            if probability > threshold and letter != "nothing":
                return letter
        return "No valid letter detected"



# Example usage
#image_path = 'TestImages/testletterF.jpg'
#predicted_letter = predict_letter_from_image(image_path)
#print(f"Predicted letter: {predicted_letter}")
