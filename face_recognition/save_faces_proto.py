import cv2
from time import sleep
import sys
import os
import numpy

#cascPath ="../classifiers/haarcascade_frontalface_default.xml"
cascPath="haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
webcam_capture = cv2.VideoCapture(0)
saved_faces = 0

recognizer = cv2.face.LBPHFaceRecognizer_create()

usrName = input ("Enter your name:")
dirName = "faces/"+usrName
action = ""
if len(sys.argv) > 1:
    action = sys.argv[1]

#if len(sys.argv) > 1:
#    dirName = "faces/" + sys.argv[1] 
try:
    # Create target Directory
    os.mkdir(dirName)
except FileExistsError:
    pass #Already exists

def saveFaces (faces,saved_faces):
    for (x,y,w,h) in faces:
                #img_pos_gray = gray[y:y+h,x:x+w]
                saved_faces += 1
                               #square coordinates (ystart, yend + xstart, xend) of face
                img_pos = frame[y:y+h,x:x+w]
                img_item = (dirName + "/{0}.png".format(saved_faces))
                cv2.imwrite(img_item, img_pos)
                #Save 10 faces

while True:
    #If no webcam is detected wait for 5 seconds
    if not webcam_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    #Sleep for performance
    sleep(0.1)

    res, frame = webcam_capture.read()
    #Convert image to gray img
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,scaleFactor=1.2,minNeighbors=5,minSize=(30, 30)    )

    if action == "save":
        #If a face is found save the face as an img
        if len(faces) > 0:
            if saved_faces != 10:
                saveFaces(faces,saved_faces)
            else:
                break
    elif action == "recognize":
        for (x,y,w,h) in faces:
            gray = gray[y:y+h,x:x+w]
            id, conf = recognizer.predict(gray)
            # confidence
    else:
        print("Unknown action")
        break
    
     #Press q to exit programm
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
webcam_capture.release()