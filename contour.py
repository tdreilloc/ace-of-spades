import numpy as np
import cv2 as cv
import pandas as pd

#Read image
img = cv.imread('/home/tdreilloc/Documents/CS463/assignments/image1.pgm', 0)
ret,thresh = cv.threshold(img,150,255,0)
cv.imshow('threshold',thresh)
cv.waitKey()

#Find contours in binary image
contours,hierarchy = cv.findContours(thresh,1,2)


#Create array for geometric attributes
a = np.zeros(shape=(14,4), dtype=object)
#Column headers for data frame
names = ['Area', 'Centroid', 'Bounding box', 'Circularity']
#Index for data frame
index = [_ for _ in range(14)]
#Create data frame
df = pd.DataFrame(a, index=index, columns=names)

#Loop for each contour (object)
i = 1
while i < len(contours):
    cnt = contours[i]
    #Get moments
    M = cv.moments(cnt)
    rect = cv.minAreaRect(cnt)
    #Get bounding box and put it in table
    box = cv.boxPoints(rect)
    a[i-1][2] = box
    box = np.int0(box)
    #Draws bounding box on the image
    cv.drawContours(thresh,[box],0,(150,150,255),2)
    #Get area of contour and put it in the table
    area = cv.contourArea(cnt)
    a[i-1][0] = area
    #Get centroid and put it in the table
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    centroid = [cx, cy]
    a[i-1][1] = centroid
    #Draw centroid on image
    cv.circle(thresh, (cx, cy), 3, (150,150,255), -1)

    i += 1

#Output data table to .csv file
df.to_csv('output.csv', index=True, header=True, sep=' ')
print (df)


#Show final image
cv.imshow('rectangle',thresh)
cv.waitKey()
