import face_recognition
import cv2
import numpy as np
import serial
from serial import Serial

ser = serial.Serial('/dev/ttyACM0')
video_capture = cv2.VideoCapture(0)

# print(cv2.getBuildInformation())

dani0 = face_recognition.load_image_file("dani0.jpg")
dani0_face_encoding = face_recognition.face_encodings(dani0)[0]

dani1 = face_recognition.load_image_file("dani1.jpg")
dani1_face_encoding = face_recognition.face_encodings(dani1)[0]

dani2 = face_recognition.load_image_file("dani2.jpg")
dani2_face_encoding = face_recognition.face_encodings(dani2)[0]

known_face_encodings = [
    dani0_face_encoding,
    dani1_face_encoding,
    dani2_face_encoding
]
known_face_names = [
    "dani0",
    "dani1",
    "dani2"
]

def serWrite():
    ser.write(b'1')
    print('yee')

def imgUn():
    imgUnlocked = cv2.imread('/home/pi/Desktop/frLock/locked.png')
    imgUnlockedResized = cv2.resize(imgUnlocked, (700,400))
    cv2.imshow('img', imgUnlockedResized)

def imgLoc():
    imgLocked = cv2.imread('/home/pi/Desktop/frLock/rllyLocked.png')
    imgLockedResized = cv2.resize(imgLocked, (700,400))
    cv2.imshow('img', imgLockedResized)

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []

        imgLoc()

        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                serWrite()
                imgUn()
            else:
                imgLoc()

            face_names.append(name)


    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    # cv2.imshow('video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
