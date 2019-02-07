import cv2
import tkinter as tk
import numpy as np
from tkinter import filedialog
from tkinter import *

# opens GUI window
root = tk.Tk()
root.title("Image Analysis Program")
root.geometry('300x500')

# creates frame
frame_main = tk.Frame(root, bg="white")
frame_main.grid(sticky='news')

# Welcome Title
label1 = tk.Label(frame_main, text="Image Analysis Program\n\nWelcome!\n\n\n", fg='blue', font=("Helvetica Bold", 16))
label1.grid(row=0, column=0, sticky='news')

# creates frame for the canvas for objects to appear in later
frame_canvas = tk.Frame(frame_main)
frame_canvas.grid(row=3, column=0, sticky='news')
# doesnt allow frame to chnage size
frame_canvas.pack_propagate(0)

# Add a canvas in that frame
canvas = tk.Canvas(frame_canvas, bg="gray")
canvas.grid(row=0, column=0, sticky="news")


# function, when browse button is clicked
def browse_file():
    # opens dialog box for file
    path2 = filedialog.askopenfilename()

    # reads and shows image
    img = cv2.imread(path2, 0)
    cv2.imshow('original', img)
    cv2.waitKey()

    # setting points for specified images
    if 'image1.pgm' in path2:
        threshold = 127
        dil1 = 3
        dil2 = 3
        setpoint = 20

    if 'image2.pgm' in path2:
        threshold = 130
        ero1 = 2
        ero2 = 2
        dil1 = 4
        dil2 = 4
        setpoint = 20

    if 'image3.pgm' in path2:
        threshold = 148
        dil1 = 2
        dil2 = 2
        setpoint = 18

    if 'image4.pgm' in path2:
        threshold = 68
        ero1 = 6
        ero2 = 5
        dil1 = 6
        dil2 = 6
        setpoint = 20

    if 'image5.pgm' in path2:
        threshold = 127
        ero1 = 2
        ero2 = 2
        dil1 = 3
        dil2 = 3
        setpoint = 20

    # Specify the connectivity
    connectivity = 8

    # Threshold to make inverted binary image
    img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY_INV)[1]
    cv2.imshow('binary', img)
    cv2.waitKey()

    # Perform dilation to close the holes in the 4s
    kernel1 = np.ones((dil1, dil2), np.uint8)
    img = cv2.dilate(img, kernel1, iterations=1)
    cv2.imshow('dilated', img)
    cv2.waitKey()

    # Only perform on image4
    if 'image4.pgm' in path2:
        kernel2 = np.ones((ero1, ero2), np.uint8)
        img = cv2.erode(img, kernel2, iterations=1)
        cv2.imshow('eroded', img)
        cv2.waitKey()

    # Create labels on the closed binary image
    ret, labels = cv2.connectedComponents(img)

    # Find contours and label all connected components
    # https://stackoverflow.com/questions/46441893/connected-component-labeling-in-python?rq=1
    contours, hierarchy = cv2.findContours(img, 1, 2)


    label_hue = np.uint8(179 * labels / np.max(labels))
    blank_ch = 255 * np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
    labeled_img[label_hue == 0] = 0

    # Show labeled image
    cv2.imshow('labeled image', labeled_img)
    cv2.waitKey()

    # creates a textbox where images will be displayed
    t = Text(frame_canvas, width=100, height=60, bg='gray')
    t.grid_propagate(False)

    # Loop for each contour (object)
    x = 1
    i = 1
    y = 0
    while i <= len(contours):
        cnt = contours[i-1]
        # Get area of contour and put it in the table
        area = cv2.contourArea(cnt)
        if area >= setpoint:
            y +=1
        # Get moments
        M = cv2.moments(cnt)
        rect = cv2.minAreaRect(cnt)
        # Get bounding box and put it in table
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        if M['m00'] > 0:
            # Get centroid and put it in the table
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            centroid = [cx, cy]
        # Get perimeter and make Circularity
        perimeter = cv2.arcLength(cnt, True)
        if area > 0:
            circularity = (int(perimeter) ^ 2) / area
        if area < setpoint:
            x += 1
        else:
            a = ["Object: ", y, "\nArea: ", area, "\nCentroid: ", centroid, "\nBounding Box: \n", box,
                 "\nCircularity: ", round(circularity, 2), "\n\n"]
            ##loop to insert into text
            for x in range(0, 11):
                root.update()
                t.insert(END, a[x])
            t.pack()

            # cv2.drawText(labeled_img, [box], i)
            # Draws bounding box on the image
            cv2.drawContours(labeled_img, [box], 0, (150, 150, 255), 1)
            # Draw centroid on image
            cv2.circle(labeled_img, (cx, cy), 2, (150, 150, 255), -1)
            # Draw Index
            cv2.putText(labeled_img, str(y), (cx, cy), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.75, (255, 255, 255))
        i += 1
    # shows labeled box, dont put WaitKey otherwise scrolling does not work
    cv2.imshow('rectangle', labeled_img)

# creates browse button
buttons = tk.Button(frame_canvas, text="Browse...", command=browse_file)
buttons.grid(sticky='news')

# Launch the GUI
root.mainloop()

