from pal.utilities.vision import Camera3D
import numpy as np
import time
import cv2

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## Timing Parameters and methods
startTime = time.time()
def elapsed_time():
    return time.time() - startTime

sampleRate = 30.0
sampleTime = 1/sampleRate
simulationTime = 600.0
print('Sample Time: ', sampleTime)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# Additional parameters
counter = 0
imageWidth = 640
imageHeight = 480

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## Initialize the RealSense camera for RGB and Depth data
hardware = 1
if hardware:
    id = '0'
else:
    id = '0@tcpip://localhost:18901'

myCam1 = Camera3D(mode='RGB&DEPTH', frameWidthRGB=imageWidth, frameHeightRGB=imageHeight,
                                frameWidthDepth=imageWidth, frameHeightDepth=imageHeight, deviceId=id, readMode=0)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## Main Loop
flag = True
try:
    while elapsed_time() < simulationTime:
        # Start timing this iteration
        start = time.time()

        # Read the RGB and Depth data (latter in meters)
        myCam1.read_RGB()
        cv2.imshow('Original RGB', myCam1.imageBufferRGB)
        if hardware:
            myCam1.read_depth(dataMode='M')
            cv2.imshow('Original Depth', myCam1.imageBufferDepthM)
        else:
            myCam1.read_depth(dataMode='PX')
            cv2.imshow('Original Depth', myCam1.imageBufferDepthPX)

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
        # binary_before = binary_now

except KeyboardInterrupt:
    print("User interrupted!")

finally:
    # Terminate RealSense camera object
    myCam1.terminate()
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --