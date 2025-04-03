from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import base64
import cv2
import io
from PIL import Image
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

def preprocess_image(image_data):
    image = Image.open(io.BytesIO(base64.b64decode(image_data))).convert('L')
    image = image.resize((28, 28))  # Adjust based on model input size
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