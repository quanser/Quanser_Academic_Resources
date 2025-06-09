# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
#region: Script Description and Imports


"""
Overview
********

This script is built to help you get started with using the QBot Platform 
cameras, lidar and sensors in Python.

To get started with running this file, open the io_instructions.md file.

"""

from pal.products.qbot_platform import QBotPlatformDriver, QBotPlatformLidar, \
    QBotPlatformCSICamera, QBotPlatformRealSense
from quanser.hardware import HILError
import time
import cv2
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use('dark_background')
from threading import Thread
import signal

#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
#region: Experiment Configurations
#======================= Experiment Configurations ============================
runTime = 20 #seconds

# Hardware I/O parameters
ipAddress = '192.168.2.3' # NOTE:Change this to your QBot Platform's IP

forwardVelocity = 0 # 0.35
turningVelocity = 1.0 #1.773
# mode 1 is education body mode.
# mode 0 is education wheel speeds mode.
# 2 & 3 are wheel and body modes respectively meant for research.
mode = 1
motorEnable = 1
hold = 0
commands = np.array([forwardVelocity, turningVelocity], dtype=np.float64)

startDelay = 1 #seconds
UpdateRate = 100

# Empty lists for plotting
plotTime = []
wheelPosition0 = []
wheelPosition1 = []
motorCmd0 = []
motorCmd1 = []
accel0 = []
accel1 = []
accel2 = []
gyro0 = []
gyro1 = []
gyro2 = []
current0 = []
current1 = []
battVoltage = []
wheelSpeed0 = []
wheelSpeed1 = []

# Camera parameters
frameRate = 30 #fps
sampleRate = 1/frameRate

x = np.zeros((1680), dtype=np.int16)
y = np.zeros((1680), dtype=np.int16)

#RealSense Camera
imageSizeRS = [640,480]
scalePercent = 25 # percent of original size
widthRS = int(imageSizeRS[0] * scalePercent / 100)
heightRS = int(imageSizeRS[1] * scalePercent / 100)
dimRS = (widthRS, heightRS)

#Downward Facing Camera
imageSizeDF = [640,400]
widthDF = int(imageSizeDF[0] * scalePercent / 100)
heightDF = int(imageSizeDF[1] * scalePercent / 100)
dimDF = (widthDF, heightDF)

# Lidar parameters
frameHeight = 300
frameWidth = 300
pixelsPerMeter = 45
offsetY = 150
offsetX = 150
imageLidar = np.zeros((frameHeight, frameWidth), dtype=np.uint8)

# Thread Handling
global KILL_THREAD
KILL_THREAD = False
def sig_handler(*args):
    global KILL_THREAD
    KILL_THREAD = True
signal.signal(signal.SIGINT, sig_handler)

#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
#region: Hardware IO Loop
def hardware_io_loop():
    countMax = UpdateRate / 10
    count = 0
    # Initializing the QBot Platform Driver - Make sure that the driver is 
    # already running and that your pc is on the same network as the QBot.
    # with QBotPlatformDriver(mode=1, ip=ip_address) as myQBot:
    myQBot = QBotPlatformDriver(mode=mode, ip=ipAddress)
    print('Forward velocity: %2.2f and turn speed %2.2f' % (commands[0], \
                                                            commands[1]))
    try:
        t0 = time.time()
        t = 0
        while (t < runTime+startDelay) and (not KILL_THREAD):

            t = time.time() - t0
            new_Q = myQBot.read_write_std(timestamp=t,
                                        # this will send the wheel or body 
                                        # commands.
                                        commands=commands,
                                        # Arm will enable the motors.
                                        arm = motorEnable, 
                                        # This will allow us to override the
                                        # current LED colors while the program
                                        # is running.
                                        userLED= False,
                                        color=[0, 1, 1],
                                        # Hold will keep the current position 
                                        # the robot is in if set to 1.
                                        hold = hold 
                                        )
            if new_Q:
                count += 1
                if count%countMax == 0 and t > 1:

                    plotTime.append(t-startDelay)
                    wheelPosition0.append(myQBot.wheelPositions[0])
                    wheelPosition1.append(myQBot.wheelPositions[1])
                    wheelSpeed0.append(myQBot.wheelSpeeds[0])
                    wheelSpeed1.append(myQBot.wheelSpeeds[1])
                    motorCmd0.append(myQBot.motorCmd[0])
                    motorCmd1.append(myQBot.motorCmd[1])
                    accel0.append(myQBot.accelerometer[0])
                    accel1.append(myQBot.accelerometer[1])
                    accel2.append(myQBot.accelerometer[2])
                    gyro0.append(myQBot.gyroscope[0])
                    gyro1.append(myQBot.gyroscope[1])
                    gyro2.append(myQBot.gyroscope[2])
                    current0.append(myQBot.currents[0])
                    current1.append(myQBot.currents[1])
                    battVoltage.append(myQBot.battVoltage)
        
    finally:
        myQBot.terminate()
#endregion
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
#region: Cameras and Lidar
def cameras_lidar_loop():
    try:
        # Initializing the Cameras
        camera_realsense = QBotPlatformRealSense(
            mode= "RGB",
            frameWidthRGB  = imageSizeRS[0],
            frameHeightRGB = imageSizeRS[1],
            frameRateRGB   = frameRate
            )

        camera_df = QBotPlatformCSICamera(
            frameWidth = imageSizeDF[0],
            frameHeight = imageSizeDF[1],
            frameRate = frameRate
        )

        # Initializing the Lidar
        myLidar = QBotPlatformLidar(
            numMeasurements=1680
        )

        # decay factor to erase older data at a slower rate, creating better 
        # accuracy in results shown
        decay = 0.1
        counter = 0

        # Starting the time
        startTime = time.time()


        while (time.time() - startTime < runTime) and (not KILL_THREAD):
            
            # continue decaying the LiDar image at 30Hz, even if the new 
            # measurements are at 10Hz.
            image_lidar = decay * image_lidar

            # new measurement for lidar at 10Hz (every 3rd sample)
            if counter%3 == 0:
                myLidar.read()
                # Converting points from polar to cartesian
                x = np.uint16(np.clip(offsetX + pixelsPerMeter * 
                                      myLidar.distances * 
                                      np.cos(myLidar.angles), 0, 
                                      frameHeight-1))
                y = np.uint16(np.clip(offsetY + pixelsPerMeter * 
                                      myLidar.distances * 
                                      np.sin(myLidar.angles), 0,  
                                      frameWidth-1))
                # This sets the points on an image to appear brighter the more 
                # times the lidar sees an obstacle at the same point
                image_lidar[x, y] += 127

            # Read & display camera data
            camera_realsense.read_RGB()
            camera_df.read()
            image_rgb = camera_realsense.imageBufferRGB
            image = camera_df.imageData

            cv2.imshow("RGB Camera", cv2.resize(image_rgb, 
                                                dimRS, 
                                                interpolation = cv2.INTER_AREA))
            cv2.imshow("Bottom Camera", cv2.resize(image, 
                                                dimDF, 
                                                interpolation = cv2.INTER_AREA))
            cv2.imshow("Lidar", image_lidar)

            endTime = time.time()

            # Sleep until the next time the program needs to read from the 
            # cameras 
            computationTime = endTime-startTime
            sleepTime = sampleRate - (computationTime % sampleRate)
            msSleepTime = int(1000 * sleepTime)
            if  msSleepTime <= 0:
                msSleepTime = 1
            cv2.waitKey(msSleepTime)
            counter = counter + 1

    except HILError as h:
        print(h.get_error_message())
    finally:
        camera_realsense.terminate()
        print("Closed RealSense Camera")
        camera_df.terminate()
        print("Closed Downward Facing Camera")
        myLidar.terminate()
        print("Closed Lidar")
        cv2.destroyAllWindows()
#endregion
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
#region: main
if __name__ == '__main__':

    # Starting multiple threads to have the basic I/O function running while 
    # the cameras and lidar are running.
    hardwareThread = Thread(target= hardware_io_loop)
    cameraLidarThread = Thread(target = cameras_lidar_loop)
    hardwareThread.start()
    cameraLidarThread.start()
    try:
        # This program will run until either the Threads are stopped or the
        # loops finish
        while hardwareThread.is_alive() or cameraLidarThread.is_alive() and \
            (not KILL_THREAD):
            pass
        # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
        #region: Plotting sensor data
        print(" To end the program close the graphs window when it appears")
        fig, axs = plt.subplots(2,3, figsize=(8, 4))
        fig.suptitle(' QBot Platform Sensor Data Overview ', fontsize=14)

        axs[0,0].plot(plotTime, wheelPosition0 , 'r', 
                      plotTime, wheelPosition1, 'w' )
        axs[0,0].set_title("Wheel Positions", fontsize = 10)
        axs[0,0].set_xlabel('Time [s]', fontsize = 8)
        axs[0,0].set_ylabel('Wheel Positions \n [rads]', fontsize = 8)
        axs[0,0].tick_params(axis='both', labelsize=6)

        axs[0,1].plot(plotTime, wheelSpeed0 , 'r', 
                      plotTime, wheelSpeed1, 'w', 
                      plotTime, motorCmd0, 'r--', 
                      plotTime, motorCmd1, 'w--' )
        axs[0,1].set_title("Wheel Speeds", fontsize = 10)
        axs[0,1].set_xlabel('Time [s]', fontsize = 8)
        axs[0,1].set_ylabel('Wheel Speeds [rads/s] & \n Motor Commanded [V]', 
                            fontsize = 8)
        axs[0,1].tick_params(axis='both', labelsize=6)

        axs[0,2].plot(plotTime, accel0 , 'r', 
                      plotTime, accel1, 'w', 
                      plotTime, accel2, '0.7')
        axs[0,2].set_title("Acceleration", fontsize = 10)
        axs[0,2].set_xlabel('Time [s]', fontsize = 8)
        axs[0,2].set_ylabel('Acceleration \n [m/s**2]', fontsize = 8)
        axs[0,2].tick_params(axis='both', labelsize=6)

        axs[1,0].plot(plotTime, gyro0 , 'r', 
                      plotTime, gyro1, 'w', 
                      plotTime, gyro2, '0.7')
        axs[1,0].set_title("Angular Acceleration ", fontsize = 10)
        axs[1,0].set_xlabel('Time [s]', fontsize = 8)
        axs[1,0].set_ylabel('Gyroscope \n [rads/s]', fontsize = 8)
        axs[1,0].tick_params(axis='both', labelsize=6)

        axs[1,1].plot(plotTime, current0 , 'r', 
                      plotTime, current1, 'w' )
        axs[1,1].set_title("Current", fontsize = 10)
        axs[1,1].set_xlabel('Time [s]', fontsize = 8)
        axs[1,1].set_ylabel('Current \n [A]', fontsize = 8)
        axs[1,1].tick_params(axis='both', labelsize=6)

        axs[1,2].plot(plotTime, battVoltage, 'r')
        axs[1,2].set_title("Battery Voltage", fontsize = 10)
        axs[1,2].set_xlabel('Time [s]', fontsize = 8)
        axs[1,2].set_ylabel('Battery Voltage \n [V]', fontsize = 8)
        axs[1,2].tick_params(axis='both', labelsize=6)

        plt.tight_layout()
        fig.canvas.set_window_title("QBot Platform Sensor Data Overview")
        plt.show()
        #endregion 

    except KeyboardInterrupt:
        print('User Interrupted')
        KILL_THREAD = True
    finally:
        print("Exiting...")
        KILL_THREAD = True
    input('Basic IO script complete. Press the Enter key to exit...')
#endregion