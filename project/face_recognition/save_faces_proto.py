import os
import pickle
import random
import sys
from time import sleep
#For image manipulation
import cv2
#For training the recognizer
import train_faces

#For only printing text if debug is enabled
def debugMsg(message):
    if debug:
        print(message)

def train(recognizer):
    if train_faces.train() == -1: #Train the "AI" with the saved faces -> -1 means no data to train exists
        raise ValueError("No training data!")
    else:
        try: #Training the recognizer
            debugMsg("Training recognizer")
            recognizer.read("trainer.yml")
            with open("labels.pickle", 'rb') as f:
                old_labels = pickle.load(f)
                #inverting
                debugMsg("Done training")
                return recognizer, {v:k for k,v in old_labels.items()} #returns the trained recognizer and the labels
        except Exception as e:
            debugMsg("Error: {0}!".format(e))

def setSaveParams():
    usrName = input("Enter your name:")
    count = input("How often to save:")
    if count != "":
        try: #How often to save -> if input invalid use default (10)
            if int(count) > 0:
                count = int(count)
        except:
            count = 10

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

    return usrName, dirName, count

#Defines if the recognizer is already trained
trained = False

#Debug to print messages
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
actionList_recognize = ['recognize','r']
actionList_save = ['save', 's']
actionList_exit = ['exit','e', 'quit','q']
actionList_debug = ['debug', 'd']
actionList_NoDebug = ['no debug', 'nodebug', 'noDebug', 'nd', 'nD']
action_reset = "125884016_reset" #random reset code

#For debugging purpose
if len(sys.argv) > 1:
    debug = sys.argv[1] is not None  #Debug is used to print to console

action = input("Enter the action to perform: \n Use 'save' for saving recognized faces to the file system or 'recognize' to recognized already identified faces or 'exit' to exit the script. \n")

if action == "":
    print ("No action set! Use 'save' for saving recognized faces to the file system or 'recognize' to recognized already identified faces or 'exit' to exit the script.")
    sys.exit()

labels = {"name":1} #Labels gives the id of the person a name eg: id=1 name="Name"

count = 10 #Default amount of saved faces
usrName = "" #Default usrName

#recognizer = cv2.face.EigenFaceRecognizer_create()
#recognizer = cv2.face.FisherFaceRecognizer_create()
recognizer = cv2.face.LBPHFaceRecognizer_create()


def saveFaces (faces,saved_faces,dirName):
    for (x,y,w,h) in faces:
                #img_pos_gray = gray[y:y+h,x:x+w]
                saved_faces += 1
                               #square coordinates (ystart, yend + xstart, xend) of face
                img_pos = frame[y:y+h,x:x+w]
                img_item = (dirName + "/" + str(random.randint(1000,99999)) + "_" + "{0}".format(saved_faces) + ".png")
                cv2.imwrite(img_item, img_pos)
                debugMsg("Saved {0}".format(saved_faces))
    return saved_faces

def writeName(name,x,y):
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255,255,255)
    stroke = 2
    cv2.putText(frame,name,(x,y), font, 1, color, stroke, cv2.LINE_AA)

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
    #sleep(0.1)

    res, frame = webcam_capture.read()
    #Convert image to gray img
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,scaleFactor=1.2,minNeighbors=5,minSize=(30, 30))

    if action in actionList_recognize:
        if not trained:
            try:
                recognizer, labels = train(recognizer)
                debugMsg(labels)
                trained = True
            except Exception as e:
                debugMsg("Error occurred: {0}".format(e))
                trained = False
        #Only if trained try to recognize
        if trained:
            if len(faces) > 0:
                for (x, y, w, h) in faces:
                    name = "Unknown"  # Default recognized face name is unknown
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    gray = gray[y:y + h, x:x + w]
                    try:
                        # Confidence of 0 = 100%
                        id_, confidence = recognizer.predict(gray)
                        # If the confidence for a certain face is higher than 45 and lower equal 85
                        debugMsg(labels[id_] + " {0:.2f}".format(round(100 - confidence, 2)))
                        if  confidence <= 50:
                            name = labels[id_]
                            if debug:  # Confidence shown in percent
                                name = labels[id_] + " {0:.2f}%".format(round(100 - confidence, 2))
                    except Exception as e:
                        debugMsg("Error: {0}".format(e))
                    writeName(name, x, y)
            cv2.imshow('Recognizing faces...', frame)
        else:
            print("Could not create recognizer! Please check if there is data to train on")
            action = action_reset

    elif action == action_reset:
        action = input("Enter the action to perform:")
        if action == "":
            print ("No action set! Use 'save' for saving recognized faces to the file system or 'recognize' to recognized already identified faces.")
            action = action_reset

    elif action in actionList_save:
        if usrName == "":
            usrName, dirName, count = setSaveParams()

        #Only 1 face detected -> save
        if len(faces) == 1:
            try:
                # If a face is found save the face as an img
                if len(faces) > 0:
                    debugMsg("Saving faces nr. {0}".format(saved_faces))
                    if saved_faces < count:  # If images still shall be saved
                        saved_faces = saveFaces(faces, saved_faces, dirName)
                    else:
                        debugMsg("Done saving")
                        recognizer, labels = train(recognizer)
                        debugMsg(labels)
                        trained = True
                        saved_faces = 0
                        action = action_reset
                        usrName = ""
            except Exception as e:
                debugMsg("Error occurred: {0}".format(e))
                print("Error occurred while saving")
                usrName = ""  # Resets user name
                action = action_reset

    elif action in actionList_exit:
        break
    elif action in actionList_debug:
        debug = True
        action = action_reset
    elif action in actionList_NoDebug:
        debug = False
        action = action_reset
    else: 
        print("Action unknown! Use: 'save' for saving recognized faces to the file system or 'recognize' to recognized already identified faces.")
        action = action_reset

    # Press q to exit program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        debugMsg("Force quit initiated")
        action = action_reset

debugMsg("Releasing webcam")
# When everything is done, release the capture
webcam_capture.release()
cv2.destroyAllWindows()
debugMsg("Completely done")