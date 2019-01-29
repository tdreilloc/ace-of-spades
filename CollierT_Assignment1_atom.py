import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

#Give me the name of the image file
path1 = '/home/tdreilloc/Documents/CS463/assignments/'
name = input("What's up, name of your image?")
#Append image name to rest of file path for ease of user inputs
path2 = path1 + name
#Show the image
img = cv.imread(path2, 0)

#Threshold to make binary image
ret,thresh1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
titles = ['original', 'binary']
images = [img, thresh1]
for i in range(2):
    plt.subplot(2,3,i+1),plt.imshow(images[i], 'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()
