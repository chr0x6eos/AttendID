'''
Code from:
https://github.com/codingforentrepreneurs/Guides/blob/master/LICENSE
The MIT License (MIT)

Copyright (c) 2014 CodingForEntrepreneurs.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import cv2
import os
import numpy as np
from PIL import Image #Python image library
import pickle

#The dir the script is saved in
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#The dir the faces are saved in
image_dir = os.path.join(BASE_DIR, "faces")

cascPath="haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath) 
#uncomment if incompatibile
#faceRecognizer = cv2.face.createLBPHFaceRecognizer()
#comment if incompatibile
faceRecognizer = cv2.face.LBPHFaceRecognizer_create()

current_id = 0
label_ids = {}
y_labels = []
x_train = []

for root, dirs, files in os.walk(image_dir):
	for file in files: #Go through all files and find pictures
		if file.endswith("png") or file.endswith("jpg"):
			path = os.path.join(root, file)
			#The folder name is the label of the pictures
			label = os.path.basename(root).replace(" ", "-").lower()

			if not label in label_ids:
				label_ids[label] = current_id
				current_id += 1
			id_ = label_ids[label]
			
			pil_image = Image.open(path).convert("L")#convert to grayscale img
			image_array = np.array(pil_image,"uint8")  #Turns image into number array
			faces = faceCascade.detectMultiScale(image_array)

			#Find faces
			for (x,y,w,h) in faces:
				face = image_array[y:y+h,x:x+w]
				#training data
				x_train.append(face)
				y_labels.append(id_)

with open("labels.pickle", 'wb') as f:
	pickle.dump(label_ids, f)

#Training
faceRecognizer.train(x_train,np.array(y_labels))
faceRecognizer.save("trainer.yml")
print("Training done")