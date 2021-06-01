import os

from compare import *
import cv2

camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

check, frame = camera.read()
recognized_faces = os.listdir(os.getcwd() + '\\images')
images_list = []
names = []
# Retrieving images and their name from the given path
for faces in recognized_faces:
    try:
        cur_image = cv2.imread(os.getcwd() + '\\images\\' + faces + '\\' + os.listdir(os.getcwd() + '\\images\\' + faces)[0])
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
            name = input("New face detected, enter your name: ")
            os.mkdir(os.getcwd() + '\\images\\' + name.upper())
        image_name = name + str(len(os.listdir(os.getcwd() + '\\images\\' + name)) + 1)
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
                break
        else:
            print("adding to others")
            break
# gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# face = face_cascade.detectMultiScale(gray_image, scaleFactor=1.5, minNeighbors=5)
# for x, y, w, h in face:
#     gray_image = cv2.rectangle(gray_image, (x, y), (x+w, y+h), (0, 255, 0), 3)

# cv2.imshow("image", gray_image)
# key = cv2.waitKey(1)
#
# if key == ord('q'):
#     break

camera.release()
