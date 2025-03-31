import numpy as np
import tensorflow as tf
import os
import glob
from sklearn.model_selection import train_test_split

# Constants
DATASET_DIR = "dataset/quickdraw_dataset/raw_categories"
IMG_SIZE = 96  # MobileNetV3 expects 96x96
NUM_SAMPLES_PER_CLASS = 10000  # Adjust as needed

# Load dataset
def load_data():
    X, y, class_names = [], [], []

    for idx, file in enumerate(glob.glob(os.path.join(DATASET_DIR, "*.npy"))):
        class_name = os.path.basename(file).replace(".npy", "")
        class_names.append(class_name)

        data = np.load(file)  # Load .npy file
        data = data[:NUM_SAMPLES_PER_CLASS]  # Limit number of samples

        X.extend(data)
        y.extend([idx] * len(data))

    X = np.array(X) / 255.0  # Normalize pixel values (0-1)
    X = X.reshape(-1, 28, 28, 1)  # Reshape to (28x28 grayscale)
    y = np.array(y)  # Convert labels to numpy array

    return X, y, class_names

# Preprocess dataset
X, y, CLASS_NAMES = load_data()
np.save("dataset/class_names.npy", CLASS_NAMES)

# Resize images to 96x96 for MobileNetV3
X_resized = tf.image.resize(X, (IMG_SIZE, IMG_SIZE)).numpy()

# Split into train & test sets
X_train, X_test, y_train, y_test = train_test_split(X_resized, y, test_size=0.2, random_state=42)

# Save processed dataset
np.save("dataset/quickdraw_dataset/X_train.npy", X_train)
np.save("dataset/quickdraw_dataset/X_test.npy", X_test)
np.save("dataset/quickdraw_dataset/y_train.npy", y_train)
np.save("dataset/quickdraw_dataset/y_test.npy", y_test)

print(f"Dataset prepared: {len(X_train)} train samples, {len(X_test)} test samples.")
