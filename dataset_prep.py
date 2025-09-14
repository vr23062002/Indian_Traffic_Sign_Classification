import os
import zipfile
import cv2
import numpy as np
import splitfolders

# -------------------------------
# Configuration
# -------------------------------
ZIP_PATH = "C:\\Users\\varun\\Downloads\\Amrita Project\\Indian-Traffic-Sign-Dataset(2).zip"
EXTRACT_DIR = "data"
RAW_DIR = os.path.join(EXTRACT_DIR, "Indian-Traffic Sign-Dataset", "Images")
OUTPUT_DIR = "data_split"

# -------------------------------
# Step 1: Unzip the dataset
# -------------------------------
def unzip_dataset():
    if not os.path.exists(EXTRACT_DIR):
        os.makedirs(EXTRACT_DIR)

    with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
        zip_ref.extractall(EXTRACT_DIR)
    print(f"Dataset unzipped to: {EXTRACT_DIR}")

# -------------------------------
# Step 2: Clean corrupt/blank images
# -------------------------------
def clean_images(data_dir):
    removed = 0
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                image = cv2.imread(file_path)
                if image is None:
                    os.remove(file_path)
                    removed += 1
                elif np.all(image == image[0, 0]):  # uniform color = blank
                    os.remove(file_path)
                    removed += 1
            except Exception:
                os.remove(file_path)
                removed += 1
    print(f"Removed {removed} corrupt/blank images.")

# -------------------------------
# Step 3: Split into train/val/test
# -------------------------------
def split_dataset():
    if not os.path.exists(OUTPUT_DIR):
        splitfolders.ratio(RAW_DIR, output=OUTPUT_DIR, seed=1337, ratio=(.8, .1, .1))
        print(f"Dataset split into train/val/test at {OUTPUT_DIR}")
    else:
        print("Split already exists. Skipping.")

# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    unzip_dataset()
    clean_images(RAW_DIR)
    split_dataset()
