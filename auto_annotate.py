"""
Auto-annotate tower images using YOLO-World (zero-shot object detection).
Uses text prompts to detect towers without manual labeling.

This generates YOLO-format label files for all images in the dataset.
You should manually review and correct the annotations afterward.
"""

import os
from pathlib import Path
from ultralytics import YOLO

DATASET_DIR = Path(r"a:\projects\ksit hackathon\dataset")
CLASSES = ["tower", "transmission tower", "cell tower", "electric tower", "radio tower", "pylon"]
TARGET_CLASS = "tower"  # All detected objects map to class 0 (tower)
CONFIDENCE_THRESHOLD = 0.15  # Lower threshold to catch more towers (review later)


def auto_annotate():
    """Use YOLO-World for zero-shot tower detection and generate labels."""
    print("Loading YOLO-World model...")
    model = YOLO("yolov8x-worldv2.pt")  # Large model for best zero-shot accuracy

    # Set custom classes for zero-shot detection
    model.set_classes(CLASSES)

    total_annotations = 0
    total_images = 0

    for split in ['train', 'val', 'test']:
        img_dir = DATASET_DIR / 'images' / split
        label_dir = DATASET_DIR / 'labels' / split
        images = sorted(img_dir.glob('*.jpg'))

        print(f"\nAnnotating {split} ({len(images)} images)...")

        for img_path in images:
            total_images += 1
            results = model.predict(
                source=str(img_path),
                conf=CONFIDENCE_THRESHOLD,
                iou=0.45,
                verbose=False,
            )

            # Write YOLO-format labels
            label_path = label_dir / f"{img_path.stem}.txt"
            annotations = []

            for result in results:
                boxes = result.boxes
                if boxes is not None and len(boxes) > 0:
                    for box in boxes:
                        # Get normalized xywh (YOLO format)
                        xywhn = box.xywhn[0].tolist()
                        conf = float(box.conf[0])
                        # All tower-related classes map to class 0
                        annotations.append(f"0 {xywhn[0]:.6f} {xywhn[1]:.6f} {xywhn[2]:.6f} {xywhn[3]:.6f}")

            label_path.write_text('\n'.join(annotations))

            status = f"  {img_path.name}: {len(annotations)} tower(s) detected"
            if annotations:
                total_annotations += len(annotations)
            else:
                status += " [NO DETECTION]"
            print(status)

    print(f"\n{'='*60}")
    print(f"Auto-annotation complete!")
    print(f"  Total images processed: {total_images}")
    print(f"  Total tower annotations: {total_annotations}")
    print(f"  Images with no detections: {total_images - sum(1 for split in ['train', 'val', 'test'] for f in (DATASET_DIR / 'labels' / split).glob('*.txt') if f.read_text().strip())}")
    print(f"\nIMPORTANT: Review annotations manually for accuracy!")
    print(f"  You can use LabelImg to visualize and correct:")
    print(f"    pip install labelImg")
    print(f"    labelImg {DATASET_DIR / 'images' / 'train'} {DATASET_DIR / 'labels' / 'train'}")


if __name__ == "__main__":
    auto_annotate()
