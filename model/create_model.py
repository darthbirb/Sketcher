import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam

# Define constants
IMG_SIZE = 96  # Input image size
NUM_CLASSES = 10  # Number of categories

# Get the absolute path of the dataset directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Go up one level to Sketcher/
DATASET_DIR = os.path.join(BASE_DIR, "dataset", "quickdraw_dataset")  # Absolute path to dataset
MODEL_DIR = os.path.dirname(__file__)  # Save model in the same folder as this script

# Load the dataset
X_train = np.load(os.path.join(DATASET_DIR, "X_train.npy"))
X_test = np.load(os.path.join(DATASET_DIR, "X_test.npy"))
y_train = np.load(os.path.join(DATASET_DIR, "y_train.npy"))
y_test = np.load(os.path.join(DATASET_DIR, "y_test.npy"))

# Normalize the images
X_train = X_train / 255.0
X_test = X_test / 255.0

# Reshape images to add a channel dimension (since we're using Conv2D)
X_train = X_train.reshape(-1, IMG_SIZE, IMG_SIZE, 1)  # Shape (N, 96, 96, 1)
X_test = X_test.reshape(-1, IMG_SIZE, IMG_SIZE, 1)  # Shape (N, 96, 96, 1)

# Build the custom CNN model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 1)),
    BatchNormalization(),
    MaxPooling2D((2, 2)),

    Conv2D(64, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),

    Conv2D(128, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),

    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(NUM_CLASSES, activation='softmax')
])

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.0001),
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])

# Train the model
history = model.fit(X_train, y_train, epochs=20, validation_data=(X_test, y_test), batch_size=32)

# Evaluate the model
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {test_accuracy * 100:.2f}%")

# Save the trained model
model_save_path = os.path.join(MODEL_DIR, "quickdraw_cnn.h5")
model.save(model_save_path)
print(f"Model trained and saved at {model_save_path}")

# Save training history
history_save_path = os.path.join(MODEL_DIR, "training_history.npy")
np.save(history_save_path, history.history)
print(f"Training history saved at {history_save_path}")
