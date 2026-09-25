"""
Tower Detection — YOLOv8 Training Script

Usage:
    uv run python train.py              # Train from scratch
    uv run python train.py --resume     # Resume interrupted training
    uv run python train.py --predict    # Run prediction on test images
"""

import argparse
from pathlib import Path
from ultralytics import YOLO

DATASET_YAML = Path(r"a:\projects\ksit hackathon\dataset\data.yaml")
PROJECT_DIR = Path(r"a:\projects\ksit hackathon\runs")


def train(resume=False):
    """Train YOLOv8 for tower detection."""
    if resume:
        # Find the latest run and resume
        last_weight = PROJECT_DIR / "detect" / "tower_detector" / "weights" / "last.pt"
        if last_weight.exists():
            model = YOLO(str(last_weight))
            print(f"Resuming from {last_weight}")
        else:
            print("No checkpoint found to resume. Starting fresh.")
            model = YOLO("yolov8n.pt")  # nano model - fastest
    else:
        # Start fresh with pretrained YOLOv8 nano
        model = YOLO("yolov8n.pt")

    # Train
    results = model.train(
        data=str(DATASET_YAML),
        epochs=100,
        imgsz=640,
        batch=16,
        patience=20,          # early stopping after 20 epochs without improvement
        save=True,
        save_period=10,       # save checkpoint every 10 epochs
        project=str(PROJECT_DIR / "detect"),
        name="tower_detector",
        exist_ok=True,
        pretrained=True,
        optimizer="auto",
        lr0=0.01,
        lrf=0.01,
        augment=True,
        hsv_h=0.015,         # hue augmentation
        hsv_s=0.7,           # saturation augmentation
        hsv_v=0.4,           # value/brightness augmentation
        degrees=10.0,        # rotation augmentation
        translate=0.1,
        scale=0.5,
        fliplr=0.5,          # horizontal flip
        flipud=0.0,          # no vertical flip (towers are always upright)
        mosaic=1.0,          # mosaic augmentation
        mixup=0.1,           # mixup augmentation
        device="0" if _has_gpu() else "cpu",
        workers=4,
        verbose=True,
    )

    print("\n✅ Training complete!")
    print(f"   Best weights: {PROJECT_DIR / 'detect' / 'tower_detector' / 'weights' / 'best.pt'}")
    print(f"   Results: {PROJECT_DIR / 'detect' / 'tower_detector'}")

    return results


def validate():
    """Validate the trained model."""
    best_weight = PROJECT_DIR / "detect" / "tower_detector" / "weights" / "best.pt"
    if not best_weight.exists():
        print("No trained model found. Run training first.")
        return

    model = YOLO(str(best_weight))
    metrics = model.val(data=str(DATASET_YAML))
    print(f"\n📊 Validation Results:")
    print(f"   mAP50:    {metrics.box.map50:.4f}")
    print(f"   mAP50-95: {metrics.box.map:.4f}")
    print(f"   Precision: {metrics.box.mp:.4f}")
    print(f"   Recall:    {metrics.box.mr:.4f}")


def predict():
    """Run prediction on test images."""
    best_weight = PROJECT_DIR / "detect" / "tower_detector" / "weights" / "best.pt"
    if not best_weight.exists():
        print("No trained model found. Run training first.")
        return

    model = YOLO(str(best_weight))
    test_dir = Path(r"a:\projects\ksit hackathon\dataset\images\test")

    results = model.predict(
        source=str(test_dir),
        save=True,
        save_txt=True,
        save_conf=True,
        conf=0.25,
        iou=0.45,
        project=str(PROJECT_DIR / "predict"),
        name="tower_predictions",
        exist_ok=True,
    )

    print(f"\n🎯 Predictions saved to: {PROJECT_DIR / 'predict' / 'tower_predictions'}")
    return results


def export_model():
    """Export the trained model to ONNX for deployment."""
    best_weight = PROJECT_DIR / "detect" / "tower_detector" / "weights" / "best.pt"
    if not best_weight.exists():
        print("No trained model found. Run training first.")
        return

    model = YOLO(str(best_weight))
    model.export(format="onnx", imgsz=640, simplify=True)
    print("✅ Model exported to ONNX format")


def _has_gpu():
    """Check if CUDA GPU is available."""
    try:
        import torch
        return torch.cuda.is_available()
    except ImportError:
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tower Detection Training")
    parser.add_argument("--resume", action="store_true", help="Resume training from last checkpoint")
    parser.add_argument("--validate", action="store_true", help="Run validation only")
    parser.add_argument("--predict", action="store_true", help="Run prediction on test images")
    parser.add_argument("--export", action="store_true", help="Export model to ONNX")
    args = parser.parse_args()

    if args.validate:
        validate()
    elif args.predict:
        predict()
    elif args.export:
        export_model()
    else:
        train(resume=args.resume)
