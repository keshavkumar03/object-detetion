from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
from ultralytics import YOLO
import numpy as np
import io
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def app_desp():
    return("this is a 0bject detetion app where we can input images and videos")

@app.get("/")
async def root():
    return({'message':app_desp()})
# Load YOLO model
model = YOLO("yolo/yolov8n.pt")  # Adjust the path as needed

def detect_objects_in_image(image: np.ndarray):
    results = model(image)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cv2.rectangle(image, (x1, y1), (x2, y2), (250, 100, 250), 3)
    return image

def generate_frames(video_path: str):
    logging.info(f"Opening video file: {video_path}")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        logging.error("Error opening video stream")
        raise RuntimeError("Error opening video stream")

    while True:
        ret, frame = cap.read()
        if not ret:
            logging.info("No more frames to read or error reading frame")
            break

        results = model(frame, stream=True)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (250, 100, 250), 3)

        ret, buffer = cv2.imencode('.jpg', frame)
        cv2.imshow('Video Stream', frame)

        if not ret:
            logging.error("Error encoding frame to JPEG")
            break

        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    logging.info("Released video capture")

@app.post("/detect/image")
async def detect_image(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    detected_image = detect_objects_in_image(image)
    
    _, img_encoded = cv2.imencode('.jpg', detected_image)
    return StreamingResponse(io.BytesIO(img_encoded.tobytes()), media_type="image/jpeg")

@app.post("/detect/video")
async def detect_video(file: UploadFile = File(...)):
    contents = await file.read()
    video_path = 'temp_video.mp4'
    logging.info(f"Saving uploaded video to {video_path}")
    with open(video_path, 'wb') as f:
        f.write(contents)
    
    if not os.path.exists(video_path):
        logging.error("Error saving video")
        raise RuntimeError("Error saving video")

    return StreamingResponse(generate_frames(video_path), media_type='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
