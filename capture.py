import os

from compare import *
import cv2

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


def save_in_others(img):
    if 'OTHERS' not in os.listdir(os.getcwd()):
        os.mkdir(os.getcwd() + '\\' + 'OTHERS')
        path = os.getcwd() + '\\' + 'OTHERS'
        cv2.imwrite(path + '\\OTHERS1.jpg', img)
    else:
        cv2.imwrite(os.getcwd() + '\\OTHERS\\OTHERS' + str(len(os.listdir(os.getcwd() + '\\OTHERS')) + 1) + '.jpg', img)


camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

check, frame = camera.read()
recognized_faces = os.listdir(os.getcwd() + '\\images')
images_list = []
names = []
if len(recognized_faces) == 0:
    cv2.imshow('img', frame)
    cv2.waitKey(0)
    face = face_cascade.detectMultiScale(frame, scaleFactor=1.5, minNeighbors=5)
    print(face)
    if len(face) == 0:
        save_in_others(frame)
    else:
        name = input("New face detected, enter name: ").upper()
        os.mkdir(os.getcwd() + '\\images\\' + name.upper())
        path = os.getcwd() + '\\images\\' + name + '\\' + name + '1'
        cv2.imwrite(path + '.jpg', frame)
# Retrieving images and their name from the given path
else:
    for faces in recognized_faces:
        try:
            cur_image = cv2.imread(os.getcwd() + '\\images\\' + faces + '\\' +
                                   os.listdir(os.getcwd() + '\\images\\' + faces)[0])
        except IndexError:
            pass
        else:
            if cur_image is not None:
                images_list.append(cur_image)
                names.append(faces)
    print(names)
    # Encoding the images
    print('encoding...')
    encode_list = []
    for image in images_list:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(image)[0]
        encode_list.append(encode)
    print('encoding complete')
    counter = 0
    while True:
        state, name = compare_and_display(frame, encode_list, names)

        if state:
            if name not in names:
                os.mkdir(os.getcwd() + '\\images\\' + name.upper())
            image_name = name.upper() + str(len(os.listdir(os.getcwd() + '\\images\\' + name)) + 1)
            path_recognized = (os.getcwd() + '\\images\\' + name + '\\' + image_name)
            # if not os.path.exists(path_recognized):
            #     os.mkdir(path_recognized)
            cv2.imwrite(path_recognized + '.jpg', frame)
            break

        else:
            counter += 1
            if counter <= 3:
                a = input("Does this image really contain a face[Y/N]: ")
                if a.upper() == 'Y':
                    pass
                else:
                    print("adding to others")
                    save_in_others(frame)
                    break
            else:
                print('adding in others')
                save_in_others(frame)
                break

camera.release()

