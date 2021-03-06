#https://docs.opencv.org/3.3.1/d3/db4/tutorial_py_watershed.html

import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('/home/tdreilloc/Documents/CS463/assignments/image1.pgm')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

cv2.imshow('result', thresh)
cv2.waitKey()
#noise removal
kernel = np.ones((3,3), np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 1)

#sure background area
sure_bg = cv2.dilate(opening,kernel,iterations=1)

#finding sure foreground area
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
ret, sure_fg = cv2.threshold(dist_transform,0.1*dist_transform.max(),255,0)

#finding unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)

#marker labeling
ret, markers = cv2.connectedComponents(sure_fg)

#add one to all labels so that sure background is not 0, but 1
markers = markers+1

#now, mark the region of unknown with zero
markers[unknown==255] = 0

#apply watershed algorithm
markers = cv2.watershed(img,markers)
img[markers == -1] = [255,0,0]

cv2.imshow('final', img)
cv2.waitKey()
