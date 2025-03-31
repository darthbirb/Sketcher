import tensorflow as tf
from tensorflow.keras.applications import MobileNetV3Small
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
import numpy as np
import os

# Constants
IMG_SIZE = 96  # MobileNetV3 input size (96x96)
NUM_CLASSES = 10  # Number of categories (based on your 10 categories)
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # Going up to the Sketcher folder
TRAIN_DIR = os.path.join(PROJECT_DIR, "dataset", "quickdraw_dataset")

# Load the data (X_train, X_test, y_train, y_test)
X_train = np.load(os.path.join(TRAIN_DIR, "X_train.npy"))
X_test = np.load(os.path.join(TRAIN_DIR, "X_test.npy"))
y_train = np.load(os.path.join(TRAIN_DIR, "y_train.npy"))
y_test = np.load(os.path.join(TRAIN_DIR, "y_test.npy"))

# Normalize data (it's already normalized, but confirming)
X_train = X_train / 255.0
X_test = X_test / 255.0

# Convert grayscale images to RGB (3 channels)
X_train_rgb = np.repeat(X_train, 3, axis=-1)
X_test_rgb = np.repeat(X_test, 3, axis=-1)

# Load MobileNetV3 (pre-trained on ImageNet)
base_model = MobileNetV3Small(input_shape=(IMG_SIZE, IMG_SIZE, 3), include_top=False, weights="imagenet")

# Freeze the base layers (do not train them)
base_model.trainable = False

# Create the custom model
model = Sequential([
    base_model,
    Flatten(),
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(NUM_CLASSES, activation='softmax')  # Output layer for classification
])

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.0001),
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])

# Train the model
history = model.fit(X_train_rgb, y_train, epochs=10, validation_data=(X_test_rgb, y_test), batch_size=32)

# Evaluate the model on the test data
test_loss, test_accuracy = model.evaluate(X_test_rgb, y_test)
print(f"Test Accuracy: {test_accuracy * 100:.2f}%")

# Save the trained model
model_save_path = os.path.join(TRAIN_DIR, "mobilenetv3_quickdraw_model.h5")
model.save(model_save_path)
print(f"Model trained and saved successfully at {model_save_path}")

# Save training history (optional, useful for later analysis)
history_save_path = os.path.join(TRAIN_DIR, "training_history.npy")
np.save(history_save_path, history.history)
print(f"Training history saved at {history_save_path}")
