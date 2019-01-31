# ace-of-spades

Download the .pgm images you'd like to analyze. Download the script. In the script, edit 'path1' to point to the directory the images are located in.

You may then run the script. When it asks you for the title of your image, enter it. It should concatinate the image title with the path in order to create 'path2', which will then be used by the script. Be aware that any change in titles will have to be edited in the script, as the 'if' cases are dependent on the current names of the images. 

Several in between images will be shown during the execution of the script. 

  1. The original image
  2. The binary image after thresholding
  3. In between stages during dilation and erosion
  4. Labeled image
  5. Labeled image with contours and centroids drawn on the detected objects
  
It will save a .csv file with the objects' characteristics as well as a .jpg with the final labeled & drawn image. 

NOTE: image1.pgm and image3.pgm seem to be in working order. All other images are not currently working.
