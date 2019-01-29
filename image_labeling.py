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

connectivity = 8

img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
ret, labels = cv2.connectedComponents(img)

label_hue = np.uint8(179*labels/np.max(labels))
blank_ch = 255*np.ones_like(label_hue)
labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

labeled_img[label_hue==0] = 0

cv2.imshow('labeled image', labeled_img)
cv2.waitKey()

