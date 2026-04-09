#-----------------------------------------------------------------------------#
#------------------Skills Progression 2 - Surveying --------------------------#
#-----------------------------------------------------------------------------#
#-------------------------Lab 1 - Localization -------------------------------#
#-----------------------------------------------------------------------------#

# Imports
from pal.products.qbot_platform import QBotPlatformDriver, QBotPlatformLidar
from hal.content.qbot_platform_functions import QBPRanging, QBPLocalization
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

ipHost, ipDriver = '192.168.5.6', 'localhost'
commands, arm, noKill = np.zeros((2), dtype = np.float64), 0, True
frameRate, sampleRate = 60.0, 1/60.0
counterLidar = 0
endFlag, offset, forSpd, turnSpd = False, 0, 0, 0
startTime = time.time()
def elapsed_time():
    return time.time() - startTime
timeHIL, prevTimeHIL = elapsed_time(), elapsed_time() - 0.017

try:
    # Section B - Initialization
    myQBot       = QBotPlatformDriver(mode=1, ip=ipDriver)
    lidar        = QBotPlatformLidar()
    gpad         = LogitechF710(1)
    ranging      = QBPRanging()
    localization = QBPLocalization()
    probe        = Probe(ip = ipHost)

    probe.add_scope(numSignals=3, name = 'Estimated Pose vs Time')
    probe.add_xy_scope(numSignals=2, name='Estimated Pose XY')
    probe.add_scope(numSignals=1, name='Score')
    probe.add_scope(numSignals=1, name='Loop Execution Time')

    refCollected = False

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
            arm = gpad.buttonLeft 
            turnStick = gpad.leftJoystickX
            driveStick = gpad.rightJoystickY
            if gpad.buttonRight:
                noKill = False

            # Get robot speed command from joystick
            forSpd=0.7*driveStick/2
            turnSpd=3.564*turnStick/2
            commands = np.array([forSpd, turnSpd], 
                                dtype = np.float64) # robot spd command

            # QBot Hardware
            newHIL = myQBot.read_write_std(timestamp = time.time() - startTime,
                                            arm = arm,
                                            commands = commands, userLED=False)
            if newHIL:
                timeHIL     = elapsed_time()
                newLidar    = lidar.read()

                if newLidar:
                    counterLidar += 1
                    
                    # Section C - LiDAR processing 

                    rangesAdj, anglesAdj = ranging.adjust_and_subsample(lidar.distances, lidar.angles)
                    # -------Replace the following line with your code--------#
                    rangesC, anglesC = None, None
                    #---------------------------------------------------------#
                   
                    # Section D - LiDAR Localization                    
                    
                    #-------Replace the following lines with your code---------#

                    # Save reference LiDAR scan
                    # if (conditions for saving current scan):
                    #    refCollected = None
                    
                    #---------------------------------------------------------#
                    
                    if refCollected and counterLidar%2==0:

                        # modify the following line to perform scan match on current LiDAR scan:
                        # matched = localization.scan_match(None, None, transRange=(0.0, 0.0), rotRange = 2*np.pi)

                        # send data to scopes
                        sending = probe.send(name = 'Estimated Pose vs Time', 
                                             scopeData=(elapsed_time(), localization.pose))
                        sending = probe.send(name = 'Estimated Pose XY', 
                                             xyData= (elapsed_time(), [[localization.refX, localization.refY],
                                                                       [localization.pose[0], localization.pose[1]]]))
                        sending = probe.send(name = 'Score', 
                                             scopeData=(elapsed_time(), localization.score))

                
                sending = probe.send(name='Loop Execution Time', scopeData=(elapsed_time(), np.array([timeHIL-prevTimeHIL])))
                prevTimeHIL = timeHIL

except KeyboardInterrupt:
    print('User interrupted.')
except HILError as h:
    print(h.get_error_message())
finally:
    lidar.terminate()
    myQBot.terminate()
    probe.terminate()
    os.system('quarc_run -q -Q -t tcpip://localhost:17000 *.rt-linux_qbot_platform -d /tmp')
