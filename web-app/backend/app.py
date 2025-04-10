from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import base64
import io
from PIL import Image, ImageOps
import os

app = Flask(__name__)

# Restricting CORS
CORS(app, resources={r"/*": {"origins": "https://darthbirb-sketcher.web.app"}})

# Loading the model and classes
model = load_model("quickdraw_cnn.h5")
class_names = np.load("class_names.npy")

def crop_and_center(image, target_size=(26, 26)):
    
    np_img = np.array(image)
    # Get non-zero (stroke) pixel coordinates
    non_zero = np.argwhere(np_img < 255)

    # If canvas is empty (not necessary, just as a failsafe)
    if non_zero.size == 0:
        return Image.new('L', (target_size[0] + 2, target_size[1] + 2), 255)

    # Get the bounding box of the drawing
    top_left = non_zero.min(axis=0)
    bottom_right = non_zero.max(axis=0)
    
    # Crop image to the bounding box
    cropped = image.crop((top_left[1], top_left[0], bottom_right[1] + 1, bottom_right[0] + 1))

    # Create a new white square image
    square_size = max(cropped.size)
    new_img = Image.new('L', (square_size, square_size), 255)
    
    # Paste the cropped image centered into the new image
    new_img.paste(cropped, ((square_size - cropped.width) // 2, (square_size - cropped.height) // 2))

    # Resize to target size before padding (26x26)
    resized_img = new_img.resize(target_size)

    # Add a 1-pixel padding around the resized image
    padded_img = ImageOps.expand(resized_img, border=1, fill=255)

    return padded_img

def preprocess_image(image_data):

    image = Image.open(io.BytesIO(base64.b64decode(image_data))).convert('L')

    image = crop_and_center(image, target_size=(26, 26))

    # Inverting white/black to match the dataset 
    image = ImageOps.invert(image)

    # ONLY FOR DEBUGGING: Save the modified image
    #image.save("image.png")

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