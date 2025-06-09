## example_test_qbot_camera.py
# This example lets you view images from the QBot camera (hardware or virtual, select device ID accordingly 
# on line 38/39). Ensure that you start the Quanser Interactive Labs - QBot 2e Workspace before using 
# the virtual QBot. 
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
#imports
from pal.utilities.vision import Camera3D
import time
import cv2

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
## Timing Parameters and methods 
startTime = time.time()
def elapsed_time():
    return time.time() - startTime

sampleRate = 60.0
sampleTime = 1/sampleRate
simulationTime = 120.0
print('Sample Time: ', sampleTime)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
# Additional parameters
counter = 0
imageWidth = 640
imageHeight = 480

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
## Initialize the RealSense camera for RGB and Depth data

# deviceId = '0'                         # hardware camera id for qbot 3
deviceId = '0@tcpip://localhost:18911' # virtual qbot 2e camera

myCam = Camera3D(mode='RGB&DEPTH', frameWidthRGB=imageWidth, frameHeightRGB=imageHeight, frameWidthDepth=imageWidth, frameHeightDepth=imageHeight, deviceId=deviceId)
counter = 0

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
## Main Loop
try:
    while elapsed_time() < simulationTime:
        # Start timing this iteration
        start = time.time()

        # Capture RGB and depth data
        myCam.read_RGB()
        myCam.read_depth(dataMode='PX')
        counter += 1
        
        # End timing this iteration
        end = time.time()

        # Display the two images
        cv2.imshow('My RGB', myCam.imageBufferRGB)
        cv2.imshow('My Depth', myCam.imageBufferDepthPX) # by default, ranges between 0 to 1 meters will show up in grayscale. Beyond 1 m, everything will look white. 
                                                            # apply a gain of 0.5 to improve range to 2 meters, 0.33 for 3 meters and so on
        # cv2.imshow('My Depth', 30*myCam.image_buffer_depth_px) # apply a gain of 30 to visualize data if using pixels

        # Pause/sleep for 1 milliseconds (the camera3D object will handle timing)
        cv2.waitKey(1)

except KeyboardInterrupt:
    print("User interrupted!")

finally:    
    # Terminate RealSense camera object
    myCam.terminate()
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 