# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
#region : File Description and Imports

"""
object_detection.py

Skills activity code for object detection lab guide.
Please review the accompanying "Lab Guide - Object Detection" PDF
"""
import numpy as np
import time
import cv2
from pit.YOLO.utils import QCar2DepthAligned
from pal.products.qcar import IS_PHYSICAL_QCAR
import math
from hal.content.qcar_functions import ObjectDetection
#endregion


# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
#region : Experiment Configuration 
# ===== Timing Parameters
# - sampleRate: Script loop rate in Hz.
sampleRate     = 30.0
sampleTime     = 1/sampleRate
simulationTime = 3000.0
print('Sample Time: ', sampleTime)

# ===== Tasks Configuration Parameters
# - task: Specify the task of the script. 'threshold' or 'detect' or 'classify'.
# - mode: Specify the mode of the task. 'hsv' or 'rgb' for 'threshold'.
#         'shape' or 'template' or 'yolo' for 'classify'.
task = 'threshold'
mode = 'rgb'

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
#region : Initial Setup

# - qcarImg: Initialize Depth/RGB alignment RT model.
# - myDetector: overarching class contaning most object detection tasks.
qcarImg = QCar2DepthAligned()
myDetector = ObjectDetection()

#endregion


# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
#region : Main Loop

try:
    
    if task == 'threshold':
        myDetector.set_tracker(mode=mode)

    elif mode == 'yolo':
    # Instantiate a YOLOv8 object to handle prediction using YOLO
        from pit.YOLO.nets import YOLOv8
        myDetector.yolo  = YOLOv8()

    while True:
        #Loop Timing Update
        start = time.time()

        #Request sensor signals from QCar
        qcarImg.read()
        img = qcarImg.rgb
        depth = qcarImg.depth

        # ==============  SECTION A - Color Thresholding  ====================
        if task == 'threshold':
            detectedMask,detectedName,detectedBbox = [],[],[]
            lower,upper = myDetector.get_tracker()
            img_mask = myDetector.color_thresholding(img,lower,upper)
            img=myDetector.mask_img(img,img_mask)
        # ==============        END OF SECTION A          ====================

        # ==============  SECTION B - Color-based Detection  ====================
        else:
            detectedMask,detectedName,detectedBbox = myDetector.obj_detect(img,task=task,mode=mode)
        # ==============          END OF SECTION B           ====================

        # ==============  SECTION C - Distance Estimation  ====================
        detectedDist = myDetector.find_distance(depth,detectedMask)
        # ==============         END OF SECTION C          ====================

        #Visualization of the detected objects
        myDetector.annotate(img,detectedName,detectedBbox,detectedDist)
        cv2.imshow('Image',img)
        
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
    qcarImg.terminate()
