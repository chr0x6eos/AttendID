import cv2
from time import sleep
import sys
import os
import numpy
import pickle
from time import strftime
import random
import train_faces

def action_save(faces,saved_faces):
    #If a face is found save the face as an img
    if len(faces) > 0:
        print ("Saving faces")
        print(saved_faces)
        if saved_faces < count:
            return saveFaces(faces,saved_faces)
        else:
            print("Done saving")
            train_faces.train() #Train the "AI" with the saved faces
            try:
                recognizer.read("trainer.yml")
                with open("labels.pickle", 'rb') as f:
                    old_labels = pickle.load(f)
                    #inverting
                    labels = {v:k for k,v in old_labels.items()}
            except Exception as e:
                print("Error: {0}!".format(e))
                sys.exit()
            return -1

def action_recognize():
    res, frame = webcam_capture.read()
    name = "Unknown Face"
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        gray = gray[y:y+h,x:x+w]
        try:
            id_, confidence = recognizer.predict(gray)
            print(confidence)
            #If the confidence for a certain face is higher than 45 and lower equal 100
            if confidence >= 50 and confidence <= 75: 
                                        #Confidence shows in percent
                name = labels[id_] + "{0:.2f}%".format(round(100 - confidence, 2))
        except:
            pass
        writeName(name)
    cv2.imshow('Video', frame)

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

count = 10

if action != "r" and action != "recognize":
    usrName = input("Enter your name:")
    count = input("How often to save:")
    if count != "":
        try: #How often to save -> if input invalid use default (10)
            if int(count) > 0:
                count = int(count)
        except:
            pass

    if usrName == "":
        usrName = "unknownFace"
    dirName = "faces/"+usrName

    try:
    #Create target Directory
        os.mkdir("faces")
    except FileExistsError:
        pass #Already exists
    try:
        os.mkdir(dirName)
    except FileExistsError:
        pass
    print("Created folder")

recognizer = cv2.face.LBPHFaceRecognizer_create()

def saveFaces (faces,saved_faces):
    for (x,y,w,h) in faces:
                #img_pos_gray = gray[y:y+h,x:x+w]
                saved_faces += 1
                               #square coordinates (ystart, yend + xstart, xend) of face
                img_pos = frame[y:y+h,x:x+w]
                img_item = (dirName + "/" + str(random.randint(1000,99999)) + "_" + "{0}".format(saved_faces) + ".png")
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
    faces = faceCascade.detectMultiScale(gray,scaleFactor=1.2,minNeighbors=5,minSize=(30, 30))

    if action == "save" or action == "s":
        saved_faces = action_save(faces,saved_faces)
        if saved_faces == -1:
            saved_faces = 0
            action = "125884016_reset"

    elif action == "recognize" or action == "r":
        action_recognize()

    elif action == "125884016_reset":  
        action = input("Enter the action to perform:")
        if action == "":
            print ("No action set! Use 'save' for saving recognized faces to the file system or 'recognize' to recognized already identified faces.")
            sys.exit(1)
    else: 
        print("Action unknown! Use: 'save' for saving recognized faces to the file system or 'recognize' to recognized already identified faces.")
        break
    
     #Press q to exit programm
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("Completely done")
# When everything is done, release the capture
webcam_capture.release()
cv2.destroyAllWindows()