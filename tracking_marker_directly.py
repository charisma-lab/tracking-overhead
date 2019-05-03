# Module to track fiducial markers and output their pose

import numpy as np
import cv2
import json
import math
import time
import csv
import sys

MAX_BOTS = 10
VIDEO_SOURCE_ID = 0


class Marker():

	def __init__(self):
		# position is (x,y)
		self._position = [0,0]
		# orientation is theta
		self._orientation = 0

	def update_pose(self, position, orientation):
		self._position = position
		self._orientation = orientation

class Tracker():

	def __init__(self):
		self._cap = cv2.VideoCapture(VIDEO_SOURCE_ID)
		self._dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
		self._gray2 = create_blank(1920, 1080, rgb_color=(0, 0, 0))

	def track_every_frame(self):
		ret, frame = self._cap.read()
		cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
		cv2.resizeWindow('frame', 1280, 960)
		gray = frame
		self._detected_markers = cv2.aruco.detectMarkers(gray, self._dictionary)
		if len(self._detected_markers[0]) > 0:
			for (fids, index) in zip(self._detected_markers[0], self._detected_markers[1]):
				for pt in fids:
					try:
						if (int(index[0])==0):
							ll = ((pt[0] +pt[1] +pt[2] +pt[3])/4)
							cv2.circle(gray,(ll[0],ll[1]), 15, (0,0,255), -1)
							cv2.circle(self._gray2,(ll[0],ll[1]), 15, (0,0,255), -1)
						elif (int(index[0])==1):
							ll = ((pt[0] +pt[1] +pt[2] +pt[3])/4)
							cv2.circle(gray,(ll[0],ll[1]), 15, (0,255,0), -1)
							cv2.circle(self._gray2,(ll[0],ll[1]), 15, (0,255,0), -1)
						elif (int(index[0])==3):
							ll = ((pt[0] +pt[1] +pt[2] +pt[3])/4)
							cv2.circle(gray,(ll[0],ll[1]), 15, (255,255,0), -1)
						elif (int(index[0])==2):
							ll = ((pt[0] +pt[1] +pt[2] +pt[3])/4)
							cv2.circle(gray,(ll[0],ll[1]), 15, (255,0,0), -1)
							cv2.circle(self._gray2,(ll[0],ll[1]), 15, (255,0,0), -1)
					except IndexError:
						pass

		if len(self._detected_markers[0]) > 0:
			cv2.aruco.drawDetectedMarkers(gray, self._detected_markers[0], self._detected_markers[1])
		cv2.imshow('frame',gray)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			# When everything done, release the capture
			self._cap.release()
			cv2.destroyAllWindows()
			sys.exit()


# for creating a blank image
def create_blank(width, height, rgb_color=(0, 0, 0)):
	"""Create new image(numpy array) filled with certain color in RGB"""
	# Create black blank image
	image = np.zeros((height, width, 3), np.uint8)
	# Since OpenCV uses BGR, convert the color first
	color = tuple(reversed(rgb_color))
	# Fill image with color
	image[:] = color
	return image

if __name__ == "__main__":
	watch_dogs = Tracker()
	while (True):
		watch_dogs.track_every_frame()
