# Motion Detection Security System with Flask & OpenCV

## Overview
This project is a **motion detection security system** built using **Flask**, **OpenCV**, and **Winsound** (for sound alerts). The system streams live camera footage, detects motion, and triggers an alarm based on adjustable parameters such as frequency, security status, and sensitivity.

---

## Features
### 1. Live Video Streaming
- Real-time video feed through a web browser using Flask.

### 2. Motion Detection
- Uses OpenCV to detect movement by comparing frame differences.

### 3. Alarm System
- Triggers an audible beep using `winsound` when motion is detected.
- Adjustable **beep frequency** via the web interface.

### 4. Adjustable Parameters
- **Frequency:** Customizable beep sound frequency.
- **Security Status:** Enable or disable motion detection.
- **Sensitivity:** Number of motion frames required to trigger the alarm.

---

## How It Works
- The application captures video frames from the webcam.
- It compares consecutive frames to detect differences.
- If the difference surpasses a threshold and exceeds the set sensitivity, the alarm is triggered.
- The user can configure the detection sensitivity, security status, and alarm sound frequency through the web interface.

---

## Technologies Used
- **Python (Flask)**
- **OpenCV** for video processing
- **Winsound** for audio alerts (Windows only)
- **HTML/CSS** for the web interface

