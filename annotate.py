"""
Browser-based bounding box annotation tool for YOLO format.
Supports 2 classes: Supporting Tower (0) and Monopole Tower (1).

Usage:
    uv run python annotate.py [--split train]
"""

import argparse
import json
import http.server
import socketserver
import webbrowser
import urllib.parse
from pathlib import Path

DATASET_DIR = Path(__file__).resolve().parent / "dataset"
PORT = 8787


def get_images_and_labels(split):
    img_dir = DATASET_DIR / "images" / split
    label_dir = DATASET_DIR / "labels" / split

    items = []
    for img_path in sorted(img_dir.glob("*.jpg")):
        label_path = label_dir / f"{img_path.stem}.txt"
        labels = []
        if label_path.exists():
            content = label_path.read_text().strip()
            if content:
                for line in content.split("\n"):
                    parts = line.strip().split()
                    if len(parts) == 5:
                        labels.append({
                            "cls": int(parts[0]),
                            "x": float(parts[1]),
                            "y": float(parts[2]),
                            "w": float(parts[3]),
                            "h": float(parts[4]),
                        })
        items.append({
            "filename": img_path.name,
            "stem": img_path.stem,
            "labels": labels,
        })
    return items


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tower Annotator</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: #0f0f13;
    color: #e0e0e0;
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .toolbar {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 16px;
    background: #1a1a24;
    border-bottom: 1px solid #2a2a3a;
    flex-shrink: 0;
    flex-wrap: wrap;
  }
  .toolbar h1 {
    font-size: 16px;
    font-weight: 600;
    color: #7c6ff7;
    margin-right: 8px;
  }
  .toolbar button {
    padding: 6px 14px;
    background: #2a2a3a;
    color: #ccc;
    border: 1px solid #3a3a4a;
    border-radius: 6px;
    cursor: pointer;
    font-size: 13px;
    transition: all 0.2s;
  }
  .toolbar button:hover { background: #3a3a4a; color: #fff; }
  .toolbar button.primary {
    background: #5b4fd4;
    color: #fff;
    border-color: #7c6ff7;
  }
  .toolbar button.primary:hover { background: #6b5fe4; }
  .toolbar button.danger {
    background: #5a2020;
    border-color: #8a3030;
  }
  .toolbar button.danger:hover { background: #7a3030; }
  .toolbar .spacer { flex: 1; }
  .toolbar .info {
    font-size: 13px;
    color: #888;
  }
  .toolbar .counter {
    font-size: 13px;
    color: #7c6ff7;
    font-weight: 600;
  }

  /* Class selector */
  .class-selector {
    display: flex;
    gap: 4px;
    background: #151520;
    border-radius: 8px;
    padding: 3px;
    border: 1px solid #2a2a3a;
  }
  .class-btn {
    padding: 6px 14px !important;
    border-radius: 6px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
    border: 2px solid transparent !important;
  }
  .class-btn.cls-0 {
    background: #1a2a1a !important;
    color: #6adf6a !important;
    border-color: #2a4a2a !important;
  }
  .class-btn.cls-0.active {
    background: #2a5a2a !important;
    color: #8fff8f !important;
    border-color: #4caf50 !important;
    box-shadow: 0 0 10px rgba(76, 175, 80, 0.3);
  }
  .class-btn.cls-1 {
    background: #2a1a1a !important;
    color: #df9a6a !important;
    border-color: #4a2a1a !important;
  }
  .class-btn.cls-1.active {
    background: #5a3a1a !important;
    color: #ffbb77 !important;
    border-color: #ff9800 !important;
    box-shadow: 0 0 10px rgba(255, 152, 0, 0.3);
  }
  .class-label {
    font-size: 11px;
    color: #888;
    margin-right: 4px;
  }

  .main {
    display: flex;
    flex: 1;
    overflow: hidden;
  }

  .sidebar {
    width: 220px;
    background: #151520;
    border-right: 1px solid #2a2a3a;
    overflow-y: auto;
    flex-shrink: 0;
  }
  .sidebar .img-item {
    padding: 8px 12px;
    cursor: pointer;
    font-size: 12px;
    border-bottom: 1px solid #1a1a28;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: background 0.15s;
  }
  .sidebar .img-item:hover { background: #1e1e30; }
  .sidebar .img-item.active { background: #252540; border-left: 3px solid #7c6ff7; }
  .sidebar .img-item .dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
  }
  .sidebar .img-item .dot.labeled { background: #4caf50; }
  .sidebar .img-item .dot.unlabeled { background: #666; }
  .sidebar .img-item .name {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    flex: 1;
  }
  .sidebar .img-item .count {
    color: #888;
    font-size: 11px;
  }

  .canvas-container {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
    background: #0a0a0f;
  }
  .canvas-wrapper {
    position: relative;
    display: inline-block;
  }
  #canvas {
    display: block;
    cursor: crosshair;
  }

  .help-bar {
    padding: 8px 16px;
    background: #1a1a24;
    border-top: 1px solid #2a2a3a;
    font-size: 12px;
    color: #666;
    display: flex;
    gap: 16px;
    flex-shrink: 0;
    flex-wrap: wrap;
  }
  .help-bar kbd {
    background: #2a2a3a;
    padding: 1px 5px;
    border-radius: 3px;
    font-size: 11px;
    color: #aaa;
  }
</style>
</head>
<body>

<div class="toolbar">
  <h1>Tower Annotator</h1>
  <span class="class-label">Class:</span>
  <div class="class-selector">
    <button class="class-btn cls-0 active" onclick="setClass(0)" id="btn-cls-0">
      [1] Supporting Tower
    </button>
    <button class="class-btn cls-1" onclick="setClass(1)" id="btn-cls-1">
      [2] Monopole Tower
    </button>
  </div>
  <span class="counter" id="progress">0 / 0</span>
  <div class="spacer"></div>
  <button onclick="prevImage()">Prev</button>
  <button onclick="nextImage()">Next</button>
  <button class="danger" onclick="clearBoxes()">Clear</button>
  <button onclick="undoBox()">Undo</button>
  <button class="primary" onclick="saveLabels()">Save</button>
  <span class="info" id="status"></span>
</div>

<div class="main">
  <div class="sidebar" id="sidebar"></div>
  <div class="canvas-container">
    <div class="canvas-wrapper">
      <canvas id="canvas"></canvas>
    </div>
  </div>
</div>

<div class="help-bar">
  <span><kbd>Click+Drag</kbd> Draw box</span>
  <span><kbd>1</kbd> Supporting Tower</span>
  <span><kbd>2</kbd> Monopole Tower</span>
  <span><kbd>A</kbd>/<kbd>D</kbd> Prev/Next</span>
  <span><kbd>S</kbd> Save</span>
  <span><kbd>Z</kbd> Undo</span>
  <span><kbd>C</kbd> Clear</span>
  <span><kbd>Right-click</kbd> Delete box</span>
</div>

<script>
const SPLIT = "__SPLIT__";
const CLASS_NAMES = ["Supporting Tower", "Monopole Tower"];
const CLASS_COLORS = ["#4caf50", "#ff9800"];
const CLASS_BG = ["rgba(76,175,80,0.7)", "rgba(255,152,0,0.7)"];
let images = __IMAGES_JSON__;
let currentIdx = 0;
let boxes = []; // [{cls, x, y, w, h}]
let currentClass = 0;
let drawing = false;
let startX, startY;
let img = new Image();
let canvas, ctx;
let scale = 1;
let dirty = false;

function init() {
  canvas = document.getElementById("canvas");
  ctx = canvas.getContext("2d");

  canvas.addEventListener("mousedown", onMouseDown);
  canvas.addEventListener("mousemove", onMouseMove);
  canvas.addEventListener("mouseup", onMouseUp);
  canvas.addEventListener("contextmenu", onRightClick);
  document.addEventListener("keydown", onKeyDown);

  buildSidebar();
  loadImage(0);
}

function setClass(cls) {
  currentClass = cls;
  document.getElementById("btn-cls-0").classList.toggle("active", cls === 0);
  document.getElementById("btn-cls-1").classList.toggle("active", cls === 1);
}

function buildSidebar() {
  const sb = document.getElementById("sidebar");
  sb.innerHTML = "";
  images.forEach((item, idx) => {
    const div = document.createElement("div");
    div.className = "img-item" + (idx === currentIdx ? " active" : "");
    div.innerHTML =
      '<span class="dot ' + (item.labels.length > 0 ? "labeled" : "unlabeled") + '"></span>' +
      '<span class="name" title="' + item.filename + '">' + item.filename.substring(4, 16) + '...</span>' +
      '<span class="count">' + item.labels.length + '</span>';
    div.onclick = function() { loadImage(idx); };
    sb.appendChild(div);
  });
}

function loadImage(idx) {
  if (dirty) saveLabels();
  currentIdx = idx;
  img.onload = function() {
    var container = canvas.parentElement.parentElement;
    var maxW = container.clientWidth - 40;
    var maxH = container.clientHeight - 40;
    scale = Math.min(maxW / img.width, maxH / img.height, 1);
    canvas.width = img.width * scale;
    canvas.height = img.height * scale;
    boxes = images[idx].labels.map(function(l) {
      return { cls: l.cls, x: l.x, y: l.y, w: l.w, h: l.h };
    });
    dirty = false;
    draw();
    updateUI();
  };
  img.src = "/image/" + SPLIT + "/" + images[idx].filename;
}

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

  boxes.forEach(function(box, i) {
    var x = (box.x - box.w / 2) * canvas.width;
    var y = (box.y - box.h / 2) * canvas.height;
    var w = box.w * canvas.width;
    var h = box.h * canvas.height;
    var cls = box.cls || 0;

    ctx.strokeStyle = CLASS_COLORS[cls];
    ctx.lineWidth = 2;
    ctx.strokeRect(x, y, w, h);

    // Label background
    var label = CLASS_NAMES[cls] + " #" + (i + 1);
    ctx.font = "12px sans-serif";
    var tw = ctx.measureText(label).width + 8;
    ctx.fillStyle = CLASS_BG[cls];
    ctx.fillRect(x, y - 20, tw, 20);
    ctx.fillStyle = "#fff";
    ctx.fillText(label, x + 4, y - 6);
  });
}

function onMouseDown(e) {
  if (e.button !== 0) return;
  drawing = true;
  var rect = canvas.getBoundingClientRect();
  startX = e.clientX - rect.left;
  startY = e.clientY - rect.top;
}

function onMouseMove(e) {
  if (!drawing) return;
  var rect = canvas.getBoundingClientRect();
  var curX = e.clientX - rect.left;
  var curY = e.clientY - rect.top;
  draw();
  ctx.strokeStyle = CLASS_COLORS[currentClass];
  ctx.lineWidth = 2;
  ctx.setLineDash([5, 3]);
  ctx.strokeRect(startX, startY, curX - startX, curY - startY);
  ctx.setLineDash([]);
}

function onMouseUp(e) {
  if (!drawing) return;
  drawing = false;
  var rect = canvas.getBoundingClientRect();
  var endX = e.clientX - rect.left;
  var endY = e.clientY - rect.top;

  if (Math.abs(endX - startX) < 5 || Math.abs(endY - startY) < 5) {
    draw();
    return;
  }

  var x1 = Math.min(startX, endX) / canvas.width;
  var y1 = Math.min(startY, endY) / canvas.height;
  var x2 = Math.max(startX, endX) / canvas.width;
  var y2 = Math.max(startY, endY) / canvas.height;

  boxes.push({
    cls: currentClass,
    x: (x1 + x2) / 2,
    y: (y1 + y2) / 2,
    w: x2 - x1,
    h: y2 - y1
  });
  dirty = true;
  draw();
  updateUI();
}

function onRightClick(e) {
  e.preventDefault();
  var rect = canvas.getBoundingClientRect();
  var mx = (e.clientX - rect.left) / canvas.width;
  var my = (e.clientY - rect.top) / canvas.height;

  for (var i = boxes.length - 1; i >= 0; i--) {
    var b = boxes[i];
    if (mx >= b.x - b.w/2 && mx <= b.x + b.w/2 &&
        my >= b.y - b.h/2 && my <= b.y + b.h/2) {
      boxes.splice(i, 1);
      dirty = true;
      draw();
      updateUI();
      return;
    }
  }
}

function onKeyDown(e) {
  if (e.key === "d" || e.key === "ArrowRight") nextImage();
  else if (e.key === "a" || e.key === "ArrowLeft") prevImage();
  else if (e.key === "s") saveLabels();
  else if (e.key === "z") undoBox();
  else if (e.key === "c") clearBoxes();
  else if (e.key === "1") setClass(0);
  else if (e.key === "2") setClass(1);
}

function nextImage() {
  if (currentIdx < images.length - 1) loadImage(currentIdx + 1);
}
function prevImage() {
  if (currentIdx > 0) loadImage(currentIdx - 1);
}
function undoBox() {
  if (boxes.length > 0) {
    boxes.pop();
    dirty = true;
    draw();
    updateUI();
  }
}
function clearBoxes() {
  boxes = [];
  dirty = true;
  draw();
  updateUI();
}

function saveLabels() {
  var item = images[currentIdx];
  var labelLines = boxes.map(function(b) {
    return b.cls + " " + b.x.toFixed(6) + " " + b.y.toFixed(6) + " " + b.w.toFixed(6) + " " + b.h.toFixed(6);
  });

  fetch("/save/" + SPLIT + "/" + item.stem, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ labels: labelLines.join("\\n") }),
  }).then(function(r) { return r.json(); }).then(function(data) {
    if (data.ok) {
      item.labels = boxes.map(function(b) { return {cls: b.cls, x: b.x, y: b.y, w: b.w, h: b.h}; });
      dirty = false;
      document.getElementById("status").textContent = "Saved!";
      setTimeout(function() { document.getElementById("status").textContent = ""; }, 1500);
      buildSidebar();
    }
  });
}

function updateUI() {
  var labeled = images.filter(function(i) { return i.labels.length > 0; }).length;
  document.getElementById("progress").textContent =
    labeled + " / " + images.length + " labeled | Boxes: " + boxes.length;
  buildSidebar();
}

window.onload = init;
window.onresize = function() { if (img.complete) loadImage(currentIdx); };
</script>
</body>
</html>
"""


class AnnotationHandler(http.server.BaseHTTPRequestHandler):
    split = "train"

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/":
            items = get_images_and_labels(self.split)
            html = HTML_TEMPLATE.replace("__SPLIT__", self.split)
            html = html.replace("__IMAGES_JSON__", json.dumps(items))
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        elif parsed.path.startswith("/image/"):
            parts = parsed.path.split("/")
            split = parts[2]
            filename = "/".join(parts[3:])
            img_path = DATASET_DIR / "images" / split / filename
            if img_path.exists():
                self.send_response(200)
                ext = img_path.suffix.lower()
                ct = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}.get(ext, "image/jpeg")
                self.send_header("Content-Type", ct)
                self.end_headers()
                self.wfile.write(img_path.read_bytes())
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path.startswith("/save/"):
            parts = parsed.path.split("/")
            split = parts[2]
            stem = parts[3]
            content_len = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(content_len))
            label_path = DATASET_DIR / "labels" / split / f"{stem}.txt"
            label_path.write_text(body["labels"])
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass


def main():
    parser = argparse.ArgumentParser(description="Tower Annotation Tool")
    parser.add_argument("--split", default="train", choices=["train", "val", "test"])
    parser.add_argument("--port", type=int, default=PORT)
    args = parser.parse_args()
    AnnotationHandler.split = args.split

    items = get_images_and_labels(args.split)
    labeled = sum(1 for i in items if i["labels"])

    print(f"Tower Annotator (2 classes: Supporting Tower, Monopole Tower)")
    print(f"  Split: {args.split}")
    print(f"  Images: {len(items)} ({labeled} already labeled)")
    print(f"  URL: http://localhost:{args.port}")
    print(f"  Press Ctrl+C to stop\n")

    webbrowser.open(f"http://localhost:{args.port}")

    with socketserver.TCPServer(("", args.port), AnnotationHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()
