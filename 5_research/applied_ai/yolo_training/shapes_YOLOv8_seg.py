'''
shapes_YOLOv8_seg.py -- Live segmentation inference demo using a trained YOLOv8 model
Reads frames from a camera in a timed loop, runs YOLOv8 segmentation inference on each
frame, prints detected objects and post-processed shape results to the console, and
displays the annotated feed in a window.

HOW TO USE
----------
1. Set the model path in the Model and Camera Initialization section to point to
   your trained .pt file or .engine file.
2. Set the camera index in cv2.VideoCapture() to match your device.
3. Adjust simulationTime (seconds) and sampleRate (Hz) in the Timing section as needed.
4. Update the classes list in myYolo.predict() to match your dataset class IDs.
5. Run:  python shapes_YOLOv8_seg.py
'''

# region Imports
import time
import cv2
from pit.YOLO.nets import YOLOv8
import os
import torch
# endregion Imports

# region Timing
def elapsed_time():
    return time.time() - startTime

sampleRate     = 30.0
sampleTime     = 1 / sampleRate
simulationTime = 200
print('Sample Time: ', sampleTime)
# endregion Timing

# region Configuration
imageWidth  = 640
imageHeight = 480

_PATH = os.path.dirname(os.path.abspath(__file__))
# endregion Configuration

# region Model and Camera Initialization
myYolo = YOLOv8(
    modelPath   = os.path.join(_PATH, 'segmentTraining/yolov8s-shapes-seg.pt'),
    imageHeight = imageHeight,
    imageWidth  = imageWidth,
)

# uncomment this line if you to run on GPU (make sure you have a compatible NVIDIA GPU and PyTorch with CUDA support installed)
# myYolo.net.to('cuda:0') 

cap = cv2.VideoCapture(4)  # Change this index to match your camera device
# endregion Model and Camera Initialization

# region Main Loop
try:
    startTime = time.time()
    while elapsed_time() < simulationTime:
        start = time.time()
        ret, frame = cap.read()

        rgbProcessed = myYolo.pre_process(frame)
        prediction   = myYolo.predict(
            inputImg   = rgbProcessed,
            classes    = [0, 1],
            confidence = 0.75,
            half       = True,
            verbose    = False
        )

        if len(myYolo.objectsDetected) > 0:
            # print('Prediction: ', myYolo.objectsDetected)

            processedResults = myYolo.post_processing_shapes()

            print('Processed Results: ')
            print(processedResults)
            print('---------------------------')

        annotatedImg = myYolo.render(showFPS=True)
        cv2.imshow('Object Segmentation', annotatedImg)

        # Compute sleep duration to hold the desired sample rate
        end             = time.time()
        computationTime = end - start
        sleepTime       = sampleTime - (computationTime % sampleTime)

        msSleepTime = int(1000 * sleepTime)
        if msSleepTime <= 0:
            msSleepTime = 1
        cv2.waitKey(msSleepTime)

except KeyboardInterrupt:
    print("User interrupted!")

finally:
    cap.release()
    cv2.destroyAllWindows()
# endregion Main Loop
