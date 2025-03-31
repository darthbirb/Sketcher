import os
import requests

# List of 10 categories
categories = [
    "cat", "dog", "car", "bicycle", "airplane",
    "tree", "house", "fish", "apple", "mug"
]

# Dataset storage folder
DATA_DIR = "quickdraw_dataset"
os.makedirs(DATA_DIR, exist_ok=True)

# Download function
def download_file(category):
    url = f"https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/{category}.npy"
    file_path = os.path.join(DATA_DIR, f"{category}.npy")

    if os.path.exists(file_path):
        print(f"{category}.npy already exists. Skipping...")
        return

    print(f"Downloading {category}.npy...")
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded {category}.npy ✅")
    else:
        print(f"Failed to download {category}.npy ❌")

# Download each category
for category in categories:
    download_file(category)

print("All downloads completed! 🚀")
