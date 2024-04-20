import cv2
import numpy as np

def detect_bad_apples(image_path):
    try:
        # Load image
        image = cv2.imread(image_path)
        
        if image is None:
            print("Error: Unable to read the image file.")
            return False

        # Convert image to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Define range of red color in HSV
        lower_red = np.array([0, 100, 100])
        upper_red = np.array([10, 255, 255])
        
        # Threshold the HSV image to get only red colors
        mask = cv2.inRange(hsv, lower_red, upper_red)
        
        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Check if any contours are found
        if contours:
            for contour in contours:
                # Calculate area of contour
                area = cv2.contourArea(contour)
                
                # If contour area is greater than a threshold, consider it as a bad apple
                if area > 1000:
                    return True
        return False

    except Exception as e:
        print("Error:", e)
        return False

# Test the function with an image
image_path = r"C:\Users\joshu\Documents\Hackathon\OpenCV\apple5.jpg"  # Replace with the path to your image
if detect_bad_apples(image_path):
    print("The apple has gone bad.")
else:
    print("The apple is fresh.")
