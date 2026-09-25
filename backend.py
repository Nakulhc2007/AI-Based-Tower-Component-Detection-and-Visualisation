from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import cv2
import numpy as np
import base64

app = FastAPI(title="Tower Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load your custom-trained hackathon model locally!
print("Loading local PyTorch model (best.pt)...")
model = YOLO("best.pt")

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    """
    Accepts an image, performs independent image quality filtering (blur, exposure),
    runs the local PyTorch YOLO model, draws bounding boxes, calculates average confidence, 
    and returns a JSON with the image and stats.
    """
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # ==========================================
    # 1. IMAGE QUALITY FILTERING
    # ==========================================
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
    print(f"--> Incoming Image Sharpness Score: {blur_score:.1f}")
    if blur_score < 10:  # Dropped from 800 to 10 (Only blocks extreme blur)
        return JSONResponse(status_code=400, content={
            "error": "Quality Check Failed", 
            "reason": f"Image is extremely blurry (sharpness score: {blur_score:.1f} < 10). Cannot guarantee accurate inference."
        })
    
    avg_brightness = np.mean(gray)
    print(f"--> Incoming Image Brightness Score: {avg_brightness:.1f}")
    if avg_brightness < 10:  # Dropped from 40 to 10 (Only blocks pitch-black)
        return JSONResponse(status_code=400, content={
            "error": "Quality Check Failed", 
            "reason": f"Image is underexposed/too dark (brightness: {avg_brightness:.1f} < 10)."
        })
    if avg_brightness > 245:  # Raised to 245 (Only blocks pure white)
        return JSONResponse(status_code=400, content={
            "error": "Quality Check Failed", 
            "reason": f"Image is overexposed/too bright (brightness: {avg_brightness:.1f} > 245)."
        })

    # ==========================================
    # 2. INFERENCE (LOCAL PYTORCH MODEL)
    # ==========================================
    # We raised confidence to 0.45 and added iou=0.45 to prevent double-labelling!
    results = model.predict(source=img, conf=0.45, iou=0.45)
    
    # Extract predictions
    preds = []
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            # Format names from "monopole_tower" to "Monopole Tower"
            cls_name = model.names[cls_id].replace('_', ' ').title()
            
            # Convert to center x, y, w, h
            w = x2 - x1
            h = y2 - y1
            x = x1 + w / 2
            y = y1 + h / 2
            
            preds.append({
                "class": cls_name,
                "confidence": conf,
                "x": x,
                "y": y,
                "width": w,
                "height": h
            })

    # ==========================================
    # 3. DRAW BOXES & CALCULATE STATS
    # ==========================================
    class_stats = {} 
    
    for p in preds:
        x, y, w, h = int(p['x']), int(p['y']), int(p['width']), int(p['height'])
        cls, conf = p['class'], p['confidence']
        
        if cls not in class_stats:
            class_stats[cls] = {"total_conf": 0.0, "count": 0}
        class_stats[cls]["total_conf"] += conf
        class_stats[cls]["count"] += 1
        
        x1, y1 = int(x - w / 2), int(y - h / 2)
        x2, y2 = int(x + w / 2), int(y + h / 2)
        
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 198, 173), 3)
        label = f"{cls} {conf:.2f}"
        
        (text_w, text_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        
        if y1 < 25:
            text_bg_y1, text_bg_y2, text_y = y1, y1 + text_h + 10, y1 + text_h + 5
        else:
            text_bg_y1, text_bg_y2, text_y = y1 - text_h - 10, y1, y1 - 5
            
        cv2.rectangle(img, (x1, text_bg_y1), (x1 + text_w, text_bg_y2), (255, 198, 173), -1)
        cv2.putText(img, label, (x1, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    # Calculate final average confidence per class
    averages = {}
    for cls, data in class_stats.items():
        averages[cls] = round((data["total_conf"] / data["count"]) * 100, 1)

    # ==========================================
    # 4. RETURN JSON PAYLOAD
    # ==========================================
    _, buffer = cv2.imencode('.jpg', img)
    final_b64 = base64.b64encode(buffer).decode('utf-8')
    
    return JSONResponse(content={
        "image": f"data:image/jpeg;base64,{final_b64}",
        "stats": averages,
        "object_count": len(preds)
    })

@app.get("/")
def health_check():
    return {"status": "Backend is running!"}
