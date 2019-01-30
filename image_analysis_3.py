#References:
#https://docs.opencv.org/3.3.1/d9/d61/tutorial_py_morphological_ops.html
#https://docs.opencv.org/3.4.2/dd/d49/tutorial_py_contour_features.html
#https://docs.opencv.org/3.3.1/d3/db4/tutorial_py_watershed.html
#https://stackoverflow.com/questions/46441893/connected-component-labeling-in-python?rq=1
#
#All credit goes to Alexander Reynolds, https://stackoverflow.com/users/5087436/alexander-reynolds
#in regards to labeling the connected components with colors

#THIS SCRIPT WILL HAVE TO BE TWEAKED ACCORDING TO THE IMAGE


import cv2
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

#Give me the name of the image file
path1 = '/home/tdreilloc/Documents/CS463/assignments/'
name = input("What's up, name of your image?")

#Append image name to rest of file path for ease of user inputs
path2 = path1 + name

#Read the image
img = cv2.imread(path2, 0)
cv2.imshow('original', img)
cv2.waitKey()


#Specify the connectivity
connectivity = 8

#Threshold to make inverted binary image
img = cv2.threshold(img, 145, 255, cv2.THRESH_BINARY_INV)[1]
cv2.imshow('binary', img)
cv2.waitKey()

#kernel2 = np.ones((2,2),np.uint8)
#erosion = cv2.erode(img,kernel2,iterations = 1)
#cv2.imshow('eroded', erosion)
#cv2.waitKey()

#Perform dilation to close the holes in the 4s
kernel1 = np.ones((2,2),np.uint8)
dilation = cv2.dilate(img,kernel1,iterations = 1)
cv2.imshow('dilated', dilation)
cv2.waitKey()

#kernel3 = np.ones((2,1),np.uint8)
#erosion2 = cv2.erode(dilation,kernel3,iterations = 1)

#Create labels on the closed binary image
ret, labels = cv2.connectedComponents(dilation)

#Find contours and label all onnected components
#https://stackoverflow.com/questions/46441893/connected-component-labeling-in-python?rq=1
contours,hierarchy = cv2.findContours(dilation,1,2)
label_hue = np.uint8(179*labels/np.max(labels))
blank_ch = 255*np.ones_like(label_hue)
labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
labeled_img[label_hue==0] = 0

#Show labeled image
cv2.imshow('labeled image', labeled_img)
cv2.waitKey()

#Create array for geometric attributes
a = np.zeros(shape=(99,4), dtype=object)
#Column headers for data frame
names = ['Area', 'Centroid', 'Bounding box', 'Circularity']
#Index for data frame
index = [_ for _ in range(1,100,1)]
#Create data frame
df = pd.DataFrame(a, index=index, columns=names)

#Loop for each contour (object)
x = 1
i = 1
while i <= len(contours):
    cnt = contours[i-1]
    #Get area of contour and put it in the table
    area = cv2.contourArea(cnt)
    #Get moments
    M = cv2.moments(cnt)
    rect = cv2.minAreaRect(cnt)
    #Get bounding box and put it in table
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    #Get centroid and put it in the table
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    centroid = [cx, cy]
    #Get perimeter and make Circularity
    perimeter = cv2.arcLength(cnt,True)
    circularity = (int(perimeter)^2)/area
    if area < 18:
        x += 1
    else:
        a[i-x][0] = area
        a[i-x][1] = centroid
        a[i-x][2] = box
        a[i-x][3] = round(circularity, 2)
        #Draws bounding box on the image
        cv2.drawContours(labeled_img,[box],0,(150,150,255),1)
        #Draw centroid on image
        cv2.circle(labeled_img, (cx, cy), 2, (150,150,255), -1)
    i += 1

#Output data table to .csv file
df.to_csv('image_3.csv', index=True, header=True, sep=' ')

#Show final image
cv2.imwrite("/home/tdreilloc/Documents/CS463/assignments/image_3.jpg", labeled_img)
cv2.imshow('rectangle',labeled_img)
cv2.waitKey()
