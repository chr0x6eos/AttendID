#!/usr/bin/python3
import cv2
import os
import sys
import time
import mysql.connector
from time import sleep
from time import strftime

class DB_Connection:

    def __init__(self):
        try:
            self.db = mysql.connector.connect(
            host="localhost",
            user="simon",
            passwd="P@ssw0rd$!-278",
            database="attendID"
            )
            self.mycursor = self.db.cursor()
            debugMsg("Initiated db connection successfully")
        except Exception as x:
            raise Exception('Error occured:' + x)

    def insert(self,timeValue,classValue='4AHITN',studentsValue=0):
        #Query for creating students
        debugMsg("Trying to insert to db")

        try:            
            sql_query=("INSERT INTO AttendingStudents (ReadingTime,Class,AttendingStudents) VALUE (%s,%s,%s)") 
            sql_values=(timeValue,classValue,studentsValue) #Value needs to be in format time,class,students
            #Executes the query and writes into the database
            self.mycursor.execute(sql_query,sql_values)
            #Commit changes to db
            self.db.commit()

            debugMsg("Successfully inserted")
        except Exception as x:
            raise Exception('Error occured:' + x)

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
classValue = "noClass"
maxStudents = 0
debug = False

#Websites tells the script the needed params: classes, maxStudents, (debug)
if len(sys.argv) > 1:
    if sys.argv[1] != "":
        try:
            classValue = sys.argv[1]
        except:
            print("Error reading param: classValue (arg[1])")
            sys.exit()

if len(sys.argv) > 2:
    if sys.argv[2] != "":
        try:
            if int(sys.argv[2]) >= 0:
                maxStudents = int(sys.argv[2])
        except:
            print("Error reading param: maxStudents (arg[2])")
            sys.exit()

if len(sys.argv) > 3:
    debug = sys.argv[3] != None #Debug is used to print to console

if maxStudents == 0 or classValue == "noClass":
    print("Invalid parameters")
    sys.exit()

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

    #Max x stundents in class
    if len(faces) <= maxStudents:
        #Print number of faces
        if debug:
            if len(faces) > 1 or len(faces)==0: #0 or more then 1 faces found
                print("{0} faces found!".format(len(faces)))
            else: #Only 1 face found
                print("{0} face found!".format(len(faces)))
        numFaces.append(len(faces))

    if len(numFaces) >= 50: #5 s
        #Saving a image for debugging purpose
        debugMsg("Saving last computed img for debugging")
        for (x,y,w,h) in faces: #Drawing rectangle
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        path = os.path.abspath("../../pics/reading.png")
        cv2.imwrite(path, frame)

        #Calculating average
        debugMsg("Calculating average")
        for x in numFaces:
            avgFace+=x #Adds all the numbers of faces
        avgFace = int(round(avgFace / len(numFaces))) #Average of faces displayed as an int
        debugMsg("Average faces:" + str(avgFace))
        try:
            db.insert(evTime,classValue,avgFace)
        except Exception as e:
            print(e)
        #Done with the script
        break

    #Press q to exit programm
    if cv2.waitKey(1) & 0xFF == ord('q'):
        debugMsg("Force quit initiated")
        break

# When everything is done, release the capture
webcam_capture.release()
debugMsg("Webcam release, completely done now")