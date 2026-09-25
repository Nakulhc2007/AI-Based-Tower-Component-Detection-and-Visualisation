from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import requests
import base64

app = FastAPI(title="Tower Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ROBOFLOW_API_URL = "https://detect.roboflow.com/abhista-ganesh/tower-type-detection-avzfo-3-yolo26s-t1"
ROBOFLOW_API_KEY = "s3MTtPRyVUy8zpa3vJRF"

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    """
    Accepts an image, performs independent image quality filtering (blur, exposure),
    sends it to Roboflow, draws bounding boxes, calculates average confidence, 
    and returns a JSON with the image and stats.
    """
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # ==========================================
    # 1. IMAGE QUALITY FILTERING
    # ==========================================
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Check for Blur (Variance of the Laplacian)
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
    print(f"--> Incoming Image Sharpness Score: {blur_score:.1f}")
    
    # We raised the threshold from 50 to 300 to be much stricter!
    if blur_score < 300:
        return JSONResponse(status_code=400, content={
            "error": "Quality Check Failed", 
            "reason": f"Image is blurry (sharpness score: {blur_score:.1f} < 300). Cannot guarantee accurate inference."
        })
    
    # Check for Exposure (Average Pixel Brightness)
    avg_brightness = np.mean(gray)
    print(f"--> Incoming Image Brightness Score: {avg_brightness:.1f}")
    
    # Raised from 30 to 80 for stricter darkness checks
    if avg_brightness < 80:
        return JSONResponse(status_code=400, content={
            "error": "Quality Check Failed", 
            "reason": f"Image is underexposed/too dark (brightness: {avg_brightness:.1f} < 80)."
        })
    # Lowered from 225 to 200 for stricter brightness checks
    if avg_brightness > 200:
        return JSONResponse(status_code=400, content={
            "error": "Quality Check Failed", 
            "reason": f"Image is overexposed/too bright (brightness: {avg_brightness:.1f} > 200)."
        })

    # ==========================================
    # 2. INFERENCE (ROBOFLOW)
    # ==========================================
    img_base64 = base64.b64encode(contents).decode("utf-8")
    url = f"{ROBOFLOW_API_URL}?api_key={ROBOFLOW_API_KEY}"
    
    try:
        resp = requests.post(url, data=img_base64, headers={"Content-Type": "application/x-www-form-urlencoded"})
        preds = resp.json().get("predictions", [])
    except Exception as e:
        print("Error communicating with Roboflow:", e)
        preds = []

    # ==========================================
    # 3. DRAW BOXES & CALCULATE STATS
    # ==========================================
    class_stats = {} # Stores totals to calculate average later
    
    for p in preds:
        x, y, w, h = int(p['x']), int(p['y']), int(p['width']), int(p['height'])
        cls, conf = p['class'], p['confidence']
        
        # Track stats
        if cls not in class_stats:
            class_stats[cls] = {"total_conf": 0.0, "count": 0}
        class_stats[cls]["total_conf"] += conf
        class_stats[cls]["count"] += 1
        
        # Draw box
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
