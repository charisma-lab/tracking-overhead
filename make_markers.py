import cv2
import numpy as np

d = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
dict_path = "marker_dictionary/"

NUMBER_OF_MARKERS = 10

def make_markers(number_of_markers=10):
	for i in range(number_of_markers):
		img = cv2.aruco.drawMarker(d, i, 1000)
		# cv2.imshow("marker", img)
		cv2.imwrite(dict_path+"marker-"+str(i)+".jpg", img)
		# cv2.waitKey(0)

make_markers(NUMBER_OF_MARKERS)
