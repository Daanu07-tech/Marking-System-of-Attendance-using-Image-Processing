import cv2
import numpy as np
import os
from datetime import datetime
import pyttsx3
import xlwt
from xlrd import open_workbook
from xlutils.copy import copy

# Ensure directory exists
def assure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Get name by ID from .npy
def get_name_from_id(id):
    if not os.path.exists('face_data.npy'):
        return None
    face_data = np.load('face_data.npy', allow_pickle=True)
    for data in face_data:
        if str(data['id']) == str(id):
            return data['name']
    return None

# Save attendance only for valid name
def output(filename, sheet, name, present):
    if name is None or name == "Unknown":
        return None  # Don't write to sheet if name is invalid

    directory = 'firebase/attendance_files/'
    assure_path_exists(directory)
    file_path = os.path.join(directory, f"{filename}{datetime.now().date()}.xls")

    if os.path.isfile(file_path):
        rb = open_workbook(file_path, formatting_info=True)
        book = copy(rb)
        sh = book.get_sheet(0)
        existing_rows = rb.sheet_by_index(0).nrows
    else:
        book = xlwt.Workbook()
        sh = book.add_sheet(sheet)
        sh.write(0, 0, 'Date')
        sh.write(0, 1, str(datetime.now().date()))
        sh.write(1, 0, 'Name')
        sh.write(1, 1, 'Present')
        sh.write(1, 2, 'Time')
        existing_rows = 2  # Header takes up first two rows

    current_time = datetime.now().strftime("%H:%M:%S")
    sh.write(existing_rows, 0, name)
    sh.write(existing_rows, 1, present)
    sh.write(existing_rows, 2, current_time)
    book.save(file_path)
    return file_path

# Initialize voice
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Main recognition loop
def recognize_and_write():
    cap = cv2.VideoCapture(0)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    attendance_dict = {}
    font = cv2.FONT_HERSHEY_SIMPLEX

    while True:
        ret, img = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            id, conf = recognizer.predict(roi_gray)

            if conf < 50:
                name = get_name_from_id(id)
                if name and id not in attendance_dict:
                    output('attendance', 'class1', name, 'yes')
                    attendance_dict[id] = name
                    speak(f"Welcome to class, {name}")
                label = name
                color = (0, 255, 0)
            else:
                label = "Unknown"
                color = (0, 0, 255)

            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y - 10), font, 0.7, color, 2)

        cv2.imshow('Recognition', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize_and_write()
