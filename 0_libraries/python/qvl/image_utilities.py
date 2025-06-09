import numpy as np
import cv2

# Convert a color image to HSV, filter for hues within a certain width of center
# hueCenter - The hue being searched for
# hueWidth - The width of the range of hue values to accept
# hueGamut - The max hue value. Open CV uses 180, set this to 255 for normal hue values
def hue_threshold(image, hueCenter = 0, hueWidth = 20, hueGamut = 180):

    invert = False
    # Scale for incompatible hue gamut
    if hueGamut != 180:
        scale = 180/hueGamut
        hueCenter = scale * hueCenter
        hueWidth = scale * hueWidth

    # Set min and max hue values and general limits for saturation and value
    hMin = (hueCenter - (hueWidth/2)) % 180
    hMax = (hueCenter + (hueWidth/2)) % 180
    svMin = 64.0
    svMax = 255.0

    # Convert and threshold image
    imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    bottomBounds = np.array([0.0,svMin,svMin])
    lowerBounds = np.array([hMin,svMin,svMin])
    upperBounds = np.array([hMax,svMax,svMax])
    topBounds = np.array([179.9,svMax,svMax])

    #Threshold for hue, special case for values that wrap past zero
    if hMin < hMax:
        binary = cv2.inRange(imageHSV, lowerBounds, upperBounds)
    else:
        binaryLow = cv2.inRange(imageHSV, bottomBounds, upperBounds)
        binaryHigh = cv2.inRange(imageHSV, lowerBounds, topBounds)
        binary = cv2.bitwise_or(binaryLow, binaryHigh)
	
    return binary

# Crop an image to extract a region of interest using x and y ranges of pixels
def crop_rect(image, xRange = [0,0], yRange = [0,0]):
    if xRange[1] > xRange[0] and yRange[1] > yRange[0]:
        imageCrop = image[yRange[0]:yRange[1], xRange[0]:xRange[1]]
    else:
        imageCrop = image

    return imageCrop

# Draw a rectangle over an image to indicate the region of interest
def show_ROI(image, xRange = [0,0], yRange = [0,0]):

    image = cv2.rectangle(image, (xRange[0], yRange[0]), (xRange[1], yRange[1]), (255, 128, 128), 2)

    return image

# Draw the rectangle ROI with a vertical line indicating the target center
def show_ROI_target(image, xRange = [0,0], yRange = [0,0], targ = -1):
    
    image = show_ROI(image, xRange, yRange)
    
    tRange = [yRange[0] - 10, yRange[1] + 10]

    if targ == -1:
        image = cv2.line(image, (320, tRange[0]), (320, tRange[1]), (0, 0, 255), 4)
    else:
        tX = int(round(targ))
        image = cv2.line(image, (tX, tRange[0]), (tX, tRange[1]), (128, 255, 128), 4)

    return image

# Find the center of a line in a thresholded image
def extract_line_ctr(image):

    center = -1

    # Average the pixels in each column and find the maximum value
    columnVals = np.mean(image, axis = 0)
    maxCol = np.amax(columnVals)

    #Check for lost line and return the average x position of max values. Else, return -1
    if maxCol > 64:
        center = np.mean(np.argwhere(columnVals == maxCol))

    return center
