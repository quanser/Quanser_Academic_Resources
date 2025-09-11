# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
#region : File Description and Imports

"""
lane_keeping.py

Skills activity code for lane keeping lab guide.
Please review the accompanying "Lab Guide - Lane Keeping" PDF
"""
from pal.utilities.keyboard import PygameKeyboardDrive,PygameKeyboard
# from pal.products.qcar import QCarRealSense,QCar
from hal.content.qcar import QCarRealSense,QCar
from hal.content.qcar_functions import LaneKeeping,SpeedController,LaneSelection
import time
import cv2
import numpy as np
from pit.LaneNet.nets import LaneNet
import os
#endregion


# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
#region : Tunable Experiment Configuration 

# ===== Timing Parameters
# - controllerUpdateRate: control update rate in Hz. 10 is sufficient for
#   lane keeping application.
controllerUpdateRate = 10

# ===== Speed Controller Parameters
# - vDesire: desired velocity in m/s
# - Kp: proportional gain for speed controller
# - Ki: integral gain for speed controller
# - Kff: feed forward gain for speed controller
vDesire=10
Kp=0.01
Ki=0.005
Kff=1/60

# ===== Bird's-Eye View (BEV) Parameters
# - bevShape: width and height of the BEV image
# - bevWorldDims: [min x, max x, min y, max y] of the world represented by the BEV image 
bevShape = [800,800]
bevWorldDims = [0,20,-10,10]

# ===== Lane Keeping Parameters
# - Kdd: gain for calculating look-ahead distance
# - ldMin: minimum look-ahead distance
# - ldMax: maximum look-ahead distance
# - maxSteer: maximum steering angle in either direction
Kdd = 0
ldMin = 10 
ldMax = 20
maxSteer = 0

# ===== Keyboard Driver Parameters
# - maxKeyThrottle: maximum PWN command from keyboard driver
# - maxKeySteer: maximum steering angle from keyboard driver
maxKeyThrottle = 0.2
maxKeySteer = 0.1
#endregion


# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
#region : Initial Setup

# - noKill: when set to False by gamepad, terminates application
# - kb: handles communication with keyboard
# - qcarCam: handles communication with qcar RealSense camera
# - qcar: handles communication with qcar motor and sensors
# - speedControl: linear speed controller
# - myLaneKeeping: overarching object contaning most lane keeping tasks
# - myLaneNet: handles lane detection using LaneNet
# - selector: facilitates the usage of gamepad to select detected lanes
# - kbdrive: converts keyboard inputs to steer and throttle command

noKill = True
kb = PygameKeyboard()
qcarCam = QCarRealSense(mode='RGB',
                        frameWidthRGB=640,
                        frameHeightRGB=480)
qcar = QCar(readMode=1, frequency=controllerUpdateRate)
speedControl = SpeedController(Kp=Kp,
                               Ki=Ki,
                               Kff=Kff)
myLaneKeeping = LaneKeeping(Kdd = Kdd,
                            ldMin = ldMin,
                            ldMax = ldMax,
                            maxSteer=maxSteer,
                            bevShape = bevShape,
                            bevWorldDims = bevWorldDims)
# myLaneNet = LaneNet(rowUpperBound=240,
#                     imageWidth=640,
#                     imageHeight=480)
selector = LaneSelection()
kbdrive = PygameKeyboardDrive(maxThrottle=maxKeyThrottle,
                              maxSteer=maxKeySteer)


#endregion


# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
#region : Main Loop

try:
    t0 = time.time()
    t=0
    while noKill:
        #Loop Timing Update
        tp = t
        t = time.time() - t0
        dt = t-tp
        
        #Request sensor signals from QCar
        qcarCam.read_RGB()
        qcar.read()
        v = qcar.motorTach*10  # motor tach output is in 1/10th scale
        img = qcarCam.imageBufferRGB
        
        # ==============  SECTION A -  Lane Marking  ====================
        laneMarking = np.zeros((480,640),dtype=np.uint8)
        # ==============       END OF SECTION A      ====================

        # Creating Bird's-Eye view of Camera Feed and Lane Markings
        bev = myLaneKeeping.ipm.create_bird_eye_view(img)
        bevLaneMarking = myLaneKeeping.ipm.create_bird_eye_view(laneMarking)

        # Process Lane Markings and Extract Availabe Lane Centers (Pure Pursuit Targets)
        processedLaneMarking = myLaneKeeping.preprocess(bevLaneMarking)
        isolated = myLaneKeeping.isolate_lane_markings(processedLaneMarking)
        targets = myLaneKeeping.find_target(isolated,v)
        
        # Receive Keyboard Signals
        kb.read()
        enableLaneKeep = kb.k_space
        if kb.k_esc:
            print("Operator: Emergency Stop")
            noKill = False

        # Annotate Camera Feed and Select Pure Pursuit Target
        for id in targets:
            point=targets[id]
            cv2.circle(bev,point.astype(int),10,(0,255,0),-1)

        # Send Driving Commands to QCar
        if enableLaneKeep: 
            throttle = speedControl.update(v, vDesire, dt)
            if len(targets)>0:
                selected = selector.select(myLaneKeeping,kb)
                steering = myLaneKeeping.pp.target2steer(selected)
                #color selected target in red
                cv2.circle(bev,selected.astype(int),10,(0,0,255),-1)
            else:
                steering = 0
        else: 
            steering, throttle = kbdrive.update(kb)
        qcar.write(throttle=throttle,steering=steering)

        # Visualization       
        cv2.imshow("camera", img)
        cv2.imshow("lane marking", laneMarking)
        # cv2.imshow("camera BEV", bev)
        # cv2.imshow("lane marking BEV",bevLaneMarking)
        # cv2.imshow("processed BEV",processedLaneMarking)
        # for i,blob in enumerate(isolated):
        #     cv2.imshow('blob'+str(i),blob)
        # myLaneKeeping.show_debug()
        cv2.waitKey(1)

except KeyboardInterrupt:
    print('User interrupted')

finally:
    qcarCam.terminate()
    qcar.terminate()
    qcar.terminate_pc_application()
    print('Simulation terminated')

#endregion

