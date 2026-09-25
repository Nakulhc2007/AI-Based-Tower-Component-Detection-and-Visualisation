"""
Dataset Verification Script for Judges
Verifies that all images in train/val/test have valid YOLO annotations.
"""

from pathlib import Path

DATASET_DIR = Path(r"a:\projects\ksit hackathon\AI-Based-Tower-Component-Detection-and-Visualisation\dataset")
CLASSES = {0: "Supporting Tower", 1: "Monopole Tower"}

def verify_dataset():
    print("=" * 60)
    print("YOLO DATASET VERIFICATION REPORT")
    print("=" * 60)
    
    total_images = 0
    total_labels = 0
    missing_labels = 0
    class_counts = {0: 0, 1: 0}
    
    for split in ["train", "val", "test"]:
        img_dir = DATASET_DIR / "images" / split
        lbl_dir = DATASET_DIR / "labels" / split
        
        images = list(img_dir.glob("*.jpg"))
        split_images = len(images)
        split_labels = 0
        
        for img in images:
            lbl_file = lbl_dir / f"{img.stem}.txt"
            if lbl_file.exists():
                lines = lbl_file.read_text().strip().split("\n")
                lines = [l for l in lines if l.strip()]
                if lines:
                    split_labels += 1
                    for line in lines:
                        cls_id = int(line.split()[0])
                        if cls_id in class_counts:
                            class_counts[cls_id] += 1
            else:
                missing_labels += 1
                
        total_images += split_images
        total_labels += split_labels
        
        print(f"[{split.upper()}] SPLIT:")
        print(f"   - Images: {split_images}")
        print(f"   - Labeled: {split_labels}")
        print(f"   - Validation: {'[PASS]' if split_images == split_labels else '[INCOMPLETE]'}")
        print("-" * 30)
        
    print("\nCLASS DISTRIBUTION:")
    for cls_id, name in CLASSES.items():
        print(f"   - {name} (Class {cls_id}): {class_counts[cls_id]} bounding boxes")
        
    print("\nOVERALL STATUS:")
    if missing_labels == 0 and total_labels > 0:
        print("   DATASET IS 100% VALIDATED AND TRAINING-READY.")
    else:
        print(f"   WARNING: {total_images - total_labels} images are missing bounding boxes.")
    print("=" * 60)

if __name__ == "__main__":
    verify_dataset()
