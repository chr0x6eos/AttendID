#!/usr/bin/python3
#Importing all needed libraries / modules
import cv2
import os
import sys
import time
import mysql.connector
from time import sleep
from time import strftime

#Class for database connection and manipulation
class DB_Connection:

    def __init__(self):
        try:
            self.db = mysql.connector.connect(
            host="localhost",
            user="simon",
            passwd="P@ssw0rd$!-278",
            database="Visitors"
            )
            self.mycursor = self.db.cursor()
            debugMsg("Initiated db connection successfully")
        except Exception as x:
            raise Exception('Error occured: {0}'.format(x))

    def insert(self,timeValue,visitorValue=0):
        #Query for creating students
        debugMsg("Trying to insert to db")

        try:            
            sql_query=("INSERT INTO AttendingVisitors (ReadingTime,Visitors) VALUE (%s,%s)") 
            sql_values=(timeValue,visitorValue) #Value needs to be in format time,class,students
            #Executes the query and writes into the database
            self.mycursor.execute(sql_query,sql_values)
            #Commit changes to db
            self.db.commit()

            debugMsg("Successfully inserted")
        except Exception as x:
            raise Exception('Error occured: {0}'.format(x))

def debugMsg(message):
    if debug:
        print(message)

#Path of the identyfier
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

webcam_capture = None
numFaces = [] #Stores the average amount of faces in the array
avgFace = 0 #Average amount of faces

#Evaluation time
evTime = strftime("%Y-%m-%d %H:%M:%S")
#Classes --> will be given from the website later
debug = False

if len(sys.argv) > 1:
    debug = sys.argv[1] != None #Debug is used to print to console

#Creates db obj
db = None
try:
    db = DB_Connection()
except Exception as e:
    print(e)
    if webcam_capture != None:
        webcam_capture.release()
    debugMsg("Error while creating db connection, exiting...")
    sys.exit()

webcam_capture = cv2.VideoCapture(0)
#Webcam capture is in this case the webcam
debugMsg("Starting to read from webcam")

while True:
    #If no webcam is detected wait for 5 seconds
    if not webcam_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass

    #Sleep to manage performance on cpu
    sleep(0.1)
    
    #Read a frame
    res, frame = webcam_capture.read()
    #Convert image to gray img
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    debugMsg("Running face detector")

    #This function returns a list of rectangles, where faces appear
    faces = faceCascade.detectMultiScale(
        gray,
        #Change scale factor if too many invalid detections
        scaleFactor=1.2,
        #3-6 is a good value
        minNeighbors=5,
        #Min size of obj
        minSize=(30, 30)
        #,maxSize=(x,x)
    )

    if debug:
        if len(faces) > 1 or len(faces) == 0: #0 or more then 1 faces found
            print("{0} faces found!".format(len(faces)))
        else: #Only 1 face found
            print("{0} face found!".format(len(faces)))
    numFaces.append(len(faces))

    if len(numFaces) >= 100: #10 s
        #Saving a image for debugging purpose
        debugMsg("Saving last computed img for debugging")
        for (x,y,w,h) in faces: #Drawing rectangle
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        path = "/var/www/html/LAST_READING/reading.png"
        if os.path.exists(path): #If file already exists delete and rewrite
            os.remove(path)
        status = cv2.imwrite(path,frame)
        debugMsg("Saved img with code: {0}".format(status))

        #Calculating average
        debugMsg("Calculating average")
        for x in numFaces:
            avgFace+=x #Adds all the numbers of faces
        avgFace = int(round(avgFace / len(numFaces))) #Average of faces displayed as an int
        debugMsg("Average faces:" + str(avgFace))

        #Save Avg of Faces to Database
        try:
            db.insert(evTime,avgFace)
        except Exception as e:
            print(e)
        #Reset values
        numFaces = []
        avgFace = 0
        faces = None

    #Press q to exit programm
    if cv2.waitKey(1) & 0xFF == ord('q'):
        debugMsg("Force quit initiated")
        break

# When everything is done, release the capture
webcam_capture.release()
debugMsg("Webcam released, completely done now")