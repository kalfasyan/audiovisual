from picamera.array import PiRGBArray
from picamera import PiCamera
from imutils import paths
import imutils
import time
import cv2
import numpy as np
import os
import pandas as pd
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import os

locations = ["beauvech", "brainelal", "kampen"]
dates = ["w38", "w39", "w40", "w41", "w42"]
a_or_b = ['A','B','C']
positions = ['1','2','3']


def choose(a):
	for i,ch in enumerate(a):
		print("{} : {}".format(i,ch))
	choice = input("Your choice: \n")
	assert int(choice) in range(len(a)), "Choice out of range!"
	return choice

while True:
	print("\n### NEW STICKY PLATE CHOICES ###:\n")
	loc = locations[int(choose(locations))]
	print("Chosen location: {}\n".format(loc))
	date = dates[int(choose(dates))]
	ab = a_or_b[int(choose(a_or_b))]
	print("\nChosen side: {}\n".format(ab))

	#print("Chosen date: {}\n".format(date))
	#idx = 1#int(input("Chosen index:"))
	print("\n")
	print("\nFILENAME: {}_{}_{}".format(loc,date,ab))

	curr_platedir = 'images/{}{}{}/'.format(loc,date,ab)
	if not os.path.isdir(curr_platedir):
		os.mkdir(curr_platedir)

	snaps = []

	filelist = [ f for f in os.listdir(curr_platedir) if f.endswith(".png") ]
	for f in filelist:
		os.remove(os.path.join(curr_platedir, f))

	while True:
		snap = input("Snapshot position?\n")
		assert isinstance(snap, str) and snap in positions, 'Try again!'
		snaps.append(snap)

		os.system("raspistill -t 1500 -awb auto -sh 100 -q 100 -o images/{}{}{}/{}_{}_{}_{}.png".format(loc,date,ab,loc,date,ab,snap))
		time.sleep(1.0)

		if set(snaps) == set(positions):
			end = input("Finished?\n")
			if end in ['y','Y','Yes','YES','yes']:
				break
			else:
				continue


	args = {'crop':0,
			'images': curr_platedir,
			'output':"images/{}{}{}/{}_{}_{}_stiched.png".format(loc,date,ab,loc,date,ab)}
				#'stitched_{}.png'.format(str(time.strftime("%d_%m_%Y_%H_%M_%S")))}

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
	print("[INFO] stitching images...{}".format(imagePaths))
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
