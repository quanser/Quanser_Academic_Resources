from pal.products.qarm import QArmRealSense
import numpy as np
import time
import cv2

# if readMode is set to 0, the user has to keep timing for the next frame.
# if readMode is set to 1, the timing is done automatically since we only read a frame when one is available.
# examples for both are provided under RGBD_Imaging_readMode0 and RGBD_Imaging_readMode1.

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## Timing Parameters and methods
startTime = time.time()
def elapsed_time():
    return time.time() - startTime

sampleRate = 30.0
sampleTime = 1/sampleRate
simulationTime = 60.0
print('Sample Time: ', sampleTime)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# Additional parameters
counter = 0
imageWidth = 640
imageHeight = 480

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
                   readMode = 0) as myCam1:

    t0 = time.time()
    while time.time() - t0 < simulationTime:
        start = time.time()

        # cameras will only give data when new data is available
        myCam1.read_RGB()
        cv2.imshow('My RGB', myCam1.imageBufferRGB)

        myCam1.read_depth()
        cv2.imshow('My Depth', myCam1.imageBufferDepthPX/max_distance)

        end = time.time()

        # Calculate the computation time, and the time that the thread should pause/sleep for
        computationTime = end - start
        sleepTime = sampleTime - ( computationTime % sampleTime )

        # Pause/sleep for sleepTime in milliseconds
        msSleepTime = int(1000*sleepTime)

        if msSleepTime <= 0:
            msSleepTime = 1
        cv2.waitKey(msSleepTime)
