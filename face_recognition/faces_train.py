import os

#Adding existing training data to list
base_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(base_dir, "faces")

for root, dirs, files  in os.walk(image_dir):
    for file in files:
       if file.endswith("png") or file.endswith("jpg"):
           path = os.path.join(root, file)
           print(path) 

