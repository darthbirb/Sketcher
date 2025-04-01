import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau

# Define constants
IMG_SIZE = 96  # Input image size
NUM_CLASSES = 10  # Number of categories

# Get dataset paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATASET_DIR = os.path.join(BASE_DIR, "dataset", "quickdraw_dataset")
MODEL_DIR = os.path.dirname(__file__)

# Load dataset
X_train = np.load(os.path.join(DATASET_DIR, "X_train.npy"))
X_test = np.load(os.path.join(DATASET_DIR, "X_test.npy"))
y_train = np.load(os.path.join(DATASET_DIR, "y_train.npy"))
y_test = np.load(os.path.join(DATASET_DIR, "y_test.npy"))

# Normalize images
X_train = X_train / 255.0
X_test = X_test / 255.0

# Reshape images
X_train = X_train.reshape(-1, IMG_SIZE, IMG_SIZE, 1)
X_test = X_test.reshape(-1, IMG_SIZE, IMG_SIZE, 1)

# Define CNN model with improvements
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 1)),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.25),  # Added dropout

    Conv2D(64, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.25),  # Added dropout

    Conv2D(64, (3, 3), activation='relu'),  # Reduced complexity
    BatchNormalization(),
    MaxPooling2D((2, 2)),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),  # Strong dropout to reduce overfitting
    Dense(NUM_CLASSES, activation='softmax')
])

# Reduce learning rate if validation loss stops improving
lr_scheduler = ReduceLROnPlateau(monitor="val_loss", patience=3, factor=0.5, verbose=1)

# Compile model
model.compile(optimizer=Adam(learning_rate=5e-5),  # Lower learning rate
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])

# Train the model with scheduler
history = model.fit(X_train, y_train, epochs=20, validation_data=(X_test, y_test),
                    batch_size=32, callbacks=[lr_scheduler])

# Evaluate model
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {test_accuracy * 100:.2f}%")

# Save model
model.save(os.path.join(MODEL_DIR, "quickdraw_cnn.h5"))
np.save(os.path.join(MODEL_DIR, "training_history.npy"), history.history)

print(f"Model saved at {MODEL_DIR}")
