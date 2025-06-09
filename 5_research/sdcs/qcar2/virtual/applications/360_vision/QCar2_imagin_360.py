## imaging_360.py
# This example demonstrates how to read all 4 csi cameras and display in a single openCV window. If you encounter any errors, 
# use the hardware_test_csi_camera.py script to find out which camera is giving you trouble. 

from pal.utilities.vision import Camera2D
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
simulationTime = 60.0
print('Sample Time: ', sampleTime)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
# Additional parameters
imageWidth = 640
imageHeight = 480
imageBuffer360 = np.zeros((imageHeight + 40, 4*imageWidth + 120, 3), dtype=np.uint8) # 20 px padding between pieces  
        
# Stitch images together with black padding
horizontalBlank     = np.zeros((20, 4*imageWidth+120, 3), dtype=np.uint8)
verticalBlank       = np.zeros((imageHeight, 20, 3), dtype=np.uint8)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
## Initialize the CSI cameras and probe
myCam1 = Camera2D(cameraId="0@tcpip://localhost:18961", frameWidth=imageWidth, frameHeight=imageHeight, frameRate=sampleRate)
myCam2 = Camera2D(cameraId="1@tcpip://localhost:18962", frameWidth=imageWidth, frameHeight=imageHeight, frameRate=sampleRate)
myCam3 = Camera2D(cameraId="2@tcpip://localhost:18963", frameWidth=imageWidth, frameHeight=imageHeight, frameRate=sampleRate)
myCam4 = Camera2D(cameraId="3@tcpip://localhost:18964", frameWidth=imageWidth, frameHeight=imageHeight, frameRate=sampleRate)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
## Main Loop
try:
    while elapsed_time() < simulationTime:
        # Start timing this iteration
        start = time.time()

        # Capture RGB Image from CSI
        flag1=myCam1.read()
        flag2=myCam2.read()
        flag3=myCam3.read()
        flag4=myCam4.read()

        imageBuffer360 = np.concatenate(
                                        (horizontalBlank, 
                                            np.concatenate((    verticalBlank, 
                                                                myCam2.imageData[:,320:640], 
                                                                verticalBlank, 
                                                                myCam3.imageData, 
                                                                verticalBlank, 
                                                                myCam4.imageData, 
                                                                verticalBlank, 
                                                                myCam1.imageData, 
                                                                verticalBlank, 
                                                                myCam2.imageData[:,0:320], 
                                                                verticalBlank), 
                                                                axis = 1), 
                                            horizontalBlank
                                            ), 
                                            axis=0
                                        )
        # Display the stitched image at half the resolution
        cv2.imshow('Combined View', cv2.resize(imageBuffer360,
                                            (int(2*imageWidth),
                                            int(imageHeight/2))))
        
        # End timing this iteration
        end = time.time()

        # Calculate the computation time, and the time that the thread should pause/sleep for
        computationTime = end - start
        sleepTime = sampleTime - ( computationTime % sampleTime )
        
        # Pause/sleep for sleepTime in milliseconds
        msSleepTime = int(1000*sleepTime)
        if sleepTime <= 0:
            sleepTime = 0 
        cv2.waitKey(msSleepTime)

except KeyboardInterrupt:
    print("User interrupted!")

finally:
    # Terminate all webcam objects    
    myCam1.terminate()
    myCam2.terminate()
    myCam3.terminate()
    myCam4.terminate()
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 