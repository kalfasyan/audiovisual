# Import the necessary packages
#from picamera.array import PiRGBArray
#from picamera import PiCamera
import cv2
import mahotas
import datetime
import time
import os
import imutils
import numpy as np
import glob
import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str, required=True,
	help="path to input image")
args = vars(ap.parse_args())

def plot_cv2(img):
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#camera = PiCamera()
#camera.resolution = (640, 480)
#camera.framerate = 32
#rawCapture = PiRGBArray(camera, size=(640, 480))

#camera.capture(rawCapture, format="bgr")
image = cv2.imread(args["image"])
image = cv2.resize(image, (1350,1350))
crop = 350
image = image[crop:-crop, crop:-crop]
img_og = image.copy()

(H, W) = image.shape[:2]

# Save the original image files in a separate subfolder
og_imageName = 'Original_' + str(time.strftime("%d_%m_%Y_%H_%M_%S")) + '.jpg'
path = './images/' 
cv2.imwrite(os.path.join(path , og_imageName), image) 

# Process the original image
gray = cv2.cvtColor(image.copy(),cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(image.copy(), (7, 7), 0)
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 19, 2)#11, 3)
filtered = cv2.medianBlur(thresh,13) # 13
edged = cv2.Canny(filtered, 30, 150)

cv2.imshow("Input", image)
cv2.imshow("Canny", edged)
cv2.waitKey(0)

(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

sorted_cnts = sorted(cnts, key=lambda cnt: cv2.boundingRect(cnt)[0])
for i, ctr in enumerate(sorted_cnts):
    x,y,w,h = cv2.boundingRect(ctr)
    roi = img_og[y:y+h, x:x+w]
    # cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0),2)
    cv2.imwrite('./images/test_{}.png'.format(i), roi)

print("I count {} insects in this image".format(len(cnts)))

# Let's highlight the insects in the original image by drawing a
# green contour around them
edged_image = image.copy()
cv2.drawContours(edged_image, cnts, -1, (0, 255, 0), 1);

fullimg_name = './images/img_' + str(time.strftime("%d_%m_%Y_%H_%M_%S")) + '.jpg'
cv2.imwrite(fullimg_name,edged_image)