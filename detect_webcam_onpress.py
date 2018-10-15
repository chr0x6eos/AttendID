import cv2
import sys

#Path of the identyfier
cascPath ="haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

#webcam capture is in this case the webcam
webcam_capture = cv2.VideoCapture(0)
lastFaces = 0

while True:
    #If no webcam is detected wait for 5 seconds
    if not webcam_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass
    
    #Read a frame
    res, frame = webcam_capture.read()
    #Convert image to gray img
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

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
        if len(faces) > 1 or len(faces)==0:
            print("{0} faces found!".format(len(faces)))
        else:
            print("{0} face found!".format(len(faces)))
        lastFaces = len(faces)
    
    #Press q to exit programm
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
