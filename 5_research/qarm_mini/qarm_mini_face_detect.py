#-------------------------QArm Mini Research Example--------------------------#
#------------------------Haar Face & Eye detect Demo -------------------------#

# imports
import numpy as np
import cv2
from pit.haar.core import HaarDetect
from pal.products.qarm_mini import QArmMini
from pal.utilities.timing import QTimer
from pal.utilities.vision import Camera2D

## Section A - Setup
poseData, jointData, timeData  = [], [], []
myMiniArm   = QArmMini(hardware=1, id=9)
timer       = QTimer(sampleRate=10.0, totalTime=300.0)
myCam       = Camera2D("0", frameWidth=640, frameHeight=360, frameRate=30)
myHaarDetector = HaarDetect()

try:
    # main loop
    while timer.check():

        myMiniArm.read_write_std(myMiniArm.HOME_POSE
                + np.sin(2*np.pi*0.1*timer.get_current_time())*np.array([np.pi/6, np.pi/8, -np.pi/4, np.pi/8], dtype=np.float64))
        flag = myCam.read()

        if flag:
            face = myHaarDetector.adjusted_detect_face(myCam.imageData, color=(0, 255, 0), thickness=2)
            eyes = myHaarDetector.detect_eyes(face, color=(255, 0, 0), thickness=2)
            cv2.imshow('Raw', eyes)
        cv2.waitKey(1)
        timer.sleep()

except KeyboardInterrupt:
    print('Received user terminate command.')

finally:

    # terminate devices
    myMiniArm.terminate()