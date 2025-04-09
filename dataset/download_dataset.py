import os
import urllib.request

SAVE_DIR = "quickdraw_dataset/raw_categories"
os.makedirs(SAVE_DIR, exist_ok=True)

CATEGORIES_URL = "https://raw.githubusercontent.com/googlecreativelab/quickdraw-dataset/master/categories.txt"

def download_categories():
    print("Downloading category list...")
    response = urllib.request.urlopen(CATEGORIES_URL)
    raw_text = response.read().decode('utf-8')
    categories = raw_text.strip().split("\n")
    return categories

def download_npy_files(categories):
    for category in categories:
        formatted = category.replace(" ", "%20")
        file_url = f"https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap/{formatted}.npy"
        save_path = os.path.join(SAVE_DIR, f"{category}.npy")
        
        if os.path.exists(save_path):
            print(f"Already exists: {category}")
            continue
        
        try:
            print(f"Downloading {category}...")
            urllib.request.urlretrieve(file_url, save_path)
        except Exception as e:
            print(f"Failed to download {category}: {e}")

if __name__ == "__main__":
    categories = download_categories()
    download_npy_files(categories)
