#!/usr/bin/python3
import cv2
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
        except Exception as x:
            print(x)

    def insert(self,timeValue,classValue='4AHITN',studentsValue=0):
        #Query for creating students
        sql_query=("INSERT INTO AttendingStudents (TimeStamp,Class,AttendingStudents) VALUE (%s,%s,%s)") 
        sql_values=(timeValue,classValue,studentsValue) #Value needs to be in format time,class,students

        #Executes the query and writes into the database
        self.mycursor.execute(sql_query,sql_values)
        #Commit changes to db
        self.db.commit()


#Path of the identyfier
cascPath ="haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

#Webcam capture is in this case the webcam
webcam_capture = cv2.VideoCapture(0)
lastFaces = 0

#Function to draw faces on output to show 
def draw(faces, frame):
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

#Stores the average amount of faces in the array
numFaces = []

#Average amount of faces
avgFace = 0

#Max students --> will be given from website later
maxStudents = 16

#Creates db obj
db = None
try:
    db = DB_Connection()
except Exception as e:
    print('Error occured' + e)
    webcam_capture.release()
    sys.exit()

#Evaluation time
evTime = strftime("%Y-%m-%d %H:%M:%S")
#Classes --> will be given from the website later
classValue = '4AHITN'

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
        if len(faces) > 1 or len(faces)==0: #0 or more then 1 faces found
            print("{0} faces found!".format(len(faces)))
        else: #Only 1 face found
            print("{0} face found!".format(len(faces)))
        lastFaces = len(faces) #Set amount of faces to current faces if different
        numFaces.append(len(faces))

    if len(numFaces) >= 50: #5 s
        for x in numFaces:
            avgFace+=x #Adds all the numbers of faces
        avgFace = avgFace / len(numFaces) #Average of faces displayed as an int
        avgFace = int(round(avgFace))
        db.insert(evTime,classValue,avgFace)
        #Done with the script
        break

    #Press q to exit programm
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #for testing show output
    #draw(faces,frame)
    
# When everything is done, release the capture
webcam_capture.release()
#cv2.destroyAllWindows()