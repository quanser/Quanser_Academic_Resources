#-----------------------------------------------------------------------------#
#------------------Skills Progression 1 - Task Automation---------------------#
#-----------------------------------------------------------------------------#
#-------------------------Lab 4 - Obstacle Detection--------------------------#
#-----------------------------------------------------------------------------#

# Imports
from pal.products.qbot_platform import QBotPlatformDriver,\
    QBotPlatformCSICamera, QBotPlatformRealSense, QBotPlatformLidar
from hal.content.qbot_platform_functions import QBPVision, QBPRanging
from quanser.hardware import HILError
from pal.utilities.probe import Probe
from pal.utilities.gamepad import LogitechF710
import time
import numpy as np
import cv2
from pal.utilities.math import Calculus
import os

# Section A - Setup
os.system('quarc_run -q -Q -t tcpip://localhost:17000 *.rt-linux_qbot_platform -d /tmp')
time.sleep(5)
os.system('quarc_run -r -t tcpip://localhost:17000 qbot_platform_driver_physical.rt-linux_qbot_platform  -d /tmp -uri tcpip://localhost:17099')
time.sleep(3)
print('driver loaded')

ipHost, ipDriver = '192.168.3.6', 'localhost'
commands, arm, noKill = np.zeros((2), dtype = np.float64), 0, True
frameRate, sampleRate = 60.0, 1/60.0
counter, counterDown, counterLidar = 0, 0, 0
endFlag, obstacle, offset, forSpd, turnSpd = False, False, 0, 0, 0
startTime = time.time()
def elapsed_time():
    return time.time() - startTime
timeHIL, prevTimeHIL = elapsed_time(), elapsed_time() - 0.017

LIDAR_POS_X = QBotPlatformDriver.LIDAR_POS_X
LIDAR_POS_Y = QBotPlatformDriver.LIDAR_POS_Y

try:
    # Section B - Initialization
    myQBot       = QBotPlatformDriver(mode=1, ip=ipDriver)
    downCam      = QBotPlatformCSICamera(frameRate=frameRate, exposure = 39.0, gain=17.0)
    lidar        = QBotPlatformLidar()
    gpad         = LogitechF710(1)
    vision       = QBPVision()
    ranging      = QBPRanging()
    probe        = Probe(ip = ipHost)
    # probe.add_display(imageSize = [200, 320, 1], scaling = True, scalingFactor= 2, name='Raw Image')
    probe.add_plot(numMeasurements=1680, scaling=True, scalingFactor=4, name='Raw Lidar')
    probe.add_plot(numMeasurements=410, scaling=False, name='Plotting Lidar')
    line2SpdMap = vision.line_to_speed_map(sampleRate=sampleRate, saturation=75)
    next(line2SpdMap)
    startTime = time.time()
    time.sleep(0.5)

    # Main loop
    while noKill and not endFlag:
        t = elapsed_time()

        if not probe.connected:
            probe.check_connection()

        if probe.connected:

            # Joystick Driver
            newGPad = gpad.read()
            arm = gpad.buttonLeft and not obstacle
            lineFollow = gpad.buttonA
            if obstacle:
                arm = 0
            turnStick = gpad.leftJoystickX
            driveStick = gpad.rightJoystickY
            if gpad.buttonRight:
                noKill = False

            # Section C - toggle line following
            if not lineFollow:
                forSpd=0.7*driveStick/2
                turnSpd=3.564*turnStick/2
                commands = np.array([forSpd, turnSpd], dtype = np.float64) # robot spd command
            else:
                commands = np.array([forSpd, turnSpd], dtype = np.float64) # robot spd command

            # QBot Hardware
            newHIL = myQBot.read_write_std(timestamp = time.time() - startTime,
                                            arm = arm,
                                            commands = commands, userLED=obstacle)
            if newHIL:
                timeHIL     = elapsed_time()
                newDownCam  = downCam.read()
                newLidar    = lidar.read()

                if newDownCam:
                    counterDown += 1

                    # Section D - Image processing 

                    # Section D.1 - Undistort and resize the image
                    undistorted = vision.df_camera_undistort(downCam.imageData)
                    gray_sm = cv2.resize(undistorted, (320, 200))

                    #-------Replace the following line with your code---------#
                    # Subselect a part of the image and perform thresholding
                    binary = None

                    # Blob Detection via Connected Component Labeling
                    col, row, area = 0, 0, 0

                    # Section D.2 - Speed command from blob information
                    forSpd, turnSpd = line2SpdMap.send((col, 1, 0))
                    #---------------------------------------------------------#
                
                if newLidar:
                    counterLidar += 1

                    # Section E - LiDAR processing 
                    #-------Replace the following line with your code---------#
                    rangesC, anglesC = None,None
                    #---------------------------------------------------------#

                    # Section F - Obstacles detection
                    #-------Replace the following line with your code---------#
                    minThreshold=0.2858
                    rangesP, anglesP, obstacle = None,None,0
                    #---------------------------------------------------------#

                # if counterDown%4 == 0:
                #     sending = probe.send(name='Raw Image', imageData=gray_sm)
                if counterLidar%2 == 0:
                    sending = probe.send(name='Raw Lidar', lidarData=(lidar.distances, np.pi/2 - lidar.angles))
                if counterLidar%2 == 1:
                    sending = probe.send(name='Plotting Lidar', lidarData=(rangesP, anglesP))

                prevTimeHIL = timeHIL

except KeyboardInterrupt:
    print('User interrupted.')
except HILError as h:
    print(h.get_error_message())
finally:
    lidar.terminate()
    downCam.terminate()
    myQBot.terminate()
    probe.terminate()
    os.system('quarc_run -q -Q -t tcpip://localhost:17000 *.rt-linux_qbot_platform -d /tmp')