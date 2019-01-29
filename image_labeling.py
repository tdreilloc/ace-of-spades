#References:
#https://docs.opencv.org/3.3.1/d9/d61/tutorial_py_morphological_ops.html
#https://docs.opencv.org/3.4.2/dd/d49/tutorial_py_contour_features.html
#https://docs.opencv.org/3.3.1/d3/db4/tutorial_py_watershed.html
#https://stackoverflow.com/questions/46441893/connected-component-labeling-in-python?rq=1
#
#All credit goes to Alexander Reynolds, https://stackoverflow.com/users/5087436/alexander-reynolds
#in regards to labeling the connected components with colors


import cv2
import numpy as np
from matplotlib import pyplot as plt

#Give me the name of the image file
path1 = '/home/tdreilloc/Documents/CS463/assignments/'
name = input("What's up, name of your image?")

#Append image name to rest of file path for ease of user inputs
path2 = path1 + name

#Read the image
img = cv2.imread(path2, 0)

#Specify the connectivity
connectivity = 8

#Threshold to make inverted binary image
img = cv2.threshold(img, 160, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]

#Perform morphological closing
kernel = np.ones((4,4),np.uint8)
closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
cv2.imshow('closed',closing)
cv2.waitKey()

#Create labels on the closed binary image
ret, labels = cv2.connectedComponents(closing)

#Find contours and label all onnected components
contours,hierarchy = cv2.findContours(closing,1,2)
label_hue = np.uint8(179*labels/np.max(labels))
blank_ch = 255*np.ones_like(label_hue)
labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
labeled_img[label_hue==0] = 0

#Show labeled image
cv2.imshow('labeled image', labeled_img)
cv2.waitKey()

#Draw each rectangle for each object detected
i = 0
while i < len(contours):
    cnt = contours[i]
    M = cv2.moments(cnt)
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(labeled_img,[box],0,(0,0,255),2)
    i += 1

#Show final image
cv2.imshow('rectangle',labeled_img)
cv2.waitKey()
