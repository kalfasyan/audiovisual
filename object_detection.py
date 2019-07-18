# Import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import mahotas
import datetime
import time
import os
import imutils
import numpy as np
import glob
import argparse

def plot_cv2(img):
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


import RPi.GPIO as GPIO
import time

pin = 17
var = 0
GPIO.setmode(GPIO.BCM)

GPIO.setup(pin, GPIO.OUT)

GPIO.output(pin, GPIO.HIGH)

time.sleep(.5)


camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

camera.capture(rawCapture, format="bgr")
image = rawCapture.array
#image = cv2.imread(args["image"])
#image = cv2.resize(image, (350,350))
image = image[100:430, 150:500]

(H, W) = image.shape[:2]
print(H,W)
# Save the original image files in a separate subfolder
imageName = 'Original_' + str(time.strftime("%d_%m_%Y_%H_%M_%S")) + '.jpg'
path = '/home/pi/Desktop/' 
#cv2.imwrite(os.path.join(path , imageName), image) 

# Process the original image
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(image, (7, 7), 0)
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 3)#11, 3)
filtered = cv2.medianBlur(thresh,9) # 13
edged = cv2.Canny(filtered, 30, 150)

cv2.imshow("Input", image)
cv2.imshow("Canny", edged)
cv2.waitKey(0)

(_,cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

print("I count {} insects in this image".format(len(cnts)))

# Let's highlight the insects in the original image by drawing a
# green contour around them
edged_image = image.copy()
cv2.drawContours(edged_image, cnts, -1, (0, 255, 0), 1);

ResultName = 'Result_' + str(time.strftime("%d_%m_%Y_%H_%M_%S")) + '.jpg'
cv2.imwrite(ResultName,edged_image)

camera.close()
GPIO.output(pin, GPIO.LOW)
time.sleep(1)

GPIO.cleanup()
