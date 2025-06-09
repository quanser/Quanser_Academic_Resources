"""qbot_platfrom: Classes to simplify interactions with the QBot Platform.

This module provides a set of API classes and tools to facilitate working with
the QBot Platform. It is designed to make it easy to set up and read
data from various QBot sensors and components, as well as perform basic
input/output operations.  The driver class is designed to also implement
important safety features into the robot.

"""

import sys
import os
import platform
import numpy as np
from quanser.hardware import HIL, HILError, MAX_STRING_LENGTH, Clock
from quanser.hardware.enumerations import BufferOverflowMode
from quanser.common import Timeout
from pal.utilities.stream import BasicStream
from pal.utilities.vision import Camera2D, Camera3D
from pal.utilities.lidar import Lidar
from pal.utilities.math import Calculus


IS_PHYSICAL_QBOTPLATFORM = (('nvidia' == os.getlogin())
                            and ('aarch64' == platform.machine()))
"""A boolean constant indicating if the current device is a physical QBot 
Platform.

This constant is set to True if both the following conditions are met:
1. The current user's login name is 'pi'.
2. The underlying system's hardware architecture is 'aarch64'.

It's intended to be used for configuring execution as needed depending on if
the executing platform is a physical and virtual QBot Platform.
"""

class QBotPlatformDriver():
    """Driver class for performing basic QBot Platform IO
    
    Args:
            mode (int, optional): Determines the driver mode. Defaults to 1. 
                1 & 2 are designed for education, 3 & 4 are designed for 
                research. 1 and 3 are body mode, 2 and 4 are wheeled mode.
            ip (str): IP address of the QBot Platform.
    """

    def __init__(self, mode=1, ip='192.168.2.15') -> None:

        # QBot reads
        self.wheelPositions = np.zeros((2), dtype = np.float64)
        self.wheelSpeeds    = np.zeros((2), dtype = np.float64)
        self.motorCmd       = np.zeros((2), dtype = np.float64)
        self.accelerometer  = np.zeros((3), dtype = np.float64)
        self.gyroscope      = np.zeros((3), dtype = np.float64)
        self.currents       = np.zeros((2), dtype = np.float64)
        self.battVoltage    = np.zeros((1), dtype = np.float64)
        self.watchdog       = np.zeros((1), dtype = np.float64)

        # QBot Platform Driver listening on port 18888
        self.uri = 'tcpip://'+ip+':18888'

        # 1 ms timeout parameter
        self._timeout = Timeout(seconds=0, nanoseconds=1000000)

        # establish stream object to communicate with QBot Platform Driver
        self._handle = BasicStream(uri=self.uri,
                                    agent='C',
                                    receiveBuffer=np.zeros((17), 
                                                           dtype=np.float64),
                                    sendBufferSize=2048,
                                    recvBufferSize=2048,
                                    nonBlocking=True)

        # Only set mode on initialization, this value is not set in read-write
        self._sendPacket = np.zeros((10), dtype=np.float64)
        self._sendPacket[0] = mode
        self._mode = mode

        # if connected to the Driver, proceed, else, try to connect.
        self.status_check('Connected to QBot Platform Driver.', iterations=20)
        # there is no return here.

    def status_check(self, message, iterations=10):
        # blocking method to establish connection to the server stream.
        self._timeout = Timeout(seconds=0, nanoseconds=1000) #1000000
        counter = 0
        while not self._handle.connected:
            self._handle.checkConnection(timeout=self._timeout)
            counter += 1
            if self._handle.connected:
                print(message)
                break
            elif counter >= iterations:
                print('Driver error: status check failed.')
                break

            # once you connect, self._handle.connected goes True, and you
            # leave this loop.

    def read_write_std(self, 
                       timestamp, 
                       arm = 1, 
                       commands=np.zeros((2), dtype=np.float64), 
                       userLED=False, 
                       color=[1, 0, 1], 
                       hold = 0):

        # data received flag
        new = False

        # 1 us timeout parameter
        self._timeout = Timeout(seconds=0, nanoseconds=1000)

        # set User LED color values if desired
        if userLED:
            self._sendPacket[1] = 1.0 # User LED packet
            self._sendPacket[2:5] = np.array([color[0], color[1], color[2]])
        else:
            self._sendPacket[1] = 0.0 # User LED packet
            self._sendPacket[2:5] = np.array([0, 0, 0])

        # set remaining packet to send
        self._sendPacket[5] = arm
        self._sendPacket[6] = hold
        self._sendPacket[7] = commands[0]
        self._sendPacket[8] = commands[1]
        self._sendPacket[9] = timestamp

        # if connected to driver, send/receive
        if self._handle.connected:
            self._handle.send(self._sendPacket)
            new, bytesReceived = self._handle.receive(timeout=self._timeout)
            # if new is True, full packet was received
            if new:
                self.wheelPositions = self._handle.receiveBuffer[0:2]
                self.wheelSpeeds = self._handle.receiveBuffer[2:4]
                self.motorCmd = self._handle.receiveBuffer[4:6]
                self.accelerometer = self._handle.receiveBuffer[6:9]
                self.gyroscope = self._handle.receiveBuffer[9:12]
                self.currents = self._handle.receiveBuffer[12:14]
                self.battVoltage = self._handle.receiveBuffer[14]
                self.watchdog = self._handle.receiveBuffer[15]
                self.timeStampRecv = self._handle.receiveBuffer[16]

        else:
            self.status_check('Reconnected to QBot Platform Driver.')

        # if new is False, data is stale, else all is good
        return new

    def terminate(self):
        self._handle.terminate()


class QBotPlatformLidar(Lidar):
    """
    QBotPlatfromLidar class represents the LIDAR sensor on the QBot Platform.

    Inherits from Lidar class in pal.utilities.lidar

    Args:
        numMeasurements (int): The number of LIDAR measurements.
        interpolationMode (int): The interpolation mode.
        interpolationMaxDistance (int): The maximum interpolation distance.
        interpolationMaxAngle (int): The maximum interpolation angle.
    """

    # Initializes a new instance of the QBotPlatformLidar class.

    def __init__(
        self,
        numMeasurements=1680,
        interpolationMode=0,
        interpolationMaxDistance=0,
        interpolationMaxAngle=0
        ):
        
        if IS_PHYSICAL_QBOTPLATFORM:
            self.url = ("serial://localhost:0?baud='512000',"
                        "word='8',parity='none',stop='1',flow='none',device='/dev/lidar'")
        else:
            self.url = "tcpip://localhost:18918"

        super().__init__(
            type='leishenm10p',
            numMeasurements=numMeasurements,
            interpolationMode=interpolationMode,
            interpolationMaxDistance=interpolationMaxDistance,
            interpolationMaxAngle=interpolationMaxAngle
        )

class QBotPlatformRealSense(Camera3D):
    """
    A class for accessing 3D camera data from the RealSense camera on the QBot 
    Platform.

    Inherits from Camera3D class in pal.utilities.vision

    Args:
        mode (str): Mode to use for capturing data. Default is 'RGB&DEPTH'.
        frameWidthRGB (int): Width of the RGB frame. Default is 640.
        frameHeightRGB (int): Height of the RGB frame. Default is 400.
        frameRateRGB (int): Frame rate of the RGB camera. Default is 30.
        frameWidthDepth (int): Width of the depth frame. Default is 640.
        frameHeightDepth (int): Height of the depth frame. Default is 400.
        frameRateDepth (int): Frame rate of the depth camera. Default is 15.
        frameWidthIR (int): Width of the infrared (IR) frame. Default is 640.
        frameHeightIR (int): The height of the IR frame. Default is 400.
        frameRateIR (int): Frame rate of the IR camera. Default is 15.
        readMode (int): Mode to use for reading data from the camera.
            Default is 1.
        focalLengthRGB (numpy.ndarray): RGB camera focal length in pixels.
            Default is np.array([[None], [None]], dtype=np.float64).
        principlePointRGB (numpy.ndarray): Principle point of the RGB camera
            in pixels. Default is np.array([[None], [None]], dtype=np.float64).
        skewRGB (float): Skew factor for the RGB camera. Default is None.
        positionRGB (numpy.ndarray): An array of shape (3, 1) that holds the
            position of the RGB camera in the QBot's frame of reference.
        orientationRGB (numpy.ndarray): An array of shape (3, 3) that holds the
            orientation of the RGB camera in the QBot's frame of reference.
        focalLengthDepth (numpy.ndarray): An array of shape (2, 1) that holds
            the focal length of the depth camera.
        principlePointDepth (numpy.ndarray): An array of shape (2, 1) that
            holds the principle point of the depth camera.
        skewDepth (float, optional): Skew of the depth camera
        positionDepth (numpy.ndarray, optional): An array of shape (3, 1) that
            holds the position of the depth camera
        orientationDepth (numpy.ndarray): An array of shape (3, 3) that holds
            the orientation of the Depth camera in the QBot's reference frame.
    """
    def __init__(
            self,
            mode='RGB&DEPTH',
            frameWidthRGB=640,
            frameHeightRGB=400,
            frameRateRGB=30,
            frameWidthDepth=640,
            frameHeightDepth=400,
            frameRateDepth=15,
            frameWidthIR=640,
            frameHeightIR=400,
            frameRateIR=15,
            readMode=1,
            focalLengthRGB=np.array([[None], [None]], dtype=np.float64),
            principlePointRGB=np.array([[None], [None]], dtype=np.float64),
            skewRGB=None,
            positionRGB=np.array([[None], [None], [None]], dtype=np.float64),
            orientationRGB=np.array([[None, None, None], [None, None, None],
                                     [None, None, None]], dtype=np.float64),
            focalLengthDepth=np.array([[None], [None]], dtype=np.float64),
            principlePointDepth=np.array([[None], [None]], dtype=np.float64),
            skewDepth=None,
            positionDepth=np.array([[None], [None], [None]], dtype=np.float64),
            orientationDepth=np.array([[None, None, None], [None, None, None],
                                       [None, None, None]], dtype=np.float64)
        ):

        if IS_PHYSICAL_QBOTPLATFORM:
            deviceId = '0'
        else:
            deviceId = "0@tcpip://localhost:18917"
            frameWidthRGB = 640
            frameHeightRGB = 480
            frameRateRGB = 30
            frameWidthDepth = 640
            frameHeightDepth = 480
            frameRateDepth = 15
            frameWidthIR = 640
            frameHeightIR = 480
            frameRateIR = 30

        super().__init__(
            mode,
            frameWidthRGB,
            frameHeightRGB,
            frameRateRGB,
            frameWidthDepth,
            frameHeightDepth,
            frameRateDepth,
            frameWidthIR,
            frameHeightIR,
            frameRateIR,
            deviceId,
            readMode,
            focalLengthRGB,
            principlePointRGB,
            skewRGB,
            positionRGB,
            orientationRGB,
            focalLengthDepth,
            principlePointDepth,
            skewDepth,
            positionDepth,
            orientationDepth
        )

class QBotPlatformCSICamera(Camera2D):

    """Class for accessing the QBot Platform CSI camera.

    Args:
        frameWidth (int, optional): Width of the camera frame.
            Defaults to 640.
        frameHeight (int, optional): Height of the camera frame.
            Defaults to 400.
        frameRate (int, optional): Frame rate of the camera.
            Defaults to 30.

    """

    def __init__(

            self,
            frameWidth=640,
            frameHeight=400,
            frameRate=30,
            focalLength=np.array([[None], [None]], dtype=np.float64),
            principlePoint=np.array([[None], [None]], dtype=np.float64),
            skew=None,
            position=np.array([[None], [None], [None]], dtype=np.float64),
            orientation=np.array(
                [[None,None,None], [None,None,None], [None,None,None]],
                dtype=np.float64),
            brightness = None,
            contrast = None,
            gain = None
        ):

        if IS_PHYSICAL_QBOTPLATFORM:
            deviceId = '6'
        else:
            deviceId = "6@tcpip://localhost:18915"

        super().__init__(
            cameraId=deviceId,
            frameWidth=frameWidth,
            frameHeight=frameHeight,
            frameRate=frameRate,
            focalLength = focalLength,
            principlePoint = principlePoint,
            skew = skew,
            position=position,
            orientation=orientation,
            imageFormat=1,
            brightness = brightness,
            contrast = contrast,
            gain = gain
        )

