## virtual_qbot_line_following.py
# This example lets you drive the QBot 2e hardware with it's camera view while following a line. 
# Ensure that you start the Quanser Interactive Labs - QBot 2e Workspace before running this script.
# This example can also be used on the hardware, after you make changes as shown from lines 41 to 49. 
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
#region: imports
from pal.products.qbot import QBot3
from pal.utilities.vision import Camera3D
import numpy as np
import time
import cv2
#endregion
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
#region: Timing Parameters and methods 
startTime = time.time()
def elapsed_time():
    return time.time() - startTime

sampleRate = 30.0
sampleTime = 1/sampleRate
simulationTime = 120 # some large number
print('Simulation rate is set to', sampleRate, '...')

# Additional parameters
counter = 0
imageWidth = 640
imageHeight = 480

#endregion
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
#region: Initialize QBot3 object

# Hardware Setup:
# deviceId = '0' # hardware qbot 3 camera
# myCam    = Camera3D(mode='RGB', readMode=0, frameWidthRGB=imageWidth, frameHeightRGB=imageHeight, deviceId=deviceId)
# myQBot   = QBot3(hardware=1, readMode=1, frequency=int(sampleRate))

# Virtual Setup:
deviceId = '0@tcpip://localhost:18911' # virtual qbot 2e camera
myCam    = Camera3D(mode='RGB', readMode=0, frameWidthRGB=imageWidth, frameHeightRGB=imageHeight, deviceId=deviceId)
myQBot   = QBot3(hardware=0, readMode=1, frequency=int(sampleRate))

startTime = time.time()
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

#endregion
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
#region: Main Loop
try:
    prev = elapsed_time() - sampleTime
    
    while elapsed_time() < simulationTime:
        
        # Start timing this iteration
        start = elapsed_time()

        # Capture RGB and depth data
        ret = myCam.read_RGB()
        rightWheelVel = 0
        leftWheelVel = 0
        if ret >= 0:
            lowerBounds = (0, 0, 100)       # color thresholds must be updated for tracking your colored line in a physical setup.
            upperBounds = (100, 100, 255)   # note that these are in BGR format, not RGB. 
            dest = cv2.inRange(myCam.imageBufferRGB, lowerBounds, upperBounds)
            mask = dest[340:400]    # focus on the bottom rows
            
            # Figure out the location of the blob in the middle, and calculate turning velocity based on this. 
            M = cv2.moments(mask)
            if M["m00"] > 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            
                turnVel = (320 - cX)/320
                counter += 1
                forwardVel = 0.0
                if counter > 100:
                    forwardVel = 0.25

                rightWheelVel = forwardVel + turnVel*myQBot.WHEEL_BASE
                leftWheelVel = forwardVel - turnVel*myQBot.WHEEL_BASE

        led1State = 0
        led2State = 0

        # Display the two images
        cv2.imshow('My RGB', myCam.imageBufferRGB)
            
        # Write commands and update measurements
        myQBot.read_write_std(rightWheelVel, leftWheelVel, led1State, led2State)        

        # Get wheel distance from encoders. 
        rightWheelDistance = myQBot.estimate_wheel_travel(myQBot.rightEncoder)
        leftWheelDistance = myQBot.estimate_wheel_travel(myQBot.leftEncoder)

        end = elapsed_time()
        cv2.waitKey(1)
        
        prev = start

except KeyboardInterrupt:
    print("User interrupted!")

finally:    
    myQBot.terminate()
    myCam.terminate()
#endregion
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 