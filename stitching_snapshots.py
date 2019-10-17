
from picamera.array import PiRGBArray
from picamera import PiCamera
from imutils import paths
import imutils
import time
import cv2
import numpy as np
import os

snaps = []
positions = ['1','2','3']
snapdir = 'images/test/'

filelist = [ f for f in os.listdir(snapdir) if f.endswith(".png") ]
for f in filelist:
    os.remove(os.path.join(snapdir, f))

# Full list of Exposure and White Balance options. 120 photos
#list_ex  = ['auto','night','nightpreview','backlight',
#            'spotlight','sports','snow','beach','verylong',
#            'fixedfps','antishake','fireworks']

while True:
	# camera = PiCamera()
	# camera.resolution = (1000, 1088)
	# #camera.framerate = 2 # 32
	# camera.awb_mode = 'off'
	# camera.awb_gains = (2.5, 0.9)


	snap = input("Snapshot position?\n")

	assert isinstance(snap, str) and snap in positions, 'Try again!'
	snaps.append(snap)

	os.system("raspistill -t 3000 -awb off -awbg 2.5,0.9 -o images/test/snapshot_{}.png".format(snap))

	# rawCapture = PiRGBArray(camera, size=(1000, 1088))
	time.sleep(1.0)
	# camera.capture(rawCapture, format="bgr")
	# image = rawCapture.array



	# if not camera.closed:
		# camera.close()
	# image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
	# cv2.imwrite("images/test/snapshot_{}.png".format(snap), image)
	
	if set(snaps) == set(positions):
		end = input("Finished?\n")
		if end in ['y','Y','Yes','YES','yes']:
			break
		else:
			continue


args = {'crop':0,
		'images':'images/test',
		'output':'stitched_{}.png'.format(str(time.strftime("%d_%m_%Y_%H_%M_%S")))}

# grab the paths to the input images and initialize our images list
print("[INFO] loading images...")
imagePaths = sorted(list(paths.list_images(args["images"])))
images = []

# loop over the image paths, load each one, rotate them by 90 degrees 
# and add them to our images to stich list
for imagePath in imagePaths:
	image = cv2.imread(imagePath)
	image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
	images.append(image)

# initialize OpenCV's image sticher object and then perform the image
# stitching
print("[INFO] stitching images...")
stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
(status, stitched) = stitcher.stitch(images)

# if the status is '0', then OpenCV successfully performed image
# stitching
if status == 0:
	# check to see if we supposed to crop out the largest rectangular
	# region from the stitched image
	if args["crop"] > 0:
		# create a 10 pixel border surrounding the stitched image
		print("[INFO] cropping...")
		stitched = cv2.copyMakeBorder(stitched, 10, 10, 10, 10,
			cv2.BORDER_CONSTANT, (0, 0, 0))

		# convert the stitched image to grayscale and threshold it
		# such that all pixels greater than zero are set to 255
		# (foreground) while all others remain 0 (background)
		gray = cv2.cvtColor(stitched, cv2.COLOR_BGR2GRAY)
		thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

		# find all external contours in the threshold image then find
		# the *largest* contour which will be the contour/outline of
		# the stitched image
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		c = max(cnts, key=cv2.contourArea)

		# allocate memory for the mask which will contain the
		# rectangular bounding box of the stitched image region
		mask = np.zeros(thresh.shape, dtype="uint8")
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)

		# create two copies of the mask: one to serve as our actual
		# minimum rectangular region and another to serve as a counter
		# for how many pixels need to be removed to form the minimum
		# rectangular region
		minRect = mask.copy()
		sub = mask.copy()

		# keep looping until there are no non-zero pixels left in the
		# subtracted image
		while cv2.countNonZero(sub) > 0:
			# erode the minimum rectangular mask and then subtract
			# the thresholded image from the minimum rectangular mask
			# so we can count if there are any non-zero pixels left
			minRect = cv2.erode(minRect, None)
			sub = cv2.subtract(minRect, thresh)

		# find contours in the minimum rectangular mask and then
		# extract the bounding box (x, y)-coordinates
		cnts = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		c = max(cnts, key=cv2.contourArea)
		(x, y, w, h) = cv2.boundingRect(c)

		# use the bounding box coordinates to extract the our final
		# stitched image
		stitched = stitched[y:y + h, x:x + w]

	# write the output stitched image to disk
	cv2.imwrite(args["output"], stitched)

	# display the output stitched image to our screen
	# cv2.imshow("Stitched", stitched)
	# cv2.waitKey(0)

# otherwise the stitching failed, likely due to not enough keypoints)
# being detected
else:
	print("[INFO] image stitching failed ({})".format(status))





###################
	# # capture frames from the camera
	# for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
		# image = frame.array
		
		# # show the frame
		# #cv2.imshow("Frame", image)
		# key = cv2.waitKey(1) & 0xFF

		# # clear the stream in preparation for the next frame
		# rawCapture.truncate(0)

		# # if the `q` key was pressed, break from the loop
		# #if key == ord("q"):
		# image = rawCapture.array
		# image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
 
		# cv2.imwrite("images/test/snapshot_{}.png".format(snap), image)
