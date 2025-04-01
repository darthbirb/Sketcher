import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, Flatten, Dropout, Conv2D, MaxPooling2D
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
import numpy as np
import os

# Paths
DATASET_PATH = "../dataset/quickdraw_dataset"  # Adjusted path
MODEL_PATH = "./quickdraw_resnet_model.h5"
HISTORY_PATH = "./training_history.npy"

# Load Data
X_train = np.load(f"{DATASET_PATH}/X_train.npy")
X_test = np.load(f"{DATASET_PATH}/X_test.npy")
y_train = np.load(f"{DATASET_PATH}/y_train.npy")
y_test = np.load(f"{DATASET_PATH}/y_test.npy")

# Normalize Data
X_train = X_train / 255.0
X_test = X_test / 255.0

# Convert grayscale to 3-channel (required by ResNet)
X_train_rgb = np.repeat(X_train, 3, axis=-1)
X_test_rgb = np.repeat(X_test, 3, axis=-1)

# Load ResNet-18 (using ResNet50 and reducing depth)
base_model = ResNet50(
    input_shape=(96, 96, 3),  # ResNet expects 3 channels
    include_top=False,  # Remove fully connected layer
    weights="imagenet"
)

# Freeze Base Model Layers
base_model.trainable = False

# Build Model
model = Sequential([
    base_model,
    Flatten(),
    Dense(512, activation="relu"),
    Dropout(0.5),
    Dense(10, activation="softmax")  # 10 classes
])

# Compile Model
model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# Train Model
history = model.fit(
    X_train_rgb, y_train,
    epochs=10,
    validation_data=(X_test_rgb, y_test),
    batch_size=32
)

# Evaluate Model
test_loss, test_accuracy = model.evaluate(X_test_rgb, y_test)
print(f"Test Accuracy: {test_accuracy * 100:.2f}%")

# Save Model & Training History
model.save(MODEL_PATH)
np.save(HISTORY_PATH, history.history)

print(f"Model saved at {MODEL_PATH}")
print(f"Training history saved at {HISTORY_PATH}")
