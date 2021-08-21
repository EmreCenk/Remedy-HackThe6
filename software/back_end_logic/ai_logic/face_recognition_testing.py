


import cv2
import pickle
from software.back_end_logic.ai_logic.face_detection import cascade_list

cascade_list.append('haarcascade_profileface.xml')
def start_testing(recognition_threshold = 80):
    """This function opens a testing window where the face recognition ai labels all faces seen from the webcam.
    this function is basically used to test how accurate the ai is."""

    with open("labels.pickle", "rb") as f:
        loaded_labels = pickle.load(f)

    labels = {}
    for name in loaded_labels:
        labels[loaded_labels[name]] = name


    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer.yml") #importing our trained model


    cascades = [cv2.CascadeClassifier(cv2.data.haarcascades + filename) for filename in cascade_list] #cv2.data.haarcascades is the cascade location

    

    cap = cv2.VideoCapture(0)
    i = 0

    keep_going = True
    while keep_going:
        #capture the frame
        ret, frame = cap.read()
        gray_version = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        stop = False
        for face_cascade in cascades:

            faces = face_cascade.detectMultiScale(gray_version)
            for (x, y, w, h) in faces:
                region_of_interest_gray = gray_version[y:y+h, x:x+w]
                region_of_interest_color = frame[y:y+h, x:x+w]

                id, difference = recognizer.predict(region_of_interest_gray) #the lower the difference, the better
                if difference > recognition_threshold:
                    continue

                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id]
                yield name


                color = (255,255,25)
                stroke = 2
                cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)

                color = (0, 0, 255) # NOT RGB. For some reason it's BGR lol
                stroke = 2
                cv2.rectangle(frame, (x,y), (x + w, y + h), color, stroke) # starting end ending coordinates

                stop = True

            if stop:
                break

        #display the frame:
        cv2.imshow("frame", frame) #"frame" is the window name

        if cv2.waitKey(20) & 0xFF == ord("q"): #press q to exit
            keep_going = False


    #when loop is broken, release the capture:
    cap.release()
    cv2.destroyAllWindows()


