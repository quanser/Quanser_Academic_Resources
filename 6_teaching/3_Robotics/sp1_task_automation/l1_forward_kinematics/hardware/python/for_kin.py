#-----------------------------------------------------------------------------#
#------------------Skills Progression 1 - Task Automation---------------------#
#-----------------------------------------------------------------------------#
#--------------------------Lab 1 - Forward Kinematics-------------------------#
#-----------------------------------------------------------------------------#

# Imports
from pal.products.qbot_platform import QBotPlatformDriver,\
    QBotPlatformCSICamera
from hal.content.qbot_platform_functions import QBPVision, QBPMovement
from quanser.hardware import HILError
from pal.utilities.probe import Probe
from pal.utilities.gamepad import LogitechF710
import time
import numpy as np
import cv2
import os

# Section A - Setup
os.system('quarc_run -q -Q -t tcpip://localhost:17000 *.rt-linux_qbot_platform -d /tmp')
time.sleep(5)
os.system('quarc_run -r -t tcpip://localhost:17000 qbot_platform_driver_physical.rt-linux_qbot_platform  -d /tmp -uri tcpip://localhost:17099')
time.sleep(3)
print('driver loaded')
ipHost, ipDriver = '192.168.3.10', 'localhost'
commands, arm, noKill = np.zeros((2), dtype = np.float64), 0, True
frameRate, sampleRate = 60.0, 1/60.0
counter, counterDown = 0, 0
endFlag, offset, forSpd, turnSpd = False, 0, 0, 0
simulationTime, startTime = 60.0, time.time()
def elapsed_time():
    return time.time() - startTime
timeHIL, prevTimeHIL = elapsed_time(), elapsed_time() - 0.017

try:
    # Section B - Initialization
    myQBot       = QBotPlatformDriver(mode=0, ip=ipDriver)
    downCam      = QBotPlatformCSICamera(frameRate=frameRate, exposure = 39.0, gain=17.0)
    gpad         = LogitechF710(1)
    vision       = QBPVision()
    movement     = QBPMovement()

    # Section C - Initialization to send data to main computer
    probe        = Probe(ip = ipHost)
    probe.add_display(imageSize = [200, 320, 1], scaling = True, scalingFactor= 2, name='Raw Image')
    probe.add_scope(numSignals = 4, name='Motor Speed')
    probe.add_scope(numSignals = 3, name='Body Speed')

    startTime = time.time()
    time.sleep(0.5)

    # Main loop
    while noKill and not endFlag:
        t = elapsed_time()
        endFlag = t > simulationTime
        if endFlag:
            print('Application terminated successfully.')

        if not probe.connected:
            probe.check_connection()

        if probe.connected:

            # Section D - Joystick to commands
            # Joystick Driver
            newGPad = gpad.read()
            arm = gpad.buttonLeft
            leftStick = gpad.leftJoystickY
            rightStick = gpad.rightJoystickY
            commands = np.array([15.75*leftStick/2, 15.75*rightStick/2], dtype = np.float64)
            if gpad.buttonRight:
                print('Operator: Emergency Stop')
                noKill = False

            # Section E - Send and Receive Data
            # QBot Hardware
            newHIL = myQBot.read_write_std(timestamp = time.time() - startTime,
                                            arm = arm,
                                            commands = commands)
            if newHIL:
                timeHIL = elapsed_time()

                # Section F - Kinematic calculations

                #-----------Replace the next line with your code--------------#
                forSpd, turnSpd = 0, 0
                #-------------------------------------------------------------#

                motor_speeds=(timeHIL,np.array([commands[0], commands[1], myQBot.wheelSpeeds[0], myQBot.wheelSpeeds[1]]))
                body_speeds=(timeHIL,np.array([forSpd,turnSpd,myQBot.gyroscope[2]]))

                newDownCam = downCam.read()
                if newDownCam:
                    counterDown += 1
                    undistorted = vision.df_camera_undistort(downCam.imageData)
                    gray_sm = cv2.resize(undistorted, (320, 200))

                # Section G - Sending data to Observer in main computer
                if counterDown%4 == 0:
                    sending = probe.send(name='Raw Image', imageData=gray_sm)

                if counterDown%4 == 1:
                    sending = probe.send(name='Motor Speed', scopeData=motor_speeds)

                if counterDown%4 == 3:
                    sending = probe.send(name='Body Speed', scopeData=body_speeds)

                prevTimeHIL = timeHIL

except KeyboardInterrupt:
    print('User interrupted.')
except HILError as h:
    print(h.get_error_message())
finally:
    # Termination
    downCam.terminate()
    myQBot.terminate()
    probe.terminate()
    os.system('quarc_run -q -Q -t tcpip://localhost:17000 *.rt-linux_qbot_platform -d /tmp')