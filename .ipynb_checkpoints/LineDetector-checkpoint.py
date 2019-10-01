#!/usr/bin/env python
# coding: utf-8

# In[2]:


import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import math
from moviepy.editor import VideoFileClip
from IPython.display import HTML
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required = True, help = "Path to input video")
args = vars(ap.parse_args())

def region_of_interest(img, vertices):
    # Define a mask
    mask = np.zeros_like(img)
    
    # Fill inside the poligon
    mask_color = 255
    
    # Fill polygon
    cv2.fillPoly(mask, vertices, mask_color)

    # Detect region of interest
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

global count
global prev_line_img
count = 0
prev_line_img = None

def draw_lines(img, lines, color=[0, 255, 0], thickness=3, line_draw_frequency = 25, num_of_channels = 3):
    
    global count
    global prev_line_img
    # If there are no lines to draw, exit.
    if lines is None:
        return
    # Make a copy of the original image.
    img = np.copy(img)
    # Create a blank image that matches the original in size.
    line_img = np.zeros(
        (
            img.shape[0],
            img.shape[1],
            num_of_channels
        ),
        dtype=np.uint8,
    )

    left_line_x = []
    left_line_y = []
    right_line_x = []
    right_line_y = []
    
    # Loop over all lines and draw them on the blank image.
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_img, (x1, y1), (x2, y2), color, thickness)
    # Add lines to image
    if count % line_draw_frequency == 0:
        img = cv2.addWeighted(img, 0.8, line_img, 1.0, 0.0)
        prev_line_img = line_img
    else:
        img = cv2.addWeighted(img, 0.8, prev_line_img, 1.0, 0.0)

    count += 1 
    # Return the modified image.
    return img

# Define pipeline
def pipeline(image):
    
    if image is None:
        return
    height = image.shape[0]
    width = image.shape[1]

    # Define region of interest (triangle)
    region_of_interest_vertices = [
        (0, height),
        (width / 2, height / 2),
        (width, height)
    ]
    
    # Convert image to gray scale
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    # Find edges in the image
    cannyed_image = cv2.Canny(gray_image, 100, 200)

    # Crop image according to region_of_interest_vertices
    cropped_image = region_of_interest (
        cannyed_image,
        np.array([region_of_interest_vertices], np.int32)
    )

    # Find lines
    lines = cv2.HoughLinesP(
        cropped_image,
        rho=6,
        theta=np.pi / 60,
        threshold=160,
        lines=np.array([]),
        minLineLength=40,
        maxLineGap=25
    )
    # Define borders
    left_line_x = []
    left_line_y = []
    right_line_x = []
    right_line_y = []

    for line in lines:
        for x1, y1, x2, y2 in line:
            # Calculate the slope.
            slope = (y2 - y1) / (x2 - x1) 
            if math.fabs(slope) < 0.5:
                continue
            # Detect if line should be attached to left or right group
            if slope <= 0:
                left_line_x.extend([x1, x2])
                left_line_y.extend([y1, y2])
            else: # <-- Otherwise, right group.
                right_line_x.extend([x1, x2])
                right_line_y.extend([y1, y2])

    min_y = image.shape[0] * (3 / 5) # <-- Just below the horizon
    max_y = image.shape[0] # <-- The bottom of the image

    # Create 1D polynomial for left line
    poly_left = np.poly1d(np.polyfit(
        left_line_y,
        left_line_x,
        deg=1
    ))

    left_x_start = int(poly_left(max_y))
    left_x_end = int(poly_left(min_y))

    # Create 1D polynomial for right line
    poly_right = np.poly1d(np.polyfit(
        right_line_y,
        right_line_x,
        deg=1
    ))

    right_x_start = int(poly_right(max_y))
    right_x_end = int(poly_right(min_y))
    
    # Draw lines
    line_image = draw_lines(
        image,
        [[
            [left_x_start, int(max_y), left_x_end, int(min_y)],
            [right_x_start, int(max_y), right_x_end, int(min_y)],
        ]],
        thickness = 3
    )

    return line_image
    
white_output = 'output.mp4'
clip1 = VideoFileClip(args['input'])
white_clip = clip1.fl_image(pipeline)
white_clip.write_videofile(white_output, audio=False)


# In[ ]:




