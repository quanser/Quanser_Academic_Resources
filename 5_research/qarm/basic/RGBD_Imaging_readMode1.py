from pal.products.qarm import QArmRealSense
import numpy as np
import time
import cv2

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## Timing Parameters and methods
startTime = time.time()
def elapsed_time():
    return time.time() - startTime

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# Additional parameters
counter = 0
imageWidth = 640
imageHeight = 480

#Initial Setup
runTime = 60.0 # seconds
max_distance = 1 # meters (for depth camera)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## Initialize the RealSense camera for RGB and Depth data
# change hardware to 1 if using a physical arm instead of a virtual one.
with QArmRealSense(mode='RGB&DEPTH',
                   hardware=0,
                   deviceID= 0,
                   frameWidthRGB=imageWidth,
                   frameHeightRGB=imageHeight,
                   frameWidthDepth=imageWidth,
                   frameHeightDepth=imageHeight,
                   readMode = 1) as myCam1:

    t0 = time.time()
    while time.time() - t0 < runTime:


        # cameras will only give data when new data is available
        myCam1.read_RGB()
        cv2.imshow('My RGB', myCam1.imageBufferRGB)

        myCam1.read_depth()
        cv2.imshow('My Depth', myCam1.imageBufferDepthPX/max_distance)

        cv2.waitKey(1)
