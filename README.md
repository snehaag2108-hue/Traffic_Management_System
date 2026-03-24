## 🚦 Traffic Management System using YOLOv8

An AI-powered Traffic Management System that uses YOLOv8 (You Only Look Once) for real-time vehicle detection, traffic density analysis, and smart traffic control.

This project leverages computer vision to improve traffic efficiency, reduce congestion, and support smart city infrastructure.

## 📌 Project Description

The Traffic Management System is designed to monitor live traffic using video feeds or recorded footage. It uses the YOLOv8 object detection model to identify vehicles such as cars, buses, trucks, and bikes.

Based on the detected traffic density, the system can:

Analyze congestion levels
Provide intelligent traffic signal control (simulation)
Generate real-time insights

---

## 🎯 What It Does

Detects vehicles in real-time using YOLOv8
Counts number of vehicles in each lane
Classifies vehicle types
Estimates traffic density
Simulates smart traffic signal timing

---

## ⚙️ Features
🚗 Real-time vehicle detection
🧠 AI-based traffic density analysis
📊 Vehicle counting & classification
🎥 Works on video streams / CCTV footage
🚦 Smart traffic signal simulation
📈 Data visualization (optional integration)

---

## 🧠 Model Used
YOLOv8 (Ultralytics)
Fast and accurate object detection
Pre-trained on COCO dataset
Detects multiple vehicle classes

---

## 🧩 Tech Stack

Machine Learning:

Python
YOLOv8 (Ultralytics)
OpenCV

Libraries:

NumPy
Pandas (optional)
Matplotlib (for visualization)

---

## ⚙️ Setup Instructions

1️⃣ Clone the Repository

git clone https://github.com/your-username/traffic-management-system.git
cd traffic-management-system

2️⃣ Create Virtual Environment

python -m venv venv

3️⃣ Activate Virtual Environment

▶ Windows:

venv\Scripts\activate
▶ Mac/Linux:

source venv/bin/activate

4️⃣ Install Dependencies

pip install flask ultralytics opencv-python numpy

5️⃣ Project Structure

Traffic-Management-system/
│
├── backend/
│   ├── app.py
│   └── uploads/
│       └── yolov8n.pt
│
├── frontend/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js

▶️ Running the Application

* ✅ Method 1: Direct Python Execution
cd backend

python app.py

* ✅ Method 2: Using Flask Command

▶ Windows (CMD):

cd backend
set FLASK_APP=app.py
flask run
▶ Windows (PowerShell):

cd backend
$env:FLASK_APP="app.py"
flask run
▶ Mac/Linux:

cd backend
export FLASK_APP=app.py
flask run

🌐 Open in Browser

http://127.0.0.1:5000/
