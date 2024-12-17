import os
import cv2
import numpy as np

def detect_bad_apples(image_path):
    try:
        # Confirm file existence
        if not os.path.exists(image_path):
            print(f"File does not exist: {image_path}")
            return None

        # Load image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Unable to read the image file: {image_path}")
            return None

        # Convert image to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define range for brown color in HSV
        # Brown is usually a mix of red, orange, and low saturation
        lower_brown = np.array([10, 50, 20])  # Lower bound for hue, saturation, and value
        upper_brown = np.array([30, 255, 200])  # Upper bound for hue, saturation, and value

        # Threshold the image to create a mask for brown areas
        brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)

        # Find contours in the mask
        contours, _ = cv2.findContours(brown_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Calculate total brown area
        total_brown_area = sum(cv2.contourArea(c) for c in contours)

        # Define threshold for brown area to classify as bad apple
        return "Bad Apple" if total_brown_area > 500 else "Fresh Apple"

    except Exception as e:
        print("Error:", e)
        return None

# Folder containing the apple images
folder_path = r"C:/Users/joshu/Documents/Software Development/Hackathon/OpenCV/" # Change the file path for your images

# Get all image files from the folder
image_extensions = ['.jpg', '.jpeg', '.png']
image_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) 
               if os.path.splitext(f)[1].lower() in image_extensions]

# Process each image
for image_path in image_paths:
    print(f"Processing: {image_path}")
    result = detect_bad_apples(image_path)
    if result:
        print(f"Result for {os.path.basename(image_path)}: {result}")
    else:
        print(f"Could not process image: {os.path.basename(image_path)}")

