import cv2
from time import sleep
import sys
import os
import numpy
import pickle
from time import strftime


print("Done importing")
#cascPath ="../classifiers/haarcascade_frontalface_default.xml"
cascPath="haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
print ("Creating classifier")
webcam_capture = cv2.VideoCapture(0)
print("Created webcam reader")
saved_faces = 0

action = input("Enter the action to perform:")
usrName = ""
if action == "":
    print ("No action set! Use 'save' for saving recognized faces to the file system or 'recognize' to recognized already identified faces.")
    sys.exit(1)

labels = labels = {"name":1}

if action == "recognize" or action == "r":
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer.yml")
    with open("labels.pickle", 'rb') as f:
        old_labels = pickle.load(f)
        # inverting
        labels = {v:k for k,v in old_labels.items()}
else:
    usrName = input("Enter your name:")
    if usrName == "":
        usrName = "unknownFace"
    dirName = "faces/"+usrName
    try:
    # Create target Directory
        os.mkdir(dirName)
    except FileExistsError:
        pass #Already exists

print("Created folder")

def saveFaces (faces,saved_faces):
    for (x,y,w,h) in faces:
                #img_pos_gray = gray[y:y+h,x:x+w]
                saved_faces += 1
                               #square coordinates (ystart, yend + xstart, xend) of face
                img_pos = frame[y:y+h,x:x+w]
                evTime = strftime("%d-%H:%M:%S") #Date too long does not save
                img_item = (dirName + "/" + evTime + "_" + "{0}".format(saved_faces) + ".png")
                cv2.imwrite(img_item, img_pos)
                print("Saved")
                #Save 10 
    return saved_faces

def writeName(name):
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255,255,255)
    stroke = 2
    cv2.putText(frame,name,(x,y), font, 1, color, stroke, cv2.LINE_AA)

print ("Reading webcam")
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

    if action == "save" or action == "s":
        #If a face is found save the face as an img
        if len(faces) > 0:
            print ("Saving faces")
            print(saved_faces)
            if saved_faces < 10:
                saved_faces = saveFaces(faces,saved_faces)
            else:
                break
    elif action == "recognize" or action == "r":
        name = "Unknown Face"
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            gray = gray[y:y+h,x:x+w]
            try:
                id_, conf = recognizer.predict(gray)
            # confidence
                if conf >=45 and conf <= 85: 
                    name = labels[id_]
            except:
                pass
            writeName(name)
        cv2.imshow('Video', frame)

    else:   
        print("Action unknown! Use: 'save' for saving recognized faces to the file system or 'recognize' to recognized already identified faces.")
        break
    
     #Press q to exit programm
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
webcam_capture.release()