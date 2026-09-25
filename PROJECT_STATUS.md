# Tower Detection — Hackathon Project Status
## Last Updated: 2026-09-25 11:25 IST

---

## PROJECT OVERVIEW

We are building a **tower detection system** using **YOLOv8** (object detection).
Given an image, the model should draw **bounding boxes** around any towers it finds.

**Tech stack:**
- Python 3.14
- uv (package manager — like pip but faster)
- Ultralytics YOLOv8 (object detection framework)
- OpenCV + Pillow (image processing)
- PyTorch (deep learning backend, installed automatically with ultralytics)

---

## WHAT HAS BEEN COMPLETED

### 1. Dataset Collection — DONE
- 124 raw tower images collected in `sample/` directory
- Mix of high-res (5472x3648, ~10MB) and web-scraped low-res images
- Formats: .JPG, .jpg, .jpeg, .png

### 2. Dataset Inspection — DONE
- Script: `inspect_dataset.py`
- Run with: `uv run python inspect_dataset.py`
- Found: 0 corrupt files, 4 duplicate pairs, 2 very dark images, 4 very bright, 1 blurry

### 3. Duplicate Removal — DONE
- Script: `cleanup_dataset.py`
- Removed 4 exact duplicate pairs (8 images → 4 removed)
- 120 unique images remain in `sample/`

### 4. Dataset Preparation (YOLO format) — DONE
- Script: `prepare_dataset.py`
- All images resized to 640x640 (letterboxed with gray padding)
- Split into train/val/test (70/20/10):
  - train: 84 images
  - val:   24 images
  - test:  12 images
- Directory structure created at `dataset/`:
  ```
  dataset/
    images/
      train/   (84 .jpg files, 640x640)
      val/     (24 .jpg files, 640x640)
      test/    (12 .jpg files, 640x640)
    labels/
      train/   (84 .txt files — CURRENTLY EMPTY)
      val/     (24 .txt files — CURRENTLY EMPTY)
      test/    (12 .txt files — CURRENTLY EMPTY)
    data.yaml  (YOLO dataset config)
  ```

### 5. Training Script — DONE (ready to use after annotation)
- Script: `train.py`
- Uses YOLOv8 nano (yolov8n.pt) — pretrained on COCO, fine-tuned on our data
- Auto-detects GPU vs CPU
- Commands:
  ```
  uv run python train.py              # Train from scratch
  uv run python train.py --resume     # Resume interrupted training
  uv run python train.py --validate   # Run validation metrics
  uv run python train.py --predict    # Run predictions on test set
  uv run python train.py --export     # Export to ONNX for deployment
  ```

### 6. Annotation Tool — DONE
- Script: `annotate.py`
- Browser-based tool at http://localhost:8787
- Run with: `uv run python annotate.py --split train`
- Dark-themed UI with keyboard shortcuts
- Saves labels in YOLO format automatically

---

## WHAT STILL NEEDS TO BE DONE

### STEP 1: ANNOTATE THE IMAGES (this is the critical blocker)
The label .txt files are currently EMPTY. You must draw bounding boxes around towers.

**How to annotate:**
1. Run: `uv run python annotate.py --split train`
2. Browser opens at http://localhost:8787
3. For each image:
   - Click and drag to draw a box around each tower
   - Press S to save
   - Press D to go to next image
4. Repeat for val: `uv run python annotate.py --split val`
5. Repeat for test: `uv run python annotate.py --split test`

**Keyboard shortcuts:**
- A / Left Arrow = previous image
- D / Right Arrow = next image
- S = save annotations
- Z = undo last box
- C = clear all boxes
- Right-click on a box = delete it

**YOLO label format** (each line in .txt file):
```
<class_id> <x_center> <y_center> <width> <height>
```
All values normalized 0-1. Class 0 = tower.

**Alternative annotation tools** (if you prefer):
- LabelImg: `pip install labelImg` then `labelImg dataset/images/train dataset/labels/train`
- Roboflow (web): https://roboflow.com (upload images, annotate, export YOLO format)
- CVAT (web): https://cvat.ai

### STEP 2: TRAIN THE MODEL
Once annotation is complete:
```
uv run python train.py
```
- Takes ~30-60 min on GPU, longer on CPU
- Results saved to `runs/detect/tower_detector/`
- Best weights: `runs/detect/tower_detector/weights/best.pt`

### STEP 3: EVALUATE & PREDICT
```
uv run python train.py --validate    # Check mAP, precision, recall
uv run python train.py --predict     # Run on test images, saves annotated results
```

### STEP 4: EXPORT FOR DEPLOYMENT (optional)
```
uv run python train.py --export      # Export to ONNX
```

---

## FILE LISTING

```
ksit hackathon/
├── sample/                    # Raw images (120 after dedup)
├── dataset/                   # YOLO-format dataset
│   ├── images/
│   │   ├── train/ (84)
│   │   ├── val/ (24)
│   │   └── test/ (12)
│   ├── labels/
│   │   ├── train/ (84 — NEED ANNOTATION)
│   │   ├── val/ (24 — NEED ANNOTATION)
│   │   └── test/ (12 — NEED ANNOTATION)
│   └── data.yaml
├── inspect_dataset.py         # Dataset quality analysis
├── cleanup_dataset.py         # Removes duplicate images
├── prepare_dataset.py         # Resizes, splits, creates YOLO structure
├── auto_annotate.py           # Auto-annotation (BROKEN — DLL policy block)
├── annotate.py                # Browser-based annotation tool (WORKING)
├── train.py                   # YOLOv8 training/validation/prediction
├── pyproject.toml             # Project config (managed by uv)
└── .venv/                     # Python virtual environment
```

---

## HOW TO RESUME ON ANOTHER LAPTOP

1. Clone the repo:
   ```
   git clone <your-repo-url>
   cd ksit-hackathon
   ```

2. Install uv (if not installed):
   ```
   pip install uv
   ```
   Or: https://docs.astral.sh/uv/getting-started/installation/

3. Install dependencies:
   ```
   uv sync
   ```

4. Continue with annotation:
   ```
   uv run python annotate.py --split train
   ```

5. Then train:
   ```
   uv run python train.py
   ```

---

## KNOWN ISSUES

1. **auto_annotate.py is broken** — Windows Application Control policy blocks the
   `regex` DLL needed by CLIP/YOLO-World. The manual annotation tool (annotate.py)
   works fine as a workaround.

2. **No GPU on this machine** — Training will run on CPU (slower). If your other
   laptop has a GPU with CUDA, training will be much faster.

3. **Large files** — The `sample/` directory has ~750MB of images. The `dataset/`
   directory has ~30MB (resized). Consider adding `sample/` to .gitignore if
   your repo has size limits.

---

## QUICK REFERENCE COMMANDS

```bash
# Inspect dataset quality
uv run python inspect_dataset.py

# Annotate images (opens browser)
uv run python annotate.py --split train
uv run python annotate.py --split val
uv run python annotate.py --split test

# Train model
uv run python train.py

# Check results
uv run python train.py --validate
uv run python train.py --predict
```
