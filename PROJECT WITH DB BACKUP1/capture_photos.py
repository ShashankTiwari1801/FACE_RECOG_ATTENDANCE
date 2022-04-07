import cv2
import time
import getpass
import os
import create_folder
import delete_folder
import count_files

def capture_photos(count,camera,ID):
    folder_loc = ID+"/"
    #create_folder.create_folder(folder_loc)
    tot_files = count_files.count_files(folder_loc)
    print(tot_files)
    try:
        cam = cv2.VideoCapture(int(camera))
    except:
        print("CAMERA NOT FOUND")
        return
    for i in range(count):
        return_value, image = cam.read()
        filename = ID + "-" + str(tot_files+i) + ".png";
        cv2.imwrite(os.path.join(folder_loc, filename), image)
        time.sleep(0.1)

    tot_files = count_files.count_files(folder_loc)
    print(tot_files)
    del cam
