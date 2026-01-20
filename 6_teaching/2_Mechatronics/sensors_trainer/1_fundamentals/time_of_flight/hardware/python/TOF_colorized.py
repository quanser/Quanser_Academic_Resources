# TOF_colorized.py
# This script reads Time-of-Flight (TOF) sensor data from a Sensors Trainer
# and displays a colorized distance matrix using OpenCV.

# region: Python level imports
import numpy as np
import cv2

from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer, SensorsDisplay
# endregion

# region: Experiment constants
simulationTime = 300 # will run for this amount of seconds
frequency = 300 # Hz

counter = 0 # counter to track scopes
counterHalfSec = 0

maxTOF = 0.6

maxSigma = 0.055
maxReflectance = 1.0
maxTargets = 3
# endregion

# region:  Main Loop
timer = Timer(sampleRate=frequency, totalTime=simulationTime)

with SensorsTrainer() as sensors, SensorsDisplay() as lcd:

    while timer.check():
        
        currentTime = timer.get_current_time()

        sensors.read_outputs()
        
        TOFSensor = sensors.TOFDistance
        NumberSquare = np.flip(sensors.TOFNumberOfTargets.reshape(8,8), axis=0)
        
        TOFSensorSquare = np.flip(TOFSensor.reshape(8,8), axis=0)
        # TOFSensor_uint8 = cv2.normalize(NumberSquare*TOFSensorSquare, None, 0, 255, cv2.NORM_MINMAX)
        TOFSensor_uint8 = np.clip(TOFSensorSquare*255/maxTOF, 0, 255).astype(np.uint8)
        
        # Apply a colormap (e.g., COLORMAP_JET)
        color_matrix = cv2.applyColorMap(TOFSensor_uint8, cv2.COLORMAP_JET)

        # TOFSensor_uint8 = np.clip(TOFSensorSquare*255/maxTOF, 0, 255).astype(np.uint8)

        ReflectanceSquare = np.flip(sensors.TOFReflectance.reshape(8,8), axis=0)
        TOFReflectance_uint8 = np.clip(ReflectanceSquare*255/maxReflectance, 0, 255).astype(np.uint8)
        TOFReflectance_uint8 = cv2.applyColorMap(TOFReflectance_uint8, cv2.COLORMAP_JET)
        
        SigmaSquare = np.flip(sensors.TOFSigma.reshape(8,8), axis=0)
        TOFSigma_uint8 = np.clip(SigmaSquare*255/maxSigma, 0, 255).astype(np.uint8)

        # print(NumberSquare)
        TOFNumber_uint8 = np.clip(NumberSquare*255/maxTargets, 0, 255).astype(np.uint8)

        if counterHalfSec == frequency/2:

            # print(sensors.TOFSigma.shape, sensors.TOFReflectance.shape, sensors.TOFNumberOfTargets.shape)
            # print(TOFSensorSquare.dtype)
            # print(sensors.TOFReflectance.max())


            counterHalfSec = 0
        
        # update scopes every 4 samples
        if counter%4 == 0:
            resizedTOFDistance = cv2.resize(color_matrix,(400,400), interpolation=cv2.INTER_NEAREST)
            resizedTOFReflectance = cv2.resize(TOFReflectance_uint8,(400,400), interpolation=cv2.INTER_NEAREST)
            resizedTOFSigma = cv2.resize(TOFSigma_uint8,(400,400), interpolation=cv2.INTER_NEAREST)
            resizedTOFNumber = cv2.resize(TOFNumber_uint8,(400,400), interpolation=cv2.INTER_NEAREST)
            
            cv2.imshow('Colorized Distance Matrix', resizedTOFDistance)

            # Uncomment below lines to visualize other matrices

            # cv2.imshow('TOF Reflectance Image', resizedTOFReflectance)
            # cv2.imshow('TOF Sigma % Image', resizedTOFSigma)
            # cv2.imshow('TOF Number Image', resizedTOFNumber)
            
            
        counter += 1
        counterHalfSec += 1
        cv2.waitKey(1)
        timer.sleep()

cv2.destroyAllWindows()
# endregion



