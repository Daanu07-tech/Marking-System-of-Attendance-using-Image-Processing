import cv2
import os
import numpy as np
from PIL import Image

def assure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def capture_faces(face_id, face_name):
    face_id = int(face_id)  # Ensure face_id is an integer
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    count = 0
    save_path = "dataset/"
    assure_path_exists(save_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image from camera.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            count += 1
            cv2.imwrite(f"{save_path}User.{face_id}.{count}.jpg", gray[y:y + h, x:x + w])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, f"Image {count}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 0, 0), 1)
            cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or count >= 60:
            break

    cap.release()
    cv2.destroyAllWindows()

    # Save face data
    face_data_path = 'face_data.npy'
    if os.path.exists(face_data_path):
        face_data = np.load(face_data_path, allow_pickle=True).tolist()
    else:
        face_data = []

    # Remove duplicate entry for the same ID
    face_data = [entry for entry in face_data if entry['id'] != face_id]
    face_data.append({'id': face_id, 'name': face_name})
    np.save(face_data_path, face_data)

    print(f"Successfully captured {count} images for ID: {face_id}, Name: {face_name}")

def get_images_and_labels(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    face_samples = []
    ids = []
    face_cas = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    for image_path in image_paths:
        img = Image.open(image_path).convert('L')
        img_np = np.array(img, 'uint8')
        id = int(os.path.split(image_path)[-1].split(".")[1])
        faces = face_cas.detectMultiScale(img_np)

        for (x, y, w, h) in faces:
            face_samples.append(img_np[y:y + h, x:x + w])
            ids.append(id)

    return face_samples, ids

def train_recognizer():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, ids = get_images_and_labels('dataset')

    if len(faces) == 0 or len(ids) == 0:
        print("No faces or labels found for training.")
        return

    recognizer.train(faces, np.array(ids))
    assure_path_exists("trainer/")
    recognizer.write('trainer/trainer.yml')
    print("Successfully trained recognizer and saved to 'trainer/trainer.yml'")

if __name__ == "__main__":
    while True:
        try:
            face_id = int(input('Enter your ID (numbers only): '))
            face_name = input('Enter your name: ')
            capture_faces(face_id, face_name)
            train_recognizer()
            more = input("Do you want to add another person? (yes/no): ")
            if more.lower() != 'yes':
                break
        except ValueError:
            print("Invalid input. Please enter a valid numeric ID.")
