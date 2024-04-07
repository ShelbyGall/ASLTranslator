import os
import cv2
import mediapipe as mp
from collections import defaultdict


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5) #idk detection conf

base_dir = r'C:\Users\joshu\OneDrive\Desktop\ASLimages'

# Dict  name, letter, # missing
no_landmarks_count = defaultdict(int)

# List of paths without landmarks
images_without_landmarks_paths = []

for folder in os.listdir(base_dir):
    if folder not in [chr(i) for i in range(ord('A'), ord('Z')+1)] + ['DEL', 'SPACE']:
        continue
    folder_path = os.path.join(base_dir, folder)
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)
        if not os.path.isdir(subfolder_path):
            continue
        # Initialize count for subfolder
        no_landmarks_count[subfolder + ' ' + folder] = 0
        for filename in os.listdir(subfolder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(subfolder_path, filename)
                image = cv2.imread(image_path)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image)
                if not results.multi_hand_landmarks:
                    #dict update
                    no_landmarks_count[subfolder + ' ' + folder] += 1
                    #list paths update
                    images_without_landmarks_paths.append(image_path)


# name, letter, # missing
output_file_path = os.path.join(base_dir, 'missing_landmarks_report.txt')
with open(output_file_path, 'w') as file:
    for label, count in no_landmarks_count.items():
        file.write(f'{label}: {count} images without landmarks\n')

# path of images without landmarks
images_paths_file_path = os.path.join(base_dir, 'images_without_landmarks_paths.txt')
with open(images_paths_file_path, 'w') as file:
    for path in images_without_landmarks_paths:
        file.write(f'{path}\n')

print("Check 'missing_landmarks_report.txt' and 'images_without_landmarks_paths.txt' for the reports.")
