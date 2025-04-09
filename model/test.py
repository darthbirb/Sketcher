import numpy as np
import os
import random
from PIL import Image

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "dataset", "quickdraw_dataset")

# Load the training data
X_train = np.load(os.path.join(DATA_DIR, "X_train.npy"))
y_train = np.load(os.path.join(DATA_DIR, "y_train.npy"))
class_names = np.load(os.path.join(DATA_DIR, "class_names.npy"))

# Function to visualize a random image of the category "smiley face"
def visualize_smiley_face_image():
    # Get the index for the "smiley face" category
    smiley_face_index = np.where(class_names == "The Eiffel Tower")[0]

    if smiley_face_index.size == 0:
        print("Category 'smiley face' not found.")
        return

    # Filter the training data for "smiley face" images
    smiley_face_indices = np.where(y_train == smiley_face_index[0])[0]

    if smiley_face_indices.size == 0:
        print("No images found for the category 'smiley face'.")
        return

    # Select a random index from the filtered indices
    random_index = random.choice(smiley_face_indices)
    
    # Get the image and label
    image = X_train[random_index]
    label = y_train[random_index]
    class_name = class_names[label]

    # Convert the image to a PIL Image for saving
    image_pil = Image.fromarray((image.squeeze() * 255).astype(np.uint8), mode='L')

    # Save the image as a PNG file
    output_path = os.path.join(DATA_DIR, f"image.png")
    image_pil.save(output_path)

    print(f"Saved random image of class '{class_name}' to '{output_path}'")

if __name__ == "__main__":
    visualize_smiley_face_image()