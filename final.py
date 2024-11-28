import tkinter as tk
from tkinter import messagebox
from time import strftime

import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

import serial
import time
# Sample function for the first code
def send_message_to_parent(student_name, parent_contact):

    print(f"Message sent to {parent_contact}: Your child {student_name} is present.")
def run_first_code():
    attendance = 0
    cred = credentials.Certificate("C:/Users/Rammohan/projects/face_attendance_system/serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://bus-safety-automation-default-rtdb.firebaseio.com/",
        "storageBucket": "bus-safety-automation.appspot.com"
    })

    face_cascade = cv2.CascadeClassifier('face.xml')

    bucket = storage.bucket()

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    background = cv2.imread("C:/Users/Rammohan/projects/face_attendance_system/background.png")

    Path_images = os.listdir("C:/Users/Rammohan/projects/face_attendance_system/images")
    img_mode = []
    for i in Path_images:
        img_mode.append(cv2.imread(os.path.join("C:/Users/Rammohan/projects/face_attendance_system/images", i)))

    file = open('encoder.p', 'rb')
    encodeList_withids = pickle.load(file)
    file.close()
    encodelist, studentids = encodeList_withids

    mode = 0
    counter = 0
    id = -1
    imgstu = []
    count=0
    # print(studentids)
    while True:
        _, img = cap.read()
        imgs = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgs = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        face_cur_frame = face_recognition.face_locations(imgs)  # location of face in imgs
        encode_cur_face = face_recognition.face_encodings(imgs,
                                                          face_cur_frame)  # encoding of face given from face_cue_frame

        background[162:162 + 480, 55:55 + 640] = img
        background[44:44 + 633, 808:808 + 414] = img_mode[mode]
        # cv2.imshow("dispay",img)
        if face_cur_frame:
            for encodeface, faceloc in zip(encode_cur_face, face_cur_frame):
                matches = face_recognition.compare_faces(encodelist, encodeface)
                face_dis = face_recognition.face_distance(encodelist, encodeface)
                # print("matches:",matches)
                # print("face_dis:",face_dis)
                match_index = np.argmin(face_dis)
                # print(match_index)
                if matches[match_index]:

                    id = studentids[match_index]
                    if counter == 0:
                        cvzone.putTextRect(background, "Loading", (275, 400))
                        cv2.imshow("face attendance", background)
                        cv2.waitKey(1)
                        counter = 1
                        mode = 1
            if counter != 0:
                if counter == 1:
                    # data from data base
                    studentinfo = db.reference(f'Students/{id}').get()
                    # print(studentinfo)
                    # data from storage
                    blob = bucket.get_blob(f'C:/Users/Rammohan/projects/face_attendance_system/data/{id}.png')
                    # print(blob)
                    arr = np.frombuffer(blob.download_as_string(), np.uint8)  # converting student id img
                    imgstu = cv2.imdecode(arr, cv2.COLOR_BGRA2RGB)

                    # update attendance
                    datetime_obj = datetime.strptime(studentinfo["last_attendance_time"],
                                                     "%Y-%m-%d %H:%M:%S")
                    secondsElapsed = (datetime.now() - datetime_obj).total_seconds()
                    # print(secondsElapsed)
                    if secondsElapsed > 20:
                        ref = db.reference(f'Students/{id}')

                        ref.child("last_attendance_time").set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        send_message_to_parent(studentinfo["name"], studentinfo["mobile"])
                        print("Attendance updated and message sent.")
                        count = count +1

                    else:
                        mode = 3
                        counter = 0
                        background[44:44 + 633, 808:808 + 414] = img_mode[mode]


                if mode != 3:

                    if 20 < counter < 40:
                        mode = 2
                        background[44:44 + 633, 808:808 + 414] = img_mode[mode]

                    if counter <= 20:
                        cv2.putText(background, str(studentinfo["branch"]), (1006, 550), cv2.FONT_HERSHEY_COMPLEX,
                                    1, (255, 255, 255), 1)
                        cv2.putText(background, str(id), (1006, 493), cv2.FONT_HERSHEY_COMPLEX,
                                    0.5, (255, 255, 255), 1)
                        (w, h), _ = cv2.getTextSize(studentinfo["name"], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                        oset = (414 - w) // 2  # 414 is the total width od the display window
                        cv2.putText(background, str(studentinfo["name"]), (808 + oset, 445), cv2.FONT_HERSHEY_COMPLEX,
                                    1, (0, 0, 0), 1)

                        background[175:175 + 216, 909:909 + 216] = imgstu

                    counter += 1
                    if counter >= 40:


                        counter = 0
                        mode = 0
                        studentinfo = []
                        imgstu = []
                        background[44:44 + 633, 808:808 + 414] = img_mode[mode]
        else:
            mode = 0
            counter = 0

        cv2.imshow("face attendance", background)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    print("count of students in bus",count)
    # Release resources and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()


    print("Running first code...")
    # Example output message (replace with your code’s functionality)
    messagebox.showinfo("Code Execution", "attendance system code executed successfully!")

# Sample function for the second code
def run_second_code():


    # Load the Haar Cascade for palm detection (replace with the correct file path)
    palm_cascade = cv2.CascadeClassifier('hand.xml')  # Ensure 'palm.xml' is available

    # Set up serial communication with Arduino
    arduino = serial.Serial('COM5', 9600)  # Replace 'COM3' with your Arduino's port
    time.sleep(2)  # Allow time for the connection to establish

    # Start the video capture (webcam)
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to grayscale (Haar Cascades work on grayscale images)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect palms in the image using the Haar cascade
        palms = palm_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5, minSize=(70, 70))

        # If palms are detected, send '1' to the Arduino
        if len(palms) > 0:
            print("Palm detected!")
            arduino.write(b'1')  # Send '1' to Arduino to trigger the buzzer
            time.sleep(0.5)  # Short delay to avoid multiple signals in quick succession

        # Draw rectangles around detected palms
        for (x, y, w, h) in palms:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the resulting frame with palm detection
        cv2.imshow("Palm Detection", frame)

        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    arduino.close()

    print("Running second code...")
    # Example output message (replace with your code’s functionality)
    messagebox.showinfo("Code Execution", "hand detection code executed successfully!")

# Set up the main window
root = tk.Tk()
root.title("Code Executor Interface")

# Set window size and center it
window_width = 500
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate x and y coordinates for the window
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

# Set geometry with calculated coordinates
root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
root.configure(bg="#2c3e50")

# Title Label
title_label = tk.Label(root, text="BUS SAFETY AUTOMATION", font=("Helvetica", 18, "bold"), fg="#ecf0f1", bg="#2c3e50")
title_label.pack(pady=20)

# Instruction Label
instruction_label = tk.Label(root, text="Please select a code to execute:", font=("Helvetica", 14), fg="#ecf0f1", bg="#2c3e50")
instruction_label.pack(pady=10)

# Style for buttons
button_style = {
    "font": ("Helvetica", 12, "bold"),
    "bg": "#3498db",
    "fg": "#ecf0f1",
    "activebackground": "#2980b9",
    "activeforeground": "#ecf0f1",
    "relief": tk.RAISED,
    "bd": 4,
    "width": 20,
    "height": 2
}

# Add buttons to run each code
button1 = tk.Button(root, text="Attendance system", command=run_first_code, **button_style)
button1.pack(pady=10)

button2 = tk.Button(root, text="Hand detection", command=run_second_code, **button_style)
button2.pack(pady=10)

# Exit button to close the interface
exit_button = tk.Button(root, text="Exit", command=root.quit, **button_style)
exit_button.pack(pady=20)

# Start the Tkinter main loop
root.mainloop()