#-----------------------------------------------------------------------------#
#--------------------Skills Progression 2 - Surveying ------------------------#
#-----------------------------------------------------------------------------#
#------------------------ Lab 2 - Sensor Fusion ------------------------------#
#-----------------------------------------------------------------------------#

# This lab covers state estimation using different sensors on the QBot 
# platform, tradeoffs between individual sensor estimates, and sensor fusion 
# techniques

# region: Python level imports
from pal.products.qbot_platform import QBotPlatformDriver,Keyboard,\
                                            QBotPlatformLidar
from hal.content.qbot_platform_functions import QBPRanging, QBPMovement, \
                                                QBPLocalization,QBPFusion, \
                                                QBotEKF
from quanser.hardware import HILError
from pal.utilities.probe import Probe
import time
import numpy as np
import subprocess
import sys 
import os
from pal.utilities.math import Calculus
from qlabs_setup import setup
# endregion

# region: Experiment constants
# Section A - Setup
setup(locationQBotP=[0.0, 0.0, 0.0], rotationQBotP=[0, 0, 0], verbose=True)
time.sleep(2)
ipHost, ipDriver = 'localhost', 'localhost'
commands, arm, noKill, endFlag = np.zeros((2), dtype = np.float64), 0, True, False
frameRate, sampleTime = 60.0, 1/60.0
counterLidar = 0
turnSpdCmd, turnSpdCmd = 0, 0
fwdAccel, fwdSpdAccel, fwdSpdOdom, fwdSpdFused = 0, 0, 0, 0
gyroRate, turnSpdGyro, turnSpdOdom, turnSpdFused = 0, 0, 0, 0
poseRateIntegrated, poseFused, poseEKF = np.array([0,0,0]),np.array([0,0,0]), np.array([0,0,0])
# endregion
startTime = time.time()
def elapsed_time():
    return time.time() - startTime
timeHIL, prevTimeHIL = elapsed_time(), elapsed_time() - 0.017

time.sleep(2.0) # wait for all processes to initialize

def init_generator(gen):
    # function for initializing generator and calling next
    next(gen)
    return gen

try:
    # Section B - Initialization
    myQBot = QBotPlatformDriver(mode=1, ip=ipDriver)
    lidar = QBotPlatformLidar()
    keyboard = Keyboard()
    ranging = QBPRanging()
    movement = QBPMovement()
    localization = QBPLocalization(resolution=10)
    fusion = QBPFusion()
    probe = Probe(ip = ipHost)

    # Initialize QBotEKF for pose estimation using LiDAR scan matching
    # Initial pose is [x=0, y=0, theta=0]
    ekf = QBotEKF(
        x_0=np.array([0.0, 0.0, 0.0]),
        omega_threshold=0.02,
        Q_ekf=0.0075 * np.eye(3),
        R_ekf=0.001 * np.eye(3)
    )

    # region: Scope setup
    probe.add_xy_scope(numSignals=5, name='Estimated Pose XY')
    for scopeName in ['Acceleration', 
                        'Forward Speed Estimate', 
                        'Turn Speed Estimate']:
        probe.add_scope(numSignals=3, name=scopeName)
    for scopeName in ['X Position Estimates',
                        'Y Position Estimates',
                        'Theta Estimates']:
        probe.add_scope(numSignals=4, name=scopeName)

    subprocess.Popen(
        [sys.executable, 
        os.path.join(os.path.dirname(__file__), 'observer.py')],
        cwd=os.path.dirname(__file__))
    # endregion

    refCollected = False

    # Initialize generators to estimate forward speed
    accelIntegrator = init_generator(Calculus().integrator(sampleTime))
    fwdSpeedComplementaryFilter = init_generator(fusion.complementary_filter(sampleTime))

    # Initialize generators to estimate turn speed
    gyroDifferentiator = init_generator(Calculus().differentiator(sampleTime))
    gyroRateIntegrator = init_generator(Calculus().integrator(sampleTime))
    turnSpdComplementaryFilter = init_generator(fusion.complementary_filter(sampleTime))

    # Initialize generators to estimate position
    poseRateIntegrator = init_generator(Calculus().integrator(sampleTime))
    poseComplementaryFilter = init_generator(fusion.complementary_filter(sampleTime))

    startTime = time.time()
    time.sleep(0.5)

    # region: Main loop
    while noKill and not endFlag:
        t = elapsed_time()

        if not probe.connected:
            probe.check_connection()

        if probe.connected:

            # Keyboard Driver
            newkeyboard = keyboard.read()
            if newkeyboard:
                arm = keyboard.k_space
                moveCircle = keyboard.k_7
                keyboardCmd = keyboard.bodyCmd
                if keyboard.k_u:
                    noKill = False

            # Get robot speed command from keyboard
            if not moveCircle:
                forSpdCmd, turnSpdCmd = keyboardCmd[0], keyboardCmd[1]
            else:
                forSpdCmd, turnSpdCmd = 0.25, 0.45
            commands = np.array([forSpdCmd, turnSpdCmd], 
                                    dtype = np.float64) # robot spd command

            # Write commands to QBot Hardware
            newHIL = myQBot.read_write_std(timestamp = time.time() - startTime,
                                            arm = arm,
                                            commands = commands, 
                                            userLED=False)
            if newHIL:
                timeHIL     = elapsed_time()
                newLidar    = lidar.read()
                accelerometer = myQBot.accelerometer
                gyro = myQBot.gyroscope

                fwdSpdOdom, turnSpdOdom = movement.diff_drive_forward_velocity_kinematics(myQBot.wheelSpeeds[0], 
                                                                                          myQBot.wheelSpeeds[1])

                # Section C - State Estimation

                # Estimate forward speed
                fwdAccel = 0
                fwdSpdAccel = accelIntegrator.send(fwdAccel)

                #The fused estimate is calculated using the values ((rate, correction, Kp, Ki))
                fwdSpdFused = fwdSpeedComplementaryFilter.send((fwdAccel, fwdSpdOdom, 0.5, 0.0))

                # Estimate turn speed
                gyroRate = gyroDifferentiator.send(gyro[2]) # rate of z gyro
                turnSpdGyro = gyroRateIntegrator.send(gyroRate)
                turnSpdFused = turnSpdComplementaryFilter.send((gyroRate, turnSpdOdom, 0.0, 0.0))

                # Calculate speeds in X and Y directions
                theta = poseFused[2]
                xSpeed, ySpeed = fwdSpdFused*np.cos(theta), fwdSpdFused*np.sin(theta)

                # Estimate pose
                poseRateIntegrated = poseRateIntegrator.send(np.array([xSpeed,ySpeed,turnSpdFused]))
                poseFused = poseComplementaryFilter.send((np.array([xSpeed,ySpeed,turnSpdFused]), 
                                                           localization.pose, 
                                                           np.array([0.0, 0.0, 0.0]), 
                                                           np.array([0.0, 0.0, 0.0])))

                # Update EKF with prediction step using odometry
                # Control input: [linear velocity, angular velocity] from fused sensors
                ekf_control_input = np.array([fwdSpdFused, turnSpdFused])
                dt = timeHIL - prevTimeHIL

                # Prediction step: propagate state using kinematic motion model
                ekf.update(u=ekf_control_input, dt=dt, lidar_pose=None)

                if newLidar:
                    counterLidar += 1

                    # Section D - LiDAR processing

                    rangesAdj, anglesAdj = ranging.adjust_and_subsample(lidar.distances, lidar.angles, 1680, 4)
                    rangesC, anglesC = None, None

                    # Section E - LiDAR Localization

                    #-------Replace the following lines with your code---------#

                    # Save reference LiDAR scan
                    # if (conditions for saving current scan):
                    #    refCollected = None
                    # ---------------------------------------------------------#

                    if refCollected and counterLidar%2==0:

                        # modify the following line to perform scan match on current LiDAR scan
                        matched = localization.scan_match(None, None, transRange=(0.0, 0.0), rotRange = 2*np.pi)

                        # Correction step with LiDAR scan-matched pose
                        ekf_lidar_pose = np.array(localization.pose)
                        ekf.update(u=None, dt=None, lidar_pose=ekf_lidar_pose)
                        # poseEKF = ekf.x_hat[:, 0]

                        # Section F - Data display

                        # send data to scopes
                        sending = probe.send(name = 'Scan Match Estimates', 
                                             scopeData=(elapsed_time(), localization.pose))
                        sending = probe.send(name = 'Estimated Pose XY', 
                                             xyData= (elapsed_time(), [[poseRateIntegrated[0], poseRateIntegrated[1]],
                                                                       [localization.pose[0], localization.pose[1]],
                                                                       [poseFused[0], poseFused[1]], 
                                                                       [poseEKF[0], poseEKF[1]],
                                                                       [localization.refX, localization.refY]]))

                # send measurements and estimates to scopes
                probe_data = {
                    'Acceleration': accelerometer,
                    'Forward Speed Estimate': [fwdSpdAccel, 0, 0],
                    'Turn Speed Estimate': [turnSpdGyro, turnSpdOdom, turnSpdFused],
                    'X Position Estimates': [poseRateIntegrated[0], localization.pose[0], poseFused[0], poseEKF[0]],
                    'Y Position Estimates':[poseRateIntegrated[1], localization.pose[1], poseFused[1], poseEKF[1]],
                    'Theta Estimates': [poseRateIntegrated[2], localization.pose[2], poseFused[2], poseEKF[2]],
                }

                for name, data in probe_data.items():
                    probe.send(name=name, scopeData=(elapsed_time(), data))

                prevTimeHIL = timeHIL
    #endregion

except KeyboardInterrupt:
    print('User interrupted.')
except HILError as h:
    print(h.get_error_message())
finally:
    localization.terminate()
    lidar.terminate()
    myQBot.terminate()
    keyboard.terminate()
    probe.terminate()