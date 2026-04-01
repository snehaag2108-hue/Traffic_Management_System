
from flask import Flask, request, Response, jsonify, send_from_directory
import cv2
import os
import math
import threading
from ultralytics import YOLO

# ================= FLASK CONFIG =================

app = Flask(
    __name__,
    template_folder="../frontend",
    static_folder="../static"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ================= MODEL LOAD =================

model = YOLO("yolov8n.pt")   # Change to best2.pt if needed

# ================= GLOBAL VARIABLES =================

cap = None
uploaded_path = None
detection_running = False
lock = threading.Lock()

avg_speed_global = 0
vehicle_count_global = 0
violation_count_global = 0
car_count_global = 0
bike_count_global = 0
bus_count_global = 0
truck_count_global = 0
bicycle_count_global = 0

prev_pos = {}

speed_limit = 30
meter_per_pixel = 0.05
TARGET_WIDTH = 960

# ================= HOME ROUTE =================

@app.route("/")
def home():
    return send_from_directory("../frontend", "index.html")

# ================= UPLOAD VIDEO =================

@app.route("/upload", methods=["POST"])
def upload():
    global uploaded_path

    file = request.files.get("video")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    uploaded_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(uploaded_path)

    return jsonify({"status": "uploaded"})

# ================= START DETECTION =================

@app.route("/start_detection", methods=["POST"])
def start_detection():
    global cap, detection_running

    if not uploaded_path:
        return jsonify({"error": "Upload video first"}), 400

    if cap:
        cap.release()

    cap = cv2.VideoCapture(uploaded_path)
    detection_running = True

    return jsonify({"status": "started"})

# ================= VIDEO STREAM =================

def generate_frames():
    global avg_speed_global
    global vehicle_count_global
    global violation_count_global
    global car_count_global
    global bike_count_global
    global bus_count_global
    global truck_count_global
    global bicycle_count_global
    global detection_running

    while True:

        if not detection_running or cap is None:
            continue

        ret, frame = cap.read()
        if not ret:
            detection_running = False
            break

        # Resize for performance
        height, width = frame.shape[:2]
        scale = TARGET_WIDTH / width
        frame = cv2.resize(frame, (TARGET_WIDTH, int(height * scale)))

        results = model.track(frame, persist=True, conf=0.4)

        vehicle_count = 0
        violation_count = 0
        total_speed = 0

        car = bike = bus = truck = bicycle = 0

        if results and results[0].boxes.id is not None:

            boxes = results[0].boxes.xyxy.cpu().numpy()
            ids = results[0].boxes.id.cpu().numpy()
            classes = results[0].boxes.cls.cpu().numpy()

            for box, track_id, cls_id in zip(boxes, ids, classes):

                class_name = model.names[int(cls_id)]

                if class_name not in ["car", "motorcycle", "bus", "truck", "bicycle"]:
                    continue

                x1, y1, x2, y2 = map(int, box)
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                speed = 0

                if track_id in prev_pos:
                    px, py = prev_pos[track_id]
                    pixel_dist = math.sqrt((cx - px)**2 + (cy - py)**2)
                    meters = pixel_dist * meter_per_pixel
                    speed = meters * 25 * 3.6

                prev_pos[track_id] = (cx, cy)

                vehicle_count += 1
                total_speed += speed

                if speed > speed_limit:
                    violation_count += 1

                if class_name == "car": car += 1
                elif class_name == "motorcycle": bike += 1
                elif class_name == "bus": bus += 1
                elif class_name == "truck": truck += 1
                elif class_name == "bicycle": bicycle += 1

                color = (0, 0, 255) if speed > speed_limit else (0, 255, 0)

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame,
                            f"{class_name} {int(speed)} km/h",
                            (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, color, 2)

        avg_speed = total_speed / vehicle_count if vehicle_count > 0 else 0

        # Thread-safe update
        with lock:
            avg_speed_global = int(avg_speed)
            vehicle_count_global = vehicle_count
            violation_count_global = violation_count
            car_count_global = car
            bike_count_global = bike
            bus_count_global = bus
            truck_count_global = truck
            bicycle_count_global = bicycle

        _, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# ================= STREAM ROUTE =================

@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# ================= LIVE STATS =================

@app.route("/stats")
def stats():
    with lock:
        return jsonify({
            "avgSpeed": avg_speed_global,
            "totalVehicles": vehicle_count_global,
            "violations": violation_count_global,
            "cars": car_count_global,
            "bikes": bike_count_global,
            "buses": bus_count_global,
            "trucks": truck_count_global,
            "bicycles": bicycle_count_global
        })

# ================= RUN SERVER =================

if __name__ == "__main__":
    app.run(debug=False, threaded=True)