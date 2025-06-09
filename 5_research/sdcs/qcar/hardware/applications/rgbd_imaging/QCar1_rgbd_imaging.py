## rgbd_imaging.py
# This example combines the depth and RGB sensors from the Intel Realsense D435 to display objects 
# within a specified distance. For troubleshooting the Realsense camera use hardware_test_intelrealsense.py
# found in the hardwate_tests folder.  

from pal.utilities.vision import Camera3D
from hal.utilities.image_processing import ImageProcessing

import time
import struct
import numpy as np 
import cv2

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
## Timing Parameters and methods 
startTime = time.time()
def elapsed_time():
    return time.time() - startTime

sampleRate     = 30.0
sampleTime     = 1/sampleRate
simulationTime = 30.0
print('Sample Time: ', sampleTime)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
# Additional parameters
imageWidth  = 1280
imageHeight = 720

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
## Initialize the RealSense camera for RGB and Depth data
myCam1  = Camera3D(mode='RGB&DEPTH', frameWidthRGB=imageWidth, frameHeightRGB=imageHeight)
# max_distance_view = 5
MAX_DISTANCE = 0.6 # pixels in RGB image farther than this will appear white  
MIN_DISTANCE = 0.0001 # pixels in RGB image closer than this will appear black

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

## Main Loop
flag = True
try:
    while elapsed_time() < simulationTime:
        # Start timing this iteration
        start = time.time()

        # Read the RGB and Depth data (latter in meters)
        myCam1.read_RGB()
        myCam1.read_depth(dataMode='M')
        
        # Threshold the depth image based on min and max distance set above, and cast it to uint8 (to be used as a mask later)
        binaryNow = ImageProcessing.binary_thresholding(myCam1.imageBufferDepthM, MIN_DISTANCE, MAX_DISTANCE).astype(np.uint8)
        
        # Initialize binaryBefore to keep a 1 step time history of the binary to do a temporal difference filter later. 
        # At the first time step, flag = True. Initialize binaryBefore and then set flag = False to not do this again.
        if flag:
            binaryBefore = binaryNow
            flag = False
        
        # clean  =  closing filter applied ON ( binaryNow BITWISE AND ( BITWISE NOT of ( the ABSOLUTE of ( difference between binary now and before ) ) ) )
        binaryClean = ImageProcessing.image_filtering_close(cv2.bitwise_and( cv2.bitwise_not(np.abs(binaryNow - binaryBefore)/255), binaryNow/255 ), dilate=3, erode=1, total=1)

        # grab a smaller chunk of the depth data and scale it back to full resolution to account for field-of-view differences and physical distance between the RGB/Depth cameras.
        binaryClean = cv2.resize(binaryClean[81:618, 108:1132], (1280, 720)).astype(np.uint8)

        # Apply the binaryClean mask to the RGB image captured, and then display it.
        maskedRGB = cv2.bitwise_and(myCam1.imageBufferRGB, myCam1.imageBufferRGB, mask=binaryClean)
        cv2.imshow('Original', cv2.resize(maskedRGB, (640, 360)))
        
        # End timing this iteration
        end = time.time()

        # Calculate the computation time, and the time that the thread should pause/sleep for
        computationTime = end - start
        sleepTime = sampleTime - ( computationTime % sampleTime )

        # Pause/sleep for sleepTime in milliseconds
        msSleepTime = int(1000*sleepTime)
        if msSleepTime <= 0:
            msSleepTime = 1
        cv2.waitKey(msSleepTime)
        binaryBefore = binaryNow

except KeyboardInterrupt:
    print("User interrupted!")

finally:    
    # Terminate RealSense camera object
    myCam1.terminate()
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 