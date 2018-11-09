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

    def insert(self,value):
        #Query for creating students
        sql_query=("INSERT INTO AttendingStudents (TimeStamp,Class,AttendingStudents) VALUE (%s,%s,%s)")
        sql_values=value #Value needs to be in format x,y,z

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

    #If a new amount of faces detected
    if len(faces) != lastFaces:
        #Print number of faces
        if len(faces) > 1 or len(faces)==0: #0 or more then 1 faces found
            print("{0} faces found!".format(len(faces)))
        else: #Only 1 face found
            print("{0} face found!".format(len(faces)))
        lastFaces = len(faces) #Set amount of faces to current faces if different
    
    #Press q to exit programm
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #for testing show output
    draw(faces,frame)
    
# When everything is done, release the capture
webcam_capture.release()
cv2.destroyAllWindows()