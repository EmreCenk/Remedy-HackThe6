


import numpy as np
import os
from PIL import Image
import cv2
import pickle
from software.back_end_logic.ai_logic.face_detection import cascade_list

IMAGE_FOLDER_LOCATION = "images"
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #gets current location
IMAGE_DIR = os.path.join(BASE_DIR, IMAGE_FOLDER_LOCATION)

CASCADE_LOCATION = r"cascades/data/"
cascades = [cv2.CascadeClassifier(cv2.data.haarcascades + filename) for filename in cascade_list] #cv2.data.haarcascades is the cascade location

def train_model(save_name = "trainer"):
    current_id = 0
    label_ids = {}
    training_list = [] #every image in the training list with index i has the profile_label_1 label_list[i]
    label_list = []
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    for root, dirs, files in os.walk(IMAGE_DIR):
        for file in files:
            if file.endswith(".png") or file.endswith(".jpg"):
                path = os.path.join(root, file)
                parent_folder = os.path.basename(root) #parent folder is the profile_label_1
                #.replace(" ", "-").lower()

                print(parent_folder, file)
                if parent_folder not in label_ids:
                    label_ids[parent_folder] = current_id
                    current_id += 1

                id = label_ids[parent_folder]


                image_object = Image.open(path).convert("L") #.convert("L") converts to grayscale
                image_array = np.array(image_object, "uint8") #converting image to numpy array

                for face_cascade in cascades:
                    faces = face_cascade.detectMultiScale(image_array)


                    for (x, y, w, h) in faces:
                        region_of_interest = image_array[y:y+h, x:x+w]
                        training_list.append(region_of_interest)
                        label_list.append(id)


    with open("labels.pickle", "wb") as f:
        pickle.dump(label_ids, f)

    # print(training_list)
    # print(label_list)
    recognizer.train(training_list, np.array(label_list))
    recognizer.save(f"{save_name}.yml")