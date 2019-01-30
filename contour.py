import numpy as np
import cv2 as cv

#Read image
img = cv.imread('/home/tdreilloc/Documents/CS463/assignments/image1.pgm', 0)
ret,thresh = cv.threshold(img,150,255,0)
cv.imshow('threshold',thresh)
cv.waitKey()
#Find contours in binary image
contours,hierarchy = cv.findContours(thresh,1,2)


#Draw each rectangle (bounding box?)
i = 1
while i <= len(contours):
    cnt = contours[i]
    M = cv.moments(cnt)
    rect = cv.minAreaRect(cnt)
    box = cv.boxPoints(rect)
    box = np.int0(box)
    cv.drawContours(thresh,[box],0,(0,0,255),2)
    area = cv.contourArea(cnt)
    print ("Object #"+str(i)+" = "+str(area))
    i += 1



#Show final image
cv.imshow('rectangle',thresh)
cv.waitKey()
