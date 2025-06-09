import numpy as np
import cv2
import time
from pit.LaneNet.nets import LaneNet
from pal.utilities.vision import Camera3D


## Timing Parameters and methods 
def elapsed_time():
    return time.time() - startTime

sampleRate     = 30.0
sampleTime     = 1/sampleRate
simulationTime = 30.0
print('Sample Time: ', sampleTime)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
# Additional parameters
imageWidth  = 640
imageHeight = 480

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
# Initialize the LaneNet model
myLaneNet = LaneNet(
                    # modelPath = 'path/to/model', 
                    imageHeight = imageHeight,
                    imageWidth = imageWidth,
                    rowUpperBound = 240
                    )

# Initialize the RealSense camera for RGB 
myCamRGB  = Camera3D(mode='RGB', frameWidthRGB=imageWidth, frameHeightRGB=imageHeight)

try:
    startTime = time.time()
    while elapsed_time()<simulationTime:
        start = time.time()
        # Read the RGB
        myCamRGB.read_RGB()

        rgbProcessed=myLaneNet.pre_process(myCamRGB.imageBufferRGB)
        binaryPred , instancePred = myLaneNet.predict(rgbProcessed)
        isolatedLane = myLaneNet.post_process(eps=0.5,
                                              min_samples=250,
                                              min_area=100)

        # annotatedImg = myLaneNet.render(showFPS = True)
        annotatedImg = myLaneNet.post_process_render(showFPS = True)

        cv2.imshow('Extracted Lane Markings', annotatedImg)

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

except KeyboardInterrupt:
    print("User interrupted!")

finally:
    myCamRGB.terminate()


