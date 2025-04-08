from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import base64
import cv2
import io
from PIL import Image, ImageOps
import os

app = Flask(__name__)
CORS(app)  # Allow requests from frontend

# Define base directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MODEL_DIR = os.path.join(BASE_DIR, "model")
DATASET_DIR = os.path.join(BASE_DIR, "dataset", "quickdraw_dataset")

# Load the trained model
model = load_model(os.path.join(MODEL_DIR, "quickdraw_cnn.h5"))
class_names = np.load(os.path.join(DATASET_DIR, "class_names.npy"))

def crop_and_center(image, target_size=(28, 28)):
    # Convert to numpy and get non-zero (stroke) pixel coordinates
    np_img = np.array(image)
    non_zero = np.argwhere(np_img < 255)  # stroke pixels (assuming white background)

    if non_zero.size == 0:
        return image.resize(target_size)  # fallback

    # Get bounding box
    top_left = non_zero.min(axis=0)
    bottom_right = non_zero.max(axis=0)
    
    # Crop image
    cropped = image.crop((top_left[1], top_left[0], bottom_right[1]+1, bottom_right[0]+1))

    # Create new square image and paste centered
    square = Image.new('L', cropped.size, 255)
    square_size = max(cropped.size)
    new_img = Image.new('L', (square_size, square_size), 255)
    new_img.paste(cropped, ((square_size - cropped.width) // 2, (square_size - cropped.height) // 2))

    return new_img.resize(target_size)

def preprocess_image(image_data):
    # Decode and convert to grayscale (L mode)
    image = Image.open(io.BytesIO(base64.b64decode(image_data))).convert('L')

    # Invert: make strokes white (255), background black (0)
    image = ImageOps.invert(image)

    # Crop and center the drawing
    image = crop_and_center(image, target_size=(28, 28))

    # Normalize and reshape
    image = np.array(image) / 255.0
    image = image.reshape(1, 28, 28, 1)
    return image


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({"error": "No image data provided"}), 400

    image = preprocess_image(data['image'])
    predictions = model.predict(image)
    top_3_indices = np.argsort(predictions[0])[-3:][::-1]
    top_3_labels = [(class_names[i], float(predictions[0][i])) for i in top_3_indices]

    return jsonify({"predictions": top_3_labels})

if __name__ == '__main__':
    app.run(debug=True)