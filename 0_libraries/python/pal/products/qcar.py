
"""qcar: A module for simplifying interactions with the QCar hardware platform.

This module provides a set of API classes and tools to facilitate working with
the QCar hardware platform. It is designed to make it easy to set up and read
data from various QCar sensors and components, as well as perform basic
input/output operations.
"""
import numpy as np
import platform
import os
import json
import time
from quanser.devices.exceptions import DeviceError
from quanser.hardware import HIL, HILError, PWMMode, MAX_STRING_LENGTH, Clock
from quanser.hardware.enumerations import BufferOverflowMode
try:
    from quanser.common import Timeout
except:
    from quanser.communications import Timeout

from pal.utilities.vision import Camera2D, Camera3D
from pal.utilities.lidar import Lidar
from pal.utilities.stream import BasicStream
from pal.utilities.math import Calculus
from pal.products.qcar_config import  QCar_check
from os.path import realpath, join, exists , dirname

IS_PHYSICAL_QCAR = ('nvidia' == os.getlogin()) \
    and ('aarch64' == platform.machine())
"""A boolean constant indicating if the current device is a physical QCar.

This constant is set to True if both the following conditions are met:
1. The current user's login name is 'nvidia'.
2. The underlying system's hardware architecture is 'aarch64'.

It's intended to be used for configuring execution as needed depending on if
the executing platform is a physical and virtual QCar.
"""

QCAR_CONFIG_PATH=join(dirname(realpath(__file__)),'qcar_config.json')
"""The absolute path of QCar configuration file.
QCar config file should always be saved in the same directory as qcar.py.
"""

try:
    QCar_check(IS_PHYSICAL_QCAR)
    QCAR_CONFIG=json.load(open(QCAR_CONFIG_PATH,'r'))
except HILError as e:
    print('QCar configuration file loading unsuccessful')
    print(e.get_error_message())
"""
A Dictionary containing QCar type-specific parameters. When a class from 
qcar module is called, the config file is automatically created and loaded.
When using a virtual QCar, user will be asked to specify the QCar type.
"""

class QCar():
    """Class for performing basic QCarIO"""
    # Car constants

    def __init__(
            self,
            readMode=0,
            frequency=500,
            pwmLimit=0.3,
            steeringBias=0,
            hilPort = 18960
        ):
        """ Configure and initialize the QCar.

        readMode:
            0 = immediate I/O,
            1 = task based I/O

        id: board identifier id number for virtual use only
        frequency: sampling frequency (used when readMode = 1)
        pwmLimit: maximum (and absolute minimum) command for writing to motors
        steeringBias: steering bias to add to steering command internally
        """

        self.card = HIL()
        self.hardware = IS_PHYSICAL_QCAR
        self.carType = QCAR_CONFIG['cartype'] #read from config file

        if self.hardware:
            boardIdentifier = "0"
        else:
            boardIdentifier = "0@tcpip://localhost:" +str(hilPort)+ "?nagle='off'"
        
        try:
            self.card.open(QCAR_CONFIG["carname"], boardIdentifier)
        except HILError as e:
            print(e.get_error_message())

        if self.carType == 0:
            print('No QCar found!')
            return
        
        self.readMode = readMode
        self.io_task_running = False
        self.pwmLimit = pwmLimit
        self.steeringBias = steeringBias
        self.frequency = frequency

        self._configure_parameters()


        if self.card.is_valid():
            self._set_options()

            if self.hardware and self.readMode == 1:
                self._create_io_task()
            print('QCar configured successfully.')

        # Read buffers (external)
        self.motorCurrent = np.zeros(1, dtype=np.float64)
        self.batteryVoltage = np.zeros(1, dtype=np.float64)
        self.motorEncoder = np.zeros(1, dtype=np.int32)
        self.motorTach = np.zeros(1, dtype=np.float64)
        self.accelerometer = np.zeros(3, dtype=np.float64)
        self.gyroscope = np.zeros(3, dtype=np.float64)

        self.START_TIME = time.time()

    def _elapsed_time(self):
        return time.time() - self.START_TIME

    def _configure_parameters(self):
        # Common Constants
        self.ENCODER_COUNTS_PER_REV = 720.0 # counts per revolution
        self.WHEEL_TRACK = 0.172 # left to right wheel distance in m

        ### QCar type-specific parameters

        self.WHEEL_RADIUS = QCAR_CONFIG['WHEEL_RADIUS'] # front/rear wheel radius in m
        self.WHEEL_BASE = QCAR_CONFIG['WHEEL_BASE'] # front to rear wheel distance in m
        self.PIN_TO_SPUR_RATIO = QCAR_CONFIG['PIN_TO_SPUR_RATIO']
        self.CPS_TO_MPS = (1/(self.ENCODER_COUNTS_PER_REV*4) # motor-speed unit conversion
            * self.PIN_TO_SPUR_RATIO * 2*np.pi * self.WHEEL_RADIUS)

        # Write channels
        self.WRITE_PWM_CHANNELS = np.array(
            QCAR_CONFIG['WRITE_PWM_CHANNELS'], 
            dtype=np.int32)
        self.WRITE_OTHER_CHANNELS = np.array(
            QCAR_CONFIG['WRITE_OTHER_CHANNELS'],
            dtype=np.int32
            )
        self.WRITE_DIGITAL_CHANNELS = np.array(
            QCAR_CONFIG['WRITE_DIGITAL_CHANNELS'],
            dtype=np.int32
            )
        # write buffer channels:
        self.writePWMBuffer = np.zeros(
            QCAR_CONFIG['writePWMBuffer'], 
            dtype=np.float64)
        self.writeDigitalBuffer = np.zeros(
            QCAR_CONFIG['writeDigitalBuffer'], 
            dtype=np.int8)
        self.writeOtherBuffer = np.zeros(
            QCAR_CONFIG['writeOtherBuffer'], 
            dtype=np.float64)

        # Read channels
        self.READ_ANALOG_CHANNELS = np.array(
            QCAR_CONFIG['READ_ANALOG_CHANNELS'], 
            dtype=np.int32)
        self.READ_ENCODER_CHANNELS = np.array(
            QCAR_CONFIG['READ_ENCODER_CHANNELS'], 
            dtype=np.uint32)
        self.READ_OTHER_CHANNELS = np.array(
            QCAR_CONFIG['READ_OTHER_CHANNELS'],
            dtype=np.int32
            )

        # Read buffers (internal)
        self.readAnalogBuffer = np.zeros(
            QCAR_CONFIG['readAnalogBuffer'], 
            dtype=np.float64)
        self.readEncoderBuffer = np.zeros(
            QCAR_CONFIG['readEncoderBuffer'], 
            dtype=np.int32)
        self.readOtherBuffer = np.zeros(
            QCAR_CONFIG['readOtherBuffer'], 
            dtype=np.float64)

    def _set_options(self):
        if self.carType == 1:
            # Set PWM mode (duty cycle)
            self.card.set_pwm_mode(
                np.array([0], dtype=np.uint32),
                1,
                np.array([PWMMode.DUTY_CYCLE], dtype=np.int32)
            )
            # Set PWM frequency
            self.card.set_pwm_frequency(
                np.array([0], dtype=np.uint32),
                1,
                np.array([60e6/4096], dtype=np.float64)
            )
            # Set Motor coast to 0
            self.card.write_digital(
                np.array([40], dtype=np.uint32),
                1,
                np.zeros(1, dtype=np.float64)
            )

        # Set board-specific options
        boardOptionsString = ("steer_bias=" + str(self.steeringBias)
            + ";motor_limit=" + str(self.pwmLimit) + ';')
        self.card.set_card_specific_options(
            boardOptionsString,
            MAX_STRING_LENGTH
        )

        # Set Encoder Properties
        self.card.set_encoder_quadrature_mode(
            self.READ_ENCODER_CHANNELS,
            len(self.READ_ENCODER_CHANNELS),
            np.array([4],
            dtype=np.uint32)
        )
        if IS_PHYSICAL_QCAR or self.carType == 1:
            self.card.set_encoder_filter_frequency(
                self.READ_ENCODER_CHANNELS,
                len(self.READ_ENCODER_CHANNELS),
                np.array([60e6/1],
                dtype=np.uint32)
            )
        self.card.set_encoder_counts(
            self.READ_ENCODER_CHANNELS,
            len(self.READ_ENCODER_CHANNELS),
            np.zeros(1, dtype=np.int32)
        )

    def _create_io_task(self):
        # Define reading task for QCar 1 or QCar 2
        self.readTask = self.card.task_create_reader(
            int(self.frequency*2),
            self.READ_ANALOG_CHANNELS,
            len(self.READ_ANALOG_CHANNELS),
            self.READ_ENCODER_CHANNELS,
            len(self.READ_ENCODER_CHANNELS),
            None,
            0,
            self.READ_OTHER_CHANNELS,
            len(self.READ_OTHER_CHANNELS)
        )

        # Set buffer overflow mode depending on
        # whether its for hardware or virtual QCar
        if self.hardware:
            self.card.task_set_buffer_overflow_mode(
                self.readTask,
                BufferOverflowMode.OVERWRITE_ON_OVERFLOW
            )
        else:
            self.card.task_set_buffer_overflow_mode(
                self.readTask,
                BufferOverflowMode.WAIT_ON_OVERFLOW
            )

        # Start the reading task
        self.card.task_start(
            self.readTask,
            Clock.HARDWARE_CLOCK_0,
            self.frequency,
            HIL.INFINITE
        )
        self.io_task_running = True

    def terminate(self):
        # This function terminates the QCar card after setting
        # final values for throttle, steering and LEDs.
        # Also terminates the task reader.

        try:
            # write 0 PWM command, 0 steering, and turn off all LEDs
            if self.carType == 1:
                self.write(0, 0, np.zeros(8, dtype=np.float64))
            elif self.carType == 2:
                self.write(0, 0, np.zeros(16, dtype=np.int8))

            # if using Task based I/O, stop the readTask.
            if self.readMode:
                self.card.task_stop(self.readTask)
            self.card.close()

        except HILError as h:
            print(h.get_error_message())

    def read_write_std(self, throttle, steering, LEDs=None):
        """ Read and write standard IO signals for the QCar

        Use this to write throttle, steering and LED commands, as well as
            update buffers for battery voltage, motor current,
            motor encoder counts, motor tach speed, and IMU data.

        throttle - this method will saturate based on the pwmLimit.

        steering - this method will saturate from -0.6 rad to 0.6 rad

        LEDs - a numpy string of 8 values

        Updates the following 6 buffers: motorCurrent, batteryVoltage,
            accelerometer, gyroscope, motorEncoder, motorTach

        """
        self.write(throttle, steering, LEDs)
        self.read()

    def read(self):
        if not (self.hardware or self.io_task_running) and self.readMode:
            self._create_io_task()

        try:
            # if using task based I/O, use the read task
            self.currentTimeStamp = self._elapsed_time()
            if self.readMode == 1:
                self.card.task_read(
                    self.readTask,
                    1,
                    self.readAnalogBuffer,
                    self.readEncoderBuffer,
                    None,
                    self.readOtherBuffer
                )
            else: # use immediate I/O
                self.card.read(
                    self.READ_ANALOG_CHANNELS,
                    len(self.READ_ANALOG_CHANNELS),
                    self.READ_ENCODER_CHANNELS,
                    len(self.READ_ENCODER_CHANNELS),
                    None,
                    0,
                    self.READ_OTHER_CHANNELS,
                    len(self.READ_OTHER_CHANNELS),
                    self.readAnalogBuffer,
                    self.readEncoderBuffer,
                    None,
                    self.readOtherBuffer
                )
        except HILError as h:
            print(h.get_error_message())
        finally:
            # update external read buffers
            # self.timeStep = self.currentTimeStamp - self.prevTimeStamp
            # self.prevTimeStamp = self.currentTimeStamp
            self.motorCurrent = self.readAnalogBuffer[0]
            self.batteryVoltage = self.readAnalogBuffer[1]
            self.gyroscope = self.readOtherBuffer[0:3]
            self.accelerometer = self.readOtherBuffer[3:6]
            self.motorEncoder = self.readEncoderBuffer
            self.motorTach = self.readOtherBuffer[-1] * self.CPS_TO_MPS # is actually estimated qcar speed

    def write(self, throttle, steering, LEDs=None):
        if not (self.hardware or self.io_task_running) and self.readMode:
            self._create_io_task()

        if self.carType == 1:
            self.writeOtherBuffer[0] = -np.clip(steering, -0.6, 0.6)
            self.writePWMBuffer = -np.clip(throttle, -self.pwmLimit, self.pwmLimit)
            if LEDs is not None:
                self.writeOtherBuffer[1:9] = LEDs
        elif self.carType == 2:
            self.writeOtherBuffer[0] = np.clip(steering, -0.6, 0.6)
            self.writeOtherBuffer[1] = np.clip(throttle, -self.pwmLimit, self.pwmLimit)
            if LEDs is not None:
                # indicators
                self.writeDigitalBuffer[0:4] = LEDs[0:4]
                # brake lights
                self.writeDigitalBuffer[4] = LEDs[4]
                self.writeDigitalBuffer[5] = LEDs[4]
                self.writeDigitalBuffer[6] = LEDs[4]
                self.writeDigitalBuffer[7] = LEDs[4]
                # reverse lights
                self.writeDigitalBuffer[8] = LEDs[5]
                self.writeDigitalBuffer[9] = LEDs[5]
                # headlamps
                self.writeDigitalBuffer[10] = LEDs[6]
                self.writeDigitalBuffer[11] = LEDs[6]
                self.writeDigitalBuffer[12] = LEDs[6]
                self.writeDigitalBuffer[13] = LEDs[7]
                self.writeDigitalBuffer[14] = LEDs[7]
                self.writeDigitalBuffer[15] = LEDs[7]

        try:
            if self.carType == 1:
                self.card.write(
                    None,
                    0,
                    self.WRITE_PWM_CHANNELS,
                    len(self.WRITE_PWM_CHANNELS),
                    None,
                    0,
                    self.WRITE_OTHER_CHANNELS,
                    len(self.WRITE_OTHER_CHANNELS),
                    None,
                    self.writePWMBuffer,
                    None,
                    self.writeOtherBuffer
                )
            elif self.carType == 2:
                self.card.write(
                    None,
                    0,
                    None,
                    0,
                    self.WRITE_DIGITAL_CHANNELS,
                    len(self.WRITE_DIGITAL_CHANNELS),
                    self.WRITE_OTHER_CHANNELS,
                    len(self.WRITE_OTHER_CHANNELS),
                    None,
                    None,
                    self.writeDigitalBuffer,
                    self.writeOtherBuffer
                )
        except HILError as h:
            print(h.get_error_message())

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.terminate()

class QCarCameras:
    """Class for accessing the QCar's CSI cameras.

    Args:
        frameWidth (int, optional): Width of the camera frame.
            Defaults to 820.
        frameHeight (int, optional): Height of the camera frame.
            Defaults to 410.
        frameRate (int, optional): Frame rate of the camera.
            Defaults to 30.
        enableRight (bool, optional): Whether to enable the right camera.
            Defaults to False.
        enableBack (bool, optional): Whether to enable the back camera.
            Defaults to False.
        enableLeft (bool, optional): Whether to enable the left camera.
            Defaults to False.
        enableFront (bool, optional): Whether to enable the front camera.
            Defaults to False.

    Attributes:
        csi (list): A list of Camera2D objects representing the enabled cameras.
        csiRight (Camera2D): The Camera2D object representing the right camera.
        csiBack (Camera2D): The Camera2D object representing the back camera.
        csiLeft (Camera2D): The Camera2D object representing the left camera.
        csiFront (Camera2D): The Camera2D object representing the front camera.
    """

    def __init__(
            self,
            frameWidth=820,
            frameHeight=410,
            frameRate=30,
            enableRight=False,
            enableBack=False,
            enableLeft=False,
            enableFront=False,
            videoPort = 18961
        ):
        """ Initializes QCarCameras object. """
        if QCAR_CONFIG['cartype'] == 1:
            enable = [enableRight, enableBack, enableLeft, enableFront]
        elif QCAR_CONFIG['cartype']==2 :
            enable = [enableRight, enableBack, enableFront, enableLeft]
        self.csi = []
        for i in range(4):
            if enable[i]:
                if IS_PHYSICAL_QCAR:
                    cameraId = str(i)
                else:
                    cameraId = str(i) + "@tcpip://localhost:" + str(videoPort+i)

                self.csi.append(
                    Camera2D(
                        cameraId=cameraId,
                        frameWidth=frameWidth,
                        frameHeight=frameHeight,
                        frameRate=frameRate
                    )
                )
            else:
                self.csi.append(None)

        self.csiRight = self.csi[QCAR_CONFIG['csiRight']]
        self.csiBack = self.csi[QCAR_CONFIG['csiBack']]
        self.csiLeft = self.csi[QCAR_CONFIG['csiLeft']]
        self.csiFront = self.csi[QCAR_CONFIG['csiFront']]

    def readAll(self):
        """Reads frames from all enabled cameras."""
        flags=[]
        for c in self.csi:
            if c is not None:
                flags.append(c.read())
        return flags

    def __enter__(self):
        """Used for with statement."""

        return self

    def __exit__(self, type, value, traceback):
        """Used for with statement. Terminates all enabled cameras."""

        for c in self.csi:
            if c is not None:
                c.terminate()

    def terminate(self):
        """Used for with statement. Terminates all enabled cameras."""

        for c in self.csi:
            if c is not None:
                c.terminate()

class QCarLidar(Lidar):
    """QCarLidar class represents the LIDAR sensor on the QCar.

    Inherits from Lidar class in pal.utilities.lidar

    Args:
        numMeasurements (int): The number of LIDAR measurements.
        rangingDistanceMode (int): The ranging distance mode.
        interpolationMode (int): The interpolation mode.
        interpolationMaxDistance (int): The maximum interpolation distance.
        interpolationMaxAngle (int): The maximum interpolation angle.
        enableFiltering (bool): enable filtering RPLidar Data.
            Defaults to True.
        angularResolution (float): Desired angular resolution of the lidar
            data after filtering (if enabled).
    """

    def __init__(
            self,
            numMeasurements=384,
            rangingDistanceMode=2,
            interpolationMode=0,
            interpolationMaxDistance=0,
            interpolationMaxAngle=0,
            enableFiltering=True,
            angularResolution=1*np.pi/180,
            lidarPort = 18966
        ):
        """Initializes a new instance of the QCarLidar class.

        Args:
            numMeasurements (int): The number of LIDAR measurements.
            rangingDistanceMode (int): The ranging distance mode.
            interpolationMode (int): The interpolation mode.
            interpolationMaxDistance (int): The maximum interpolation distance.
            interpolationMaxAngle (int): The maximum interpolation angle.
            enableFiltering (bool): enable filtering RPLidar Data.
                Defaults to True.
            angularResolution (float): Desired angular resolution of the lidar
                data after filtering (if enabled).
        """

        try:
            # QCar 1
            if IS_PHYSICAL_QCAR:
                self.url = QCAR_CONFIG['lidarurl']
            else:
                self.url = "tcpip://localhost:" +str(lidarPort)

            super().__init__(
                type='RPLidar',
                numMeasurements=numMeasurements,
                rangingDistanceMode=rangingDistanceMode,
                interpolationMode=interpolationMode,
                interpolationMaxDistance=interpolationMaxDistance,
                interpolationMaxAngle=interpolationMaxAngle
            )

        except DeviceError as e:
            print("Lidar Error")
            print(e.get_error_message())


        # print(Lidar().url)

        self.enableFiltering = enableFiltering
        self.angularResolution = angularResolution
        self._phi = np.linspace(
            0,
            2*np.pi,
            np.int_(np.round(2*np.pi/self.angularResolution))
            )

    def read(self):
        """
        Reads data from the LIDAR sensor and applies filtering if enabled.
        """
        new=super().read()
        if self.enableFiltering:
            self.angles, self.distances = self.filter_rplidar_data(
                self.angles, self.distances
            )
        return new

    def filter_rplidar_data(self, angles, distances):
        """ Filters RP LIDAR data

        Filters RP LIDAR data by deleting invalid reads, eliminating duplicate
        reads, interpolating distances to regularly spaced angles, and
        filling gaps with zeros.

        Args:
            angles (numpy.ndarray): The array of measured angles in radians.
            distances (numpy.ndarray): The array of measured distances.

        Returns:
            phiMeas (numpy.ndarray): An array of regularly spaced angles
                in radians.
            rFiltered (numpy.ndarray): The filtered array of distances.
        """

        phiRes = self.angularResolution
        # Delete invalid reads
        ids = (distances==0).squeeze()
        rMeas = np.delete(distances,ids)
        phiMeas = np.delete(angles,ids)
        if phiMeas.size == 0: return phiMeas,rMeas

        # Flip angle direction from CW to CCW and add 90 deg offset
        #phiMeas = wrap_to_2pi(2.5*np.pi-phiMeas)

        # Eliminate duplicate reads and sort
        phiMeas, ids = np.unique(phiMeas,return_index=True)
        rMeas = rMeas[ids]

        # Interpolate distances to regularly spaced angles
        rFiltered = np.interp(
            self._phi,
            phiMeas,
            rMeas,
            period=2*np.pi
        )

        # Find gaps where measurements were missed
        ids = np.diff(phiMeas) > 1.1*phiRes
        ids_lb = np.append(ids,False)
        ids_ub = np.append(False,ids)

        # Fill gaps with zeros
        lb = np.int_(np.ceil(phiMeas[ids_lb]/phiRes))
        ub = np.int_(np.floor(phiMeas[ids_ub]/phiRes))
        for i in range(lb.size):
            rFiltered[lb[i]:ub[i]] = 0

        phiMeasMin = np.int_(np.round(phiMeas[0]/phiRes))
        phiMeasMax = np.int_(np.round(phiMeas[-1]/phiRes))
        rFiltered[0:phiMeasMin] = 0
        rFiltered[phiMeasMax+1:] = 0

        return self._phi.astype('float32'), rFiltered.astype('float32')

class QCarRealSense(Camera3D):
    """
    A class for accessing 3D camera data from the RealSense camera on the QCar.

    Inherits from Camera3D class in pal.utilities.vision

    Args:
        mode (str): Mode to use for capturing data. Default is 'RGB&DEPTH'.
        frameWidthRGB (int): Width of the RGB frame. Default is 1920.
        frameHeightRGB (int): Height of the RGB frame. Default is 1080.
        frameRateRGB (int): Frame rate of the RGB camera. Default is 30.
        frameWidthDepth (int): Width of the depth frame. Default is 1280.
        frameHeightDepth (int): Height of the depth frame. Default is 720.
        frameRateDepth (int): Frame rate of the depth camera. Default is 15.
        frameWidthIR (int): Width of the infrared (IR) frame. Default is 1280.
        frameHeightIR (int): The height of the IR frame. Default is 720.
        frameRateIR (int): Frame rate of the IR camera. Default is 15.
        readMode (int): Mode to use for reading data from the camera.
            Default is 1.
        focalLengthRGB (numpy.ndarray): RGB camera Focal length in pixels.
            Default is np.array([[None], [None]], dtype=np.float64).
        principlePointRGB (numpy.ndarray): Principle point of the RGB camera
            in pixels. Default is np.array([[None], [None]], dtype=np.float64).
        skewRGB (float): Skew factor for the RGB camera. Default is None.
        positionRGB (numpy.ndarray): An array of shape (3, 1) that holds the
            position of the RGB camera in the car's frame of reference.
        orientationRGB (numpy.ndarray): An array of shape (3, 3) that holds the
            orientation of the RGB camera in the car's frame of reference.
        focalLengthDepth (numpy.ndarray): An array of shape (2, 1) that holds
            the focal length of the depth camera.
        principlePointDepth (numpy.ndarray): An array of shape (2, 1) that
            holds the principle point of the depth camera.
        skewDepth (float, optional): Skew of the depth camera
        positionDepth (numpy.ndarray, optional): An array of shape (3, 1) that
            holds the position of the depth camera
        orientationDepth (numpy.ndarray): An array of shape (3, 3) that holds
            the orientation of the Depth camera in the car's reference frame.
    """
    def __init__(
            self,
            mode='RGB&DEPTH',
            frameWidthRGB=1920,
            frameHeightRGB=1080,
            frameRateRGB=30,
            frameWidthDepth=1280,
            frameHeightDepth=720,
            frameRateDepth=15,
            frameWidthIR=1280,
            frameHeightIR=720,
            frameRateIR=15,
            readMode=1,
            focalLengthRGB=np.array([[None], [None]], dtype=np.float64),
            principlePointRGB=np.array([[None], [None]], dtype=np.float64),
            skewRGB=None,
            positionRGB=np.array([[None], [None], [None]], dtype=np.float64),
            orientationRGB=np.array(
                [[None, None, None], [None, None, None], [None, None, None]],
                dtype=np.float64),
            focalLengthDepth=np.array([[None], [None]], dtype=np.float64),
            principlePointDepth=np.array([[None], [None]], dtype=np.float64),
            skewDepth=None,
            positionDepth=np.array([[None], [None], [None]], dtype=np.float64),
            orientationDepth=np.array(
                [[None, None, None], [None, None, None], [None, None, None]],
                dtype=np.float64),
            video3dPort = 18965,
        ):

        if IS_PHYSICAL_QCAR:
            deviceId = '0'
        else:
            deviceId = "0@tcpip://localhost:" +str(video3dPort)
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


class QCarGPS:
    """A class that reads GPS data from the GPS server.

    In order to use this class, the qcarLidarToGPS must already be running.
    You can launch a qcarLidarToGPS server using the QCarLidarToGPS class
    defined in pal.products.qcar.

    Attributes:
        position (numpy.ndarray): Holds the most recent position
            read from the GPS. Format is [x, y, z].
        orientation (numpy.ndarray): Holds the most recent orientation
            read from the GPS. Format is [roll, pitch, yaw].

    Methods:
        read(): Reads GPS data from the GPS server and updates the position
            and orientation attributes.
        terminate(): Terminates the GPS client.

    Example:
        .. code-block:: python

            # Launch the qcarLidarToGPS server (if not already running)
            gpsServer = QCarLidarToGPS(initialPose=[0, 0, 0])

            # Create an instance of the QCarGPS class
            gps = QCarGPS()

            # Read GPS data
            gps.read()

            print('position = ' + gps.position)
            print('orientation = ' + gps.orientation)

            # Terminate the GPS client
            gps.terminate()

    """

    def __init__(self, initialPose=[0, 0, 0], calibrate=False, gpsPort = 18967, lidarIdealPort = 18968):
        """
        Initializes the QCarGPS class with the initial pose of the QCar.

        Args:
            initialPose (list, optional): Initial pose of the QCar
                as [x0, y0, th0] (default [0, 0, 0]).
        """
        
        self._need_calibrate = calibrate
        if IS_PHYSICAL_QCAR:
            self.__initLidarToGPS(initialPose)

        self._timeout = Timeout(seconds=0, nanoseconds=1)
        # Setup GPS client and connect to GPS server
        self.position = np.zeros((3))
        self.orientation = np.zeros((3))

        self._gps_data = np.zeros((6), dtype=np.float32)
        self._gps_client = BasicStream(
            uri="tcpip://localhost:" +str(gpsPort),
            agent='C',
            receiveBuffer=np.zeros(6, dtype=np.float32),
            sendBufferSize=1,
            recvBufferSize=(self._gps_data.size * self._gps_data.itemsize),
            nonBlocking=True
        )
        t0 = time.time()
        while not self._gps_client.connected:
            if time.time()-t0 > 5:
                print("Couldn't Connect to GPS Server")
                return
            self._gps_client.checkConnection()

        # Setup Lidar data client and connect to Lidar data server
        self.scanTime = 0
        self.angles = np.zeros(384)
        self.distances = np.zeros(384)

        self._lidar_data = np.zeros(384*2 + 1, dtype=np.float64)
        self._lidar_client = BasicStream(
            uri="tcpip://localhost:" +str(lidarIdealPort),
            agent='C',
            receiveBuffer=np.zeros(384*2 + 1, dtype=np.float64),
            sendBufferSize=1,
            recvBufferSize=8*(384*2 + 1),
            nonBlocking=True
        )
        t0 = time.time()
        if IS_PHYSICAL_QCAR or QCAR_CONFIG['cartype']==1:
            while not self._lidar_client.connected:
                if time.time()-t0 > 5:
                    print("Couldn't Connect to Lidar Server")
                    return
                self._lidar_client.checkConnection()
        else:
            self.lidar = QCarLidar()
        self.enableFiltering = True
        self.angularResolution = 1*np.pi/180
        self._phi = np.linspace(
            0,
            2*np.pi,
            np.int_(np.round(2*np.pi/self.angularResolution))
        )


    def __initLidarToGPS(self, initialPose):
        self.__initialPose = initialPose

        self.__stopLidarToGPS()

        if self._need_calibrate:
            self.__calibrate()
            # wait period to complete calibration completely
            time.sleep(16)
        if os.path.exists(os.path.join(os.getcwd(),'angles_new.mat')):
            self.__emulateGPS()
            time.sleep(4)
            print('GPS Server started.')
        else:
            print('Calibration files not found, please set the argument \'calibration\' to True.')
            exit(1)

    def __stopLidarToGPS(self):
        # Quietly stop qcarLidarToGPS if it is already running:
        # the -q flag kills the executable
        # the -Q flag kills quietly (no errors thrown if its not running)
        os.system(
            'quarc_run -t tcpip://localhost:17000 -q -Q '
            + QCAR_CONFIG['lidarToGps']
        )

    def __calibrate(self):
        """Calibrates the QCar at its initial position and heading."""

        print('Calibrating QCar at position ', self.__initialPose[0:2],
            ' (m) and heading ', self.__initialPose[2], ' (rad).')

        # setup the path to the qcarCaptureScan file
        captureScanfile = os.path.normpath(os.path.join(
            os.path.dirname(__file__),
            '../../../resources/applications/QCarScanMatching/'
                + QCAR_CONFIG['captureScan']
        ))

        os.system(
            'quarc_run -t tcpip://localhost:17000 '
            + captureScanfile + ' -d ' + os.getcwd()
        )

    def __emulateGPS(self):
        """Starts the GPS emulation using the qcarLidarToGPS executable."""

        # setup the path to the qcarLidarToGPS file
        lidarToGPSfile = os.path.normpath(os.path.join(
            os.path.dirname(__file__),
            '../../../resources/applications/QCarScanMatching/'
                + QCAR_CONFIG['lidarToGps']
        ))
        os.system(
            'quarc_run -r -t tcpip://localhost:17000 '
            + lidarToGPSfile + ' -d ' + os.getcwd()
            + ' -pose_0 ' + str(self.__initialPose[0])
            + ',' + str(self.__initialPose[1])
            + ',' + str(self.__initialPose[2])
        )

    def readGPS(self):
        """Reads GPS data from the server and updates the position
            and orientation attributes.

        Returns:
            bool: True if new GPS data was received.
        """
        recvFlag, bytesReceived = self._gps_client.receive(
            iterations=1,
            timeout=self._timeout)

        if recvFlag:
            self.position = self._gps_client.receiveBuffer[0:3]
            self.orientation = self._gps_client.receiveBuffer[3:6]

        return recvFlag

    def readLidar(self):
        """Reads GPS data from the server and updates the position
            and orientation attributes.

        Returns:
            bool: True if new GPS data was received.
        """
        if not IS_PHYSICAL_QCAR and QCAR_CONFIG['cartype']==2:
            # print('use QCarLidar() class to use Lidar for virtual QCar2')
            recvFlag = self.lidar.read()
            self.angles = self.lidar.angles
            self.distances = self.lidar.distances
            return recvFlag
        recvFlag, bytesReceived = self._lidar_client.receive(
            iterations=1,
            timeout=self._timeout)

        if recvFlag:
            self.scanTime = self._lidar_client.receiveBuffer[0]
            self.distances = self._lidar_client.receiveBuffer[1:385]
            self.angles = self._lidar_client.receiveBuffer[385:769]

            self.angles, self.distances = self.filter_rplidar_data(
                self.angles,
                self.distances
            )

        return recvFlag


    def filter_rplidar_data(self, angles, distances):
        """ Filters RP LIDAR data

        Filters RP LIDAR data by deleting invalid reads, eliminating duplicate
        reads, interpolating distances to regularly spaced angles, and
        filling gaps with zeros.

        Args:
            angles (numpy.ndarray): The array of measured angles in radians.
            distances (numpy.ndarray): The array of measured distances.

        Returns:
            phiMeas (numpy.ndarray): An array of regularly spaced angles
                in radians.
            rFiltered (numpy.ndarray): The filtered array of distances.
        """

        phiRes = self.angularResolution
        # Delete invalid reads
        ids = (distances==0)
        phiMeas = np.delete(angles,ids)
        rMeas = np.delete(distances,ids)
        if phiMeas.size == 0: return phiMeas,rMeas

        # Flip angle direction from CW to CCW and add 90 deg offset
        #phiMeas = wrap_to_2pi(2.5*np.pi-phiMeas)

        # Eliminate duplicate reads and sort
        phiMeas, ids = np.unique(phiMeas,return_index=True)
        rMeas = rMeas[ids]

        # Interpolate distances to regularly spaced angles
        rFiltered = np.interp(
            self._phi,
            phiMeas,
            rMeas,
            period=2*np.pi
        )

        # Find gaps where measurements were missed
        ids = np.diff(phiMeas) > 1.1*phiRes
        ids_lb = np.append(ids,False)
        ids_ub = np.append(False,ids)

        # Fill gaps with zeros
        lb = np.int_(np.ceil(phiMeas[ids_lb]/phiRes))
        ub = np.int_(np.floor(phiMeas[ids_ub]/phiRes))
        for i in range(lb.size):
            rFiltered[lb[i]:ub[i]] = 0

        phiMeasMin = np.int_(np.round(phiMeas[0]/phiRes))
        phiMeasMax = np.int_(np.round(phiMeas[-1]/phiRes))
        rFiltered[0:phiMeasMin] = 0
        rFiltered[phiMeasMax+1:] = 0

        return self._phi, rFiltered


    def terminate(self):
        """ Terminates the GPS client. """
        self._gps_client.terminate()
        self._lidar_client.terminate()
        if IS_PHYSICAL_QCAR or QCAR_CONFIG['cartype']==1:
            self.__stopLidarToGPS()
        else:
            self.lidar.terminate()
            
    def __enter__(self):
        """ Used for with statement. """
        return self

    def __exit__(self, type, value, traceback):
        """ Used for with statement. Terminates the GPS client. """
        self.terminate()