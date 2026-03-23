import os
import shutil
import pandas as pd
from pathlib import Path
from tqdm import tqdm

# ──── Adjust these paths ────────────────────────────────────────
ORIGINAL_IMAGES_ROOT = "/home/yash/A. RFMiD_All_Classes_Dataset/1. Original Images"
TRAIN_CSV   = "/home/yash/A. RFMiD_All_Classes_Dataset/2. Groundtruths/a. RFMiD_Training_Labels.csv"
VALID_CSV   = "/home/yash/A. RFMiD_All_Classes_Dataset/2. Groundtruths/b. RFMiD_Validation_Labels.csv"
TEST_CSV    = "/home/yash/A. RFMiD_All_Classes_Dataset/2. Groundtruths/c. RFMiD_Testing_Labels.csv"

TARGET_ROOT = "/home/yash/rfmid_imagefolder"

# ─────────────────────────────────────────────────────────────────

def organize_split(csv_path, split_name):
    df = pd.read_csv(csv_path)
    src_dir = os.path.join(ORIGINAL_IMAGES_ROOT, split_name)
    
    for _, row in tqdm(df.iterrows(), total=len(df), desc=f"Organizing {split_name}"):
        img_name = f"{row['ID']}.png"  # assuming filenames are ID.png – CHECK THIS!
        label    = int(row["ARMD"])
        
        src_path = os.path.join(src_dir, img_name)
        if not os.path.isfile(src_path):
            print(f"Missing: {src_path}")
            continue
        
        dst_folder = os.path.join(TARGET_ROOT, split_name, str(label))
        os.makedirs(dst_folder, exist_ok=True)
        
        dst_path = os.path.join(dst_folder, img_name)
        
        # Option 1: copy           → uses more space but safest
        shutil.copy2(src_path, dst_path)
        
        # Option 2: hard link      → saves space (if same filesystem)
        # os.link(src_path, dst_path)
        
        # Option 3: symlink        → symbolic link (most space efficient)
        # os.symlink(src_path, dst_path)

# Run for train & valss
organize_split(TRAIN_CSV,  "a. Training Set")
organize_split(VALID_CSV,  "b. Validation Set")
organize_split(TEST_CSV,   "c. Testing Set")

print("Done. You can now use:")
print(f"  --data_path {TARGET_ROOT}")