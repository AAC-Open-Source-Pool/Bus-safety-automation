import cv2
import serial
import time

# Load the Haar Cascade for hand detection (replace with correct file path)
hand_cascade = cv2.CascadeClassifier('hand.xml')  # Ensure 'hand.xml' is available

# Set up serial communication with Arduino
arduino = serial.Serial('COM5', 9600)  # Replace 'COM3' with your Arduino's port
time.sleep(2)  # Allow time for the connection to establish

# Input video file (replace with the correct file path)
  # Provide the path to your video file

# Start the video capture (from video file)
inp="C://Users\Rammohan\projects//face_attendance_system//inpu.mp4"
cap = cv2.VideoCapture(inp)

# Check if video file is opened successfully
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break  # Exit when the video ends

    # Convert the frame to grayscale (Haar Cascades work on grayscale images)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect hands in the image using the Haar cascade
    hands = hand_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(70, 70))

    # If hands are detected, send '1' to the Arduino
    if len(hands) > 0:
        print("Hand detected!")
        arduino.write(b'1')  # Send '1' to Arduino to trigger the buzzer
        time.sleep(0.5)  # Short delay to avoid multiple signals in quick succession
    #for (x, y, w, h) in hands:
    #cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    # Draw rectangles around detected hands


    # Display the resulting frame with hand detection
    cv2.imshow("Hand Detection from Video", frame)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
arduino.close()
