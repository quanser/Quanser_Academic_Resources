import numpy as np
import time
import cv2
from pit.YOLO.nets import YOLOv8
from pit.YOLO.utils import QCar2DepthAligned

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
# Initialize YOLOv8 segmentation model
myYolo  = YOLOv8(
                 # modelPath = 'path/to/model', 
                 imageHeight= imageHeight,
                 imageWidth = imageWidth,
                )

# Initialize Depth/RGB alignment RT model
QCarImg = QCar2DepthAligned()

try:
    startTime = time.time()
    while elapsed_time()<simulationTime:
        start = time.time()

        # Get aligned RGB and Depth images
        QCarImg.read()
            
        rgbProcessed = myYolo.pre_process(QCarImg.rgb)
        predecion = myYolo.predict(inputImg = rgbProcessed,
                                   classes = [2,9,11],
                                   confidence = 0.3,
                                   half = True,
                                   verbose = False
                                   )
        
        processedResults=myYolo.post_processing(alignedDepth = QCarImg.depth,
                                                clippingDistance = 5)
        for object in processedResults:
            print(object.__dict__)
        print('---------------------------')

        # annotatedImg=myYolo.render(showFPS = True)
        annotatedImg=myYolo.post_process_render(showFPS = True)
        cv2.imshow('Object Segmentation', annotatedImg)

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
    QCarImg.terminate()

