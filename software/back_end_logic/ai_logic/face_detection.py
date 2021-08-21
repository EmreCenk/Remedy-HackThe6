

import cv2
import os
from time import perf_counter

cascade_list = [
    'haarcascade_frontalface_alt.xml',
    'haarcascade_frontalface_alt2.xml',
    # 'haarcascade_frontalface_alt_tree.xml',
    'haarcascade_frontalface_default.xml',
    # 'haarcascade_profileface.xml',
]

def take_picture_with_specific_cascade(person_name,
                                       how_many_pictures,
                                       capturer,
                                       time_limit_seconds = 10,
                                       draw_rect_around_face = True,
                                       cascade_name = "haarcascade_frontalface_alt2.xml",
                                       save_pictures = True,
                                       starting_index_for_picture_labels = 0):

    original_dir = os.getcwd()
    filename = cv2.data.haarcascades + cascade_name
    print(filename)

    face_cascade = cv2.CascadeClassifier(filename)
    i = starting_index_for_picture_labels


    path_to_go = os.path.join(original_dir, rf"software\back_end_logic\ai_logic\images\{person_name}")
    try:
        #try going to it
        os.chdir(path_to_go)
    except:
        try:
            #if it doesn't exist, create it yourself
            os.mkdir(path_to_go)
            os.chdir(path_to_go)

        except:
            #if this doesn't work that means the "images" has not been created yet
            os.mkdir(r"software\back_end_logic\ai_logic\images")
            os.mkdir(path_to_go)
            os.chdir(path_to_go)

    keep_going = True

    starting_time = perf_counter()
    while keep_going and perf_counter() - starting_time < time_limit_seconds:

        # capture the frame
        ret, frame = capturer.read()
        gray_version = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #make it grayscale
        faces = face_cascade.detectMultiScale(gray_version)
        for (x, y, w, h) in faces:
            region_of_interest_gray = gray_version[y:y + h, x:x + w]
            region_of_interest_color = frame[y:y + h, x:x + w]

            if i > how_many_pictures:
                keep_going = False

            if save_pictures:
                cv2.imwrite(f"img{i}.png", gray_version)  # saves the region of interest
                i += 1

            if draw_rect_around_face:
                color = (0, 0, 255)  # NOT RGB. For some reason it's BGR lol
                stroke = 2
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, stroke)  # drawing rectangle around the face

        cv2.imshow("frame", frame)  # "frame" is the window name

        if cv2.waitKey(20) & 0xFF == ord("q"):  # press q to exit
            keep_going = False

    # when loop is broken, release the capture
    os.chdir(original_dir)

    return i

def take_pictures(person_name, how_many_pictures, time_out_seconds = 10, draw_rect_around_recognized = True):


    pic_num_per_cascade = how_many_pictures // len(cascade_list)
    cap = cv2.VideoCapture(0)

    i = 0
    for j in range(len(cascade_list)):
        c = cascade_list[j]
        print("Current Cascade:", c)
        taken_picture_num = take_picture_with_specific_cascade(person_name, pic_num_per_cascade, cap, time_out_seconds, draw_rect_around_recognized, c, True, i)

        pic_num_per_cascade += how_many_pictures - taken_picture_num
        i += 1 + taken_picture_num


    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':

    take_pictures("Cenk", 100, time_out_seconds = 5)
