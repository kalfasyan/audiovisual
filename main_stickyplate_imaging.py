import pandas as pd
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import os

locations = ["herent", "leuven", "heverlee"]
dates = ["1429_011219", "0529_131219", "0615_131219"]
a_or_b = ['a','b']

def choose(a):
    for i,ch in enumerate(a):
        print("{} : {}".format(i,ch))
    choice = input("Your choice: \n")
    assert int(choice) in range(len(a)), "Choice out of range!"
    return choice

def take_pic(loc,date,idx,ab):
    camera = PiCamera()
    rawCapture = PiRGBArray(camera)

    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    camera.close()

    cv2.imwrite("{}_{}_{}{}.jpg".format(loc,date,idx,ab), image)
    print("Image saved.")

while True:
    print("\n### NEW STICKY PLATE CHOICES ###:\n")
    loc = locations[int(choose(locations))]
    print("Chosen location: {}\n".format(loc))
    date = dates[int(choose(dates))]
    print("Chosen date: {}\n".format(date))

    idx = int(input("Chosen index:"))
    print("\n")

    ab = a_or_b[int(choose(a_or_b))]
    print("\nChosen side: {}\n".format(ab))

    if ab == 'b':
        path = "{}_{}_{}{}.jpg".format(loc,date,idx,'a')
#        fnames = os.listdir('.')
#        print(fnames)
#        print("check:", path in fnames)
        check_path = os.path.isfile(path)
        print("Checking path", path)
        if not check_path: 
            print("############################################################")
            print("[WARN] There is no \'A\' image file for this selection! Restarting..")
            print("############################################################")
            continue
    take_pic(loc,date,idx,ab)
    print("\nFILENAME: {}_{}_{}{}".format(loc,date,idx,ab))
