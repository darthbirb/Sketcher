import os
import numpy as np
from sklearn.model_selection import train_test_split

RAW_DATA_DIR = "quickdraw_dataset/raw_categories"
PROCESSED_DATA_DIR = "quickdraw_dataset"
NUM_SAMPLES_PER_CLASS = 2000

os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

X = []
y = []
class_names = []

category_files = sorted(os.listdir(RAW_DATA_DIR))

print("Preparing dataset...")

for idx, file_name in enumerate(category_files):
    class_name = file_name.replace(".npy", "")
    file_path = os.path.join(RAW_DATA_DIR, file_name)
    
    try:
        data = np.load(file_path)
        data = data[:NUM_SAMPLES_PER_CLASS] 
        X.append(data)
        y.append(np.full(len(data), idx))
        class_names.append(class_name)
        print(f"Loaded {len(data)} samples for '{class_name}'")
    except Exception as e:
        print(f"Error loading {file_name}: {e}")

X = np.concatenate(X, axis=0).reshape(-1, 28, 28, 1).astype("float32") / 255.0
y = np.concatenate(y, axis=0)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

np.save(os.path.join(PROCESSED_DATA_DIR, "X_train.npy"), X_train)
np.save(os.path.join(PROCESSED_DATA_DIR, "y_train.npy"), y_train)
np.save(os.path.join(PROCESSED_DATA_DIR, "X_test.npy"), X_test)
np.save(os.path.join(PROCESSED_DATA_DIR, "y_test.npy"), y_test)
np.save(os.path.join(PROCESSED_DATA_DIR, "class_names.npy"), np.array(class_names))

print(f"\nSaved processed dataset:")
print(f" - {len(X_train)} training samples")
print(f" - {len(X_test)} testing samples")
print(f" - {len(class_names)} classes")
