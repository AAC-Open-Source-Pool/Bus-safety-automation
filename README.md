# Bus-safety-automation

<h2>Team Details</h2>
<b>Team Number: </b><p>24AACR06</p>
<b>Senior Mentor:</b><p> Abhiram Peddamallu</p>
<b>Junior Mentor:</b><p> Sujay Anishetti</p>
<b>Team Member 1:</b><p> Vivek Malempati</p>
<b>Team Member 2:</b><p> Kongari Vishal</p>
<b>Team Member 3:</b><p> Bingi Hansika</p>

---
## Table of Contents
- [Introduction](#introduction) <br>
- [Requirements](#requirements) <br>
- [How to use](#installation-and-usage) <br>
- [Preview](#previews)
- [Contribution](#contribution)

---

## Introduction
The **Bus Safety Automation Project** integrates computer vision, IoT, and a user-friendly interface to ensure the safety of children traveling by bus. This project includes two core functionalities:

1. **Attendance System**: Utilizes facial recognition for attendance and sends notifications to parents.
2. **Hand Detection System**: Monitors for hands outside the bus window and triggers a buzzer using Arduino.


### Features
#### Attendance System
- Facial recognition for student identification.
- Integration with Firebase for:
  - Storing student data.
  - Tracking attendance.
  - Sending parent notifications.
- Real-time UI updates displaying attendance status.

#### Hand Detection System
- Palm detection using Haar Cascades.
- Arduino integration to trigger a buzzer upon detection.
- Real-time monitoring via a live video feed.

---

## Requirements

<pre>
Package                Version
--------------------- -----------
Python                3.7.x
OpenCV                4.8.0
Face Recognition      1.3.0
Firebase Admin SDK    6.0.1
CVZone                1.5.6
NumPy                 1.24.3
PySerial              3.5
</pre>

<h3>Additional Resources</h3>
<pre>
Resource               Details
--------------------- -----------
Haar Cascade XML       face.xml (for facial detection)
                       hand.xml (for palm detection)

Firebase Configuration:
serviceAccountKey.json Firebase service account configuration file
Database URL           Your Firebase Database URL
Storage Bucket         Your Firebase Storage Bucket

Hardware Requirements:
Arduino                Arduino board (tested with Uno)
Buzzer                 Connected to Arduino for hand detection alerts
</pre>



---

## Installation and usage
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/bus-safety-automation.git
   cd bus-safety-automation
2. Install the required dependencies:
   ```bash
   pip install opencv-python face-recognition firebase-admin cvzone numpy pyserial
3. Configure Firebase:

   - Place `serviceAccountKey.json` in the root directory.
   - Update Firebase Database URL and Storage Bucket in the script.
4. Connect Arduino:

   - Upload the Arduino sketch to the board.
   - Update the COM port in the script to match your Arduino's port.
5. Prepare Haar Cascades:

   - Download `face.xml` and `hand.xml`.
   - Place them in the project directory.
---
## Preview
Screenshots of the project

![WhatsApp Image 2024-11-17 at 15 11 57_556bc8df](https://github.com/user-attachments/assets/d3f8c545-aeeb-40d6-8d6e-08b3e2e25314)
![Screenshot (545)](https://github.com/user-attachments/assets/e529cd69-adf8-4652-8bbe-232d65b274df)

