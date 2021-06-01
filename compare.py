import cv2
import numpy as np
import face_recognition
import os


def compare_and_display(image_received, encode_list, names):


    face_detected = True
    # Resizing the image for processing purposes
    img = image_received
    img_resized = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    img_resized = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
    # detecting all the faces in the image and encoding only the faces
    faces_in_frame = face_recognition.face_locations(img_resized)
    encodes_in_frame = face_recognition.face_encodings(img_resized, faces_in_frame)
    # Comparing the given image with the list of images
    try:
        matches = face_recognition.compare_faces(encode_list, encodes_in_frame[0])
        face_dis = face_recognition.face_distance(encode_list, encodes_in_frame[0])
    except IndexError:
        print("Face not found")
        face_detected = False
        name = 'others'
        cv2.imshow("webcam", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return face_detected, name
    else:
        # Getting the index of the image from the image list which best matches the input image
        match_index = np.argmin(face_dis)
        # placing a rectangular box on the detected face and displaying the name of the individual
        if matches[match_index] and face_dis[match_index] < 0.4:
            name = names[match_index].upper()
            face = face_cascade.detectMultiScale(img, scaleFactor=1.5, minNeighbors=5)
            for x, y, w, h in face:
                img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
                cv2.putText(img, name, (x+6, y+6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        print(name)
        cv2.imshow("webcam", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return face_detected, name




