import os
import pickle
import random
import sys
from time import sleep, strftime
#For image manipulation
import cv2
import numpy
#For training the recognizer
import train_faces

#For only printing text if debug is enabled
def debugMsg(message):
    if debug:
        print(message)

def action_save(faces, saved_faces, recognizer):
    #If a face is found save the face as an img
    if len(faces) > 0:
        debugMsg("Saving faces nr. {0}".format(saved_faces))
        if saved_faces < count: #If images still shall be saved
            return saveFaces(faces,saved_faces), {"name":1}, recognizer
        else:
            debugMsg("Done saving")
            try: #When done saving try to train the recognizer
                recognizer, labels = train(recognizer)
                return -1, labels, recognizer #Returns -1 (done saving), the labels of the faces, the recognizer
            except ValueError: #Raises a value error if no training data is here
                return -1, -1, recognizer #Returns -1 (done saving), -1 (could not create recognizer), the recognizer (empty)
            except Exception as e: #Other error
                print("Error occurred: {0}".format(e))
                return -1, -1, recognizer


def action_recognize(gray, faces, frame, recognizer, labels, trained):
    if not trained: #If not yet trained, try to train
        try:
            recognizer, labels = train(recognizer)
            trained = True
        except ValueError:
            return -1 #-1 means could not train -> save faces first!
        except Exception as e:
            print ("Error occurred: {0}".format(e))
            return -1
      
    debugMsg(labels)
    for (x,y,w,h) in faces:
        name = "Unknown" #Default recognized face name is unknown
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        gray = gray[y:y+h,x:x+w]
        try:
            #Confidence of 0 = 100%
            id_, confidence = recognizer.predict(gray)
            #If the confidence for a certain face is higher than 45 and lower equal 85
            if 45 <= confidence <= 85:
                                        #Confidence shows in percent
                name = labels[id_]
                if debug:
                    name += " {0:.2f}%".format(round(100 - confidence, 2))
        except:
            pass
        writeName(name,x,y)
    cv2.imshow('Video', frame)

def train(recognizer):
    if train_faces.train() == -1: #Train the "AI" with the saved faces -> -1 means no data to train exists
        raise ValueError("No training data!")
    else:
        try: #Training the recognizer
            recognizer.read("trainer.yml")
            with open("labels.pickle", 'rb') as f:
                old_labels = pickle.load(f)
                #inverting
                return recognizer, {v:k for k,v in old_labels.items()} #returns the trained recognizer and the labels
        except Exception as e:
            print("Error: {0}!".format(e))

def setSaveParams():
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
    debugMsg ("Created folder {0}".format(dirName))

    return usrName, count

#Defines if the recognizer is already trained
trained = False

#Debug to print messagges
debug = False

debugMsg("Done importing")
#cascPath ="../classifiers/haarcascade_frontalface_default.xml"
cascPath="haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
debugMsg ("Creating classifier")
webcam_capture = cv2.VideoCapture(0)
debugMsg("Created webcam reader")
saved_faces = 0

#Action values as lists
actionList_recognize = ['r', 'recognize']
actionList_save = ['s', 'save']
actionList_exit = ['exit','e','quit','q']
action_reset = "125884016_reset" #random reset code

#For debugging purpose
if len(sys.argv) > 1:
    debug = sys.argv[1] != None #Debug is used to print to console

action = input("Enter the action to perform: \n Use 'save' for saving recognized faces to the file system or 'recognize' to recognized already identified faces or 'exit' to exit the script. \n")

if action == "":
    print ("No action set! Use 'save' for saving recognized faces to the file system or 'recognize' to recognized already identified faces or 'exit' to exit the script.")
    sys.exit()

labels = {"name":1} #Labels gives the id of the person a name eg: id=1 name="Name"

count = 10 #Default amount of saved faces
usrName = "" #Default usrName

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

def writeName(name,x,y):
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255,255,255)
    stroke = 2
    cv2.putText(frame,name,(x,y), font, 1, color, stroke, cv2.LINE_AA)

debugMsg ("Reading webcam")

#How often webcam could not be read
errorCam = 0

while True:
    #If no webcam is detected wait for 5 seconds
    if not webcam_capture.isOpened():
        errorCam+=1
        print ("Unable to load camera. {0}. try".format(errorCam))
        sleep(5)
        if errorCam < 3:
            continue #Jumps back to beginning of loop
        else:
            print ("Could not access camera. Exiting...")
            sys.exit()

    #Sleep for performance
    sleep(0.1)

    res, frame = webcam_capture.read()
    #Convert image to gray img
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,scaleFactor=1.2,minNeighbors=5,minSize=(30, 30))

    if action in actionList_save:
        if usrName == "":
            usrName, count = setSaveParams()

        if len(faces) != 0:
            try:
                saved_faces, labels, recognizer = action_save(faces,saved_faces,recognizer)
                if saved_faces == -1:
                    saved_faces = 0
                    action = action_reset
                    if labels == -1:
                        labels = {"name":1}
                    else:
                        trained = True
            except Exception as e:
                print("Error occured: {0}".format(e))
                action = action_reset #Reset action
                usrName = "" #Resets user name

    elif action in actionList_recognize:
        if action_recognize(gray,faces,frame,recognizer,labels,trained) == -1: #-1 --> Could not train recognizer -> therefore try other action first
            action = action_reset

    elif action == action_reset:  
        action = input("Enter the action to perform:")
        if action == "":
            print ("No action set! Use 'save' for saving recognized faces to the file system or 'recognize' to recognized already identified faces.")
            break

    elif action in actionList_exit:
        break
    else: 
        print("Action unknown! Use: 'save' for saving recognized faces to the file system or 'recognize' to recognized already identified faces.")
        action = action_reset
    
     #Press q to exit programm
    if cv2.waitKey(1) & 0xFF == ord('q'):
        debugMsg("Force quit initiated")
        break

debugMsg("Releasing webcam")
# When everything is done, release the capture
webcam_capture.release()
cv2.destroyAllWindows()
debugMsg("Completely done")