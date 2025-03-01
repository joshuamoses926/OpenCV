from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import os

# Initialize Flask app
app = Flask(__name__)

# Define upload folder and create it if it doesn't exist
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to detect bad apples based on image analysis
def detect_bad_apples(image_path):
    try:
        # Read the uploaded image
        image = cv2.imread(image_path)
        if image is None:
            return "Error: Unable to read the image."

        # Convert the image to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define HSV range for brown color (potential rot on apples)
        lower_brown = np.array([10, 50, 20])
        upper_brown = np.array([30, 255, 200])

        # Create a mask to isolate brown regions in the image
        brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)

        # Find contours in the mask
        contours, _ = cv2.findContours(brown_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Calculate the total brown area by summing the contour areas
        total_brown_area = sum(cv2.contourArea(c) for c in contours)
        
        # If the brown area exceeds a threshold, classify as "Bad Apple"
        return "Bad Apple" if total_brown_area > 500 else "Fresh Apple"
    except Exception as e:
        return f"Error: {str(e)}"

# Route to serve the homepage with the HTML form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle image upload and return freshness result
@app.route('/upload', methods=['POST'])
def upload():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    
    # Get the uploaded file
    file = request.files['file']
    
    # Check if the file has a valid name
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    # Save the uploaded file to the server
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Analyze the image to determine if the apple is fresh or bad
    result = detect_bad_apples(filepath)
    
    # Delete the uploaded file after processing
    os.remove(filepath)
    
    # Return the result as a JSON response
    return jsonify({'result': result})

# Run the app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
