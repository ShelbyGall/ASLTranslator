import os
import random
import cv2
from PredictLetter import predict_letter_from_image, actions

# The directory where the test images are stored, organized by letter
test_images_dir = "TestImages"

# The number of images to evaluate for each letter
num_images_to_test_per_letter = 100

# Generate a list of uppercase letters from A to Z. Same as A, B, C, ect
letters = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

def main():
    # Create a dictionary to store the results: correct and incorrect counts for each letter
    results = {letter: {'correct': 0, 'incorrect': 0} for letter in letters}

    # Iterate over each letter 
    for letter in letters:
        print(f"Processing letter: {letter}")
        # Path to the folder containing images for the current letter
        letter_dir = os.path.join(test_images_dir, letter)
        # Check if the directory exists; if not, skip to the next letter
        if not os.path.isdir(letter_dir):
            print(f"Directory for letter '{letter}' not found.")
            continue

        # List all image files (jpg, png, jpeg) in the letter's directory.
        all_images = [f for f in os.listdir(letter_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        # Keep track of which images have been tested to avoid repetition
        tested_images = set()

        # Continue selecting and testing images until num_images_to_test_per_letter valid images have been evaluated or all images have been attempted
        while len(tested_images) < num_images_to_test_per_letter and len(tested_images) < len(all_images):
            # Randomly select an image from the list
            image_name = random.choice(all_images)
            if image_name in tested_images:
                continue  # Skip if this image has already been tested
            image_path = os.path.join(letter_dir, image_name)
            # read the actual image into the code using openCV
            img = cv2.imread(image_path)
            # Call prediction function to get the predicted letter for the image
            predicted_letter = predict_letter_from_image(img)
            
            # Only count the image if keypoints were detected otherwise choose another image
            if predicted_letter != "No valid letter detected":
                tested_images.add(image_name)  # Add image to tested
                if predicted_letter == letter:
                    results[letter]['correct'] += 1  # Correct
                else:
                    results[letter]['incorrect'] += 1  # incorrect 

    # Print results
    for letter, result in results.items():
        total_tested = result['correct'] + result['incorrect']
        percentage_correct = (result['correct'] / total_tested) * 100
        print(f"Results for letter '{letter}':")
        print(f"  Correct: {result['correct']} ({percentage_correct:.2f}%)")
        print(f"  Incorrect: {result['incorrect']}")

if __name__ == "__main__":
    main()
