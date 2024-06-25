Object Detection System using Deep Learning
Implemented an object detection system using YOLO V8 and deployed it as a React web application using FAST api. The system allows users to upload images and receive real-time Images with bounding boxes around detected objects.

Technologies Used
Backend: FastAPI (Python)
Frontend: React (JavaScript, HTML, CSS)
Deep Learning Framework: YOLO V8
Languages: Python, JavaScript
Features
Real-time object detection in videos using YOLO V8.
FastAPI backend for processing video uploads and streaming.
React frontend with an intuitive user interface for uploading videos and viewing processed outputs.
Responsive design for seamless user experience across devices.
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/object-detection.git
cd object-detection
Setup Backend (FastAPI):

bash
Copy code
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
Setup Frontend (React):

bash
Copy code
cd frontend
npm install
npm start
Open in Browser:
Open http://localhost:3000 to view the app in your browser.

Usage
Upload a Image file using the provided interface.
The backend will process the video using YOLO V8 and return a stream with bounding boxes around detected objects.
View the processed video with real-time object detection.
Contributing
Contributions are welcome! Please fork the repository and create a pull request with your improvements.
