🚦 Automated Traffic Management and Control System using Raspberry Pi

📌 Overview

Traffic congestion is a critical issue in urban cities, where conventional traffic lights operate on fixed timers and fail to adapt dynamically to real-time road conditions. This project presents an automated traffic control system using Raspberry Pi, socket programming, and YOLOv5 (ONNX) for vehicle detection.

We implemented a client-server model with three Raspberry Pis:

- 1 Server Raspberry Pi – Processes images, detects vehicles, and decides traffic priority.

- 2 Client Raspberry Pis – Capture traffic images, send them to the server, and control LEDs (red/green) to simulate traffic lights.

The system dynamically decides signal priority based on the number of vehicles detected in each client’s image, thereby mimicking an intelligent adaptive traffic control system.

🛠️ Tech Stack

- Hardware: Raspberry Pi 3B, LEDs, GPIO circuits

- Programming Language: Python

- Libraries:

- OpenCV (Image Processing)

- ONNX Runtime (Model Inference)

- NumPy (Array Manipulation)

- Socket Programming (Client-Server Communication)

- RPi.GPIO (LED Control)

- Model: YOLOv5s (converted to ONNX for lightweight inference on Raspberry Pi)

🔌 Circuit Setup

- Green LED: GPIO 17 (Pin 11)

- Red LED: GPIO 27 (Pin 13)

- GND: Pin 6

- Logic:

- 1 → Green ON, Red OFF

- 0 → Red ON, Green OFF

👨‍💻 Authors

Developed as a major project using Raspberry Pi for smart traffic management.

⚡ This project demonstrates how low-cost hardware + AI can drive smart city solutions for real-world problems.
