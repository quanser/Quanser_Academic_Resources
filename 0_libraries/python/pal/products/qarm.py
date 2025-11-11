import numpy as np
from quanser.hardware import HIL, HILError, MAX_STRING_LENGTH, Clock
from quanser.hardware.enumerations import BufferOverflowMode
from pal.utilities.vision import Camera3D

class QArm():
    """
    QArm class for initialization, I/O, and termination.

    Notes
    -----
    - The QArm can operate in Position mode (0) or PWM mode (1).
    - Use the `read_write_std` method for standard I/O operations.
    - Use the `terminate` method to cleanly shut down the QArm.
    """

    '''QArm class for initialization, I/O and termination'''
    HOME_POSE  = np.array([0, 0, 0, 0], dtype=np.float64)
    SLEEP_POSE = np.array([0, -17*np.pi/36, 15*np.pi/36, 0], dtype=np.float64)

    LIMITS_MAX = np.array([ 17*np.pi/18,  17*np.pi/36,  15*np.pi/36,  8*np.pi/9], dtype=np.float64)
    LIMITS_MIN = np.array([-17*np.pi/18, -17*np.pi/36, -19*np.pi/36, -8*np.pi/9], dtype=np.float64)

    #region: Channel and Buffer definitions

    # Channels
    WRITE_OTHER_CHANNELS = np.array([1000, 1001, 1002, 1003, 
                                     1004, 11005, 11006, 11007], dtype=np.int32)
    READ_OTHER_CHANNELS = np.array([1000, 1001, 1002, 1003, 1004, 
                                    3000, 3001, 3002, 3003, 3004, 
                                    10000, 10001, 10002, 10003, 10004, 
                                    11000, 11001, 11002, 11003, 11004], dtype=np.int32)
    READ_ANALOG_CHANNELS = np.array([5, 6, 7, 8, 9], dtype=np.int32)

    # Buffers (internal)
    writeOtherBuffer = np.zeros(len(WRITE_OTHER_CHANNELS), dtype=np.float64)
    readOtherBuffer = np.zeros(len(READ_OTHER_CHANNELS), dtype=np.float64)
    readAnalogBuffer = np.zeros(len(READ_ANALOG_CHANNELS), dtype=np.float64)

    # Buffers (external)
    measJointCurrent        = np.zeros(5, dtype=np.float64)
    measJointPosition       = np.zeros(5, dtype=np.float64)
    measJointSpeed          = np.zeros(5, dtype=np.float64)
    measJointPWM            = np.zeros(5, dtype=np.float64)
    measJointTemperature    = np.zeros(5, dtype=np.float64)


    #endregion

    def __init__(self, hardware=1, readMode=0, frequency=500, deviceId = 0, hilPort = 18900):
        """
        Initializes and configures the QArm in Position Mode. 
        (PWM mode not supported)

        Parameters
        ----------
        hardware : int, optional
            Indicates whether the QArm is hardware-based (1) or virtual (0). Defaults to 1.
        readMode : int, optional
            Mode for reading data. 0 for immediate I/O, 1 for task-based I/O. Defaults to 0.
        frequency : int, optional
            Sampling frequency (used when `readMode` is set to 1). Defaults to 500.
        deviceId : int, optional
            Identifier for the QArm device. Defaults to 0.
        hilPort : int, optional
            Port number for the HIL connection when using virtual QArm. Defaults to 18900.

        Raises
        ------
        HILError
            If there is an error during initialization.
        """

        self.readMode = readMode
        self.hardware = hardware
        self.status = False
        self.card = HIL()
        if self.hardware:
            boardIdentifier = str(deviceId)
        else:
            boardIdentifier = "0@tcpip://localhost:" + str(hilPort) + "?nagle='off'"

        
        # if empty BSO, use defaults

        boardSpecificOptions = (
            "j0_mode=0;j1_mode=0;j2_mode=0;j3_mode=0;"
            "gripper_mode=0;j0_profile_config=0;j0_profile_velocity=1.5708;"
            "j0_profile_acceleration=1.0472;j1_profile_config=0;"
            "j1_profile_velocity=1.5708;j1_profile_acceleration=1.0472;"
            "j2_profile_config=0;j2_profile_velocity=1.5708;"
            "j2_profile_acceleration=1.0472;j3_profile_config=0;"
            "j3_profile_velocity=1.5708;j3_profile_acceleration=1.0472;"
        )

        try:
            # Open the Card
            self.card.open("qarm_usb", boardIdentifier)
            if self.card.is_valid():
                self.card.set_card_specific_options(boardSpecificOptions, MAX_STRING_LENGTH)
                self.status = True
                if self.readMode == 1:
                    self.frequency = frequency
                    self.samples = HIL.INFINITE
                    self.samplesToRead = 1

                    # Define reading task
                    self.readTask = self.card.task_create_reader(   int(self.frequency),
                                                                    self.READ_ANALOG_CHANNELS, len(self.READ_ANALOG_CHANNELS),
                                                                    None, 0,
                                                                    None, 0,
                                                                    self.READ_OTHER_CHANNELS, len(self.READ_OTHER_CHANNELS))

                    # Set buffer overflow mode depending on whether its for hardware or virtual QArm
                    if self.hardware:
                        self.card.task_set_buffer_overflow_mode(self.readTask, BufferOverflowMode.OVERWRITE_ON_OVERFLOW)
                        self.card.set_double_property(np.array([128 , 129, 130, 131,   133,   134,   135,   136,  138,  139,  140,  141]),
                                                      12,
                                                      np.array([8.89,8.89,8.89,8.89, 0.012, 0.012, 0.012, 0.012,10.23,10.23,10.23,10.23]))
                        print('setting PID gains')
                    else:
                        self.card.task_set_buffer_overflow_mode(self.readTask, BufferOverflowMode.SYNCHRONIZED)

                    # Start the reading task
                    self.card.task_start(self.readTask, Clock.HARDWARE_CLOCK_0, self.frequency, 2**32-1)


                else:
                    if self.hardware:
                        self.card.set_double_property(np.array([128 , 129, 130, 131,   133,   134,   135,   136,  138,  139,  140,  141]),
                                                      12,
                                                      np.array([8.89,8.89,8.89,8.89, 0.012, 0.012, 0.012, 0.012,10.23,10.23,10.23,10.23]))
                        print('setting PID gains')
                    print('QArm configured in Position Mode.')

        except HILError as h:
            print(h.get_error_message())

    def read_write_std(self, phiCMD=np.zeros(4, dtype=np.float64),
                        gprCMD=np.zeros(1, dtype=np.float64),
                        baseLED=np.array([1, 0, 0], dtype=np.float64)):
        """
        Writes motor and LED commands, 
        and reads battery voltage, motor current, and encoder counts.

        Parameters
        ----------
        phiCMD : numpy.ndarray, optional
            Angular position of joints 1 to 4 as a 4x1 numpy array. Defaults to zeros.
            Active in Position mode only.
        gprCMD : numpy.ndarray, optional
            Gripper position as a 1x1 numpy array. Defaults to zeros.
        baseLED : numpy.ndarray, optional
            Base RGB LED state as a 3x1 numpy array. Defaults to red: [1, 0, 0].

        Notes
        -----
        The method reads data from the QArm 
        and updates the corresponding member variables.

        Updates the following member variables:
        - `measJointCurrent` (Amps)
        - `measJointPosition`
        - `measJointSpeed` (rad/s)
        - `measJointPWM` (0-1)
        - `measJointTemperature` 
        """

        self.writeOtherBuffer[4] = np.clip(gprCMD,0.1,0.9) # Saturate gripper between 0.1 (open) and 0.9 (close)
        self.writeOtherBuffer[5:] = baseLED
        for motorIndex in range(4):
            self.writeOtherBuffer[motorIndex] = phiCMD[motorIndex]

        # IO
        try:
            #Writes: Analog Channel, Num Analog Channel,
            # PWM Channel, Num PWM Channel, Digital Channel,
            #  Num Digital Channel, Other Channel,
            # Num Other Channel, Analog Buffer,
            # PWM Buffer, Digital Buffer, Other Buffer
            self.card.write(None, 0,
                            None, 0,
                            None, 0,
                            self.WRITE_OTHER_CHANNELS, len(self.WRITE_OTHER_CHANNELS),
                            None,
                            None,
                            None,
                            self.writeOtherBuffer)

            # self.write_position(phiCMD, gprCMD)
            # self.write_led(baseLED)
            self.read_std()

        except HILError as h:
            print(h.get_error_message())

    def read_std(self):
        """
        Reads battery voltage, motor current, and encoder counts.

        Notes
        -----
        The method reads data from the QArm 
        and updates the corresponding member variables.

        Updates the following member variables:
        - `measJointCurrent` (Amps)
        - `measJointPosition`
        - `measJointSpeed` (rad/s)
        - `measJointPWM` (0-1)
        - `measJointTemperature` 
        """

        # IO
        try:
            if self.readMode == 1:
                self.card.task_read(
                    self.readTask,
                    self.samplesToRead,
                    self.readAnalogBuffer,
                    None,
                    None,
                    self.readOtherBuffer
                )
            else:
                self.card.read(
                    self.READ_ANALOG_CHANNELS,
                    len(self.READ_ANALOG_CHANNELS),
                    None, 0,
                    None, 0,
                    self.READ_OTHER_CHANNELS,
                    len(self.READ_OTHER_CHANNELS),
                    self.readAnalogBuffer,
                    None,
                    None,
                    self.readOtherBuffer
                )
        except HILError as h:
            print(h.get_error_message())
        finally:
            self.measJointCurrent = self.readAnalogBuffer
            self.measJointPosition = self.readOtherBuffer[0:5]
            self.measJointSpeed = self.readOtherBuffer[5:10]
            self.measJointPWM = self.readOtherBuffer[15:20]
            self.measJointTemperature = self.readOtherBuffer[10:15]

    def write_position(self, phiCMD=np.zeros(4, dtype=np.float64),
                        gprCMD=np.zeros(1, dtype=np.float64) ):
        
        """
        Writes motor commands.

        Parameters
        ----------
        phiCMD : numpy.ndarray, optional
            Angular position of joints 1 to 4 as a 4x1 numpy array. Defaults to zeros.
            Active in Position mode only.
        gprCMD : numpy.ndarray, optional
            Gripper position as a 1x1 numpy array. Defaults to zeros.
        """

        self.writeOtherBuffer[4] = np.clip(gprCMD,0.1,0.9) # Saturate gripper between 0.1 (open) and 0.9 (close)

        new = False
        for motorIndex in range(4):
            self.writeOtherBuffer[motorIndex] = phiCMD[motorIndex]

        # IO
        try:
            #Writes: Analog Channel, Num Analog Channel,
            # PWM Channel, Num PWM Channel,
            # Digital Channel, Num Digital Channel,
            # Other Channel, Num Other Channel,
            # Analog Buffer, PWM Buffer,
            # Digital Buffer, Other Buffer
            self.card.write(None, 0,
                            None, 0,
                            None, 0,
                            self.WRITE_OTHER_CHANNELS[0:5], 5,
                            None,
                            None,
                            None,
                            self.writeOtherBuffer[0:5])

            new = True

        except HILError as h:
            print(h.get_error_message())
            new = False

    def write_led(self, baseLED=np.array([1, 0, 0], dtype=np.float64)):
        """
        Writes LED commands.

        Parameters
        ----------
        baseLED : numpy.ndarray, optional
            Base RGB LED state as a 3x1 numpy array. Defaults to [1, 0, 0].
        """

        self.writeOtherBuffer[5:] = baseLED

        # IO
        try:
            if True:
                #Writes: Analog Channel, Num Analog Channel, PWM Channel, Num PWM Channel, Digital Channel, Num Digital Channel, Other Channel, Num Other Channel, Analog Buffer, PWM Buffer, Digital Buffer, Other Buffer
                self.card.write(None, 0,
                                None, 0,
                                None, 0,
                                self.WRITE_OTHER_CHANNELS[5:], 3,
                                None,
                                None,
                                None,
                                self.writeOtherBuffer[5:])

        except HILError as h:
            print(h.get_error_message())

    def terminate(self):
        """
        Terminates the QArm card.

        Notes
        -----
        - Stops and deletes the reading task if `readMode` is 1.
        - Closes the connection to the QArm.
        """
        try:

            if self.readMode == 1:
                self.card.task_stop(self.readTask)
                self.card.task_delete(self.readTask)

            self.card.close()
            print('QArm terminated successfully.')

        except HILError as h:
            print(h.get_error_message())

    def __enter__(self):
        """
        Used for the `with` statement.

        Returns
        -------
        QArm
            The current instance of the class.
        """
        return self

    def __exit__(self, type, value, traceback):
        """
        Used for the `with` statement. Terminates the connection with the QArm.

        Parameters
        ----------
        type : Exception type
            The exception type, if any.
        value : Exception value
            The exception value, if any.
        traceback : Traceback
            The traceback object, if any.
        """
        self.terminate()  



class QArmRealSense(Camera3D):
    """
    A class for accessing 3D camera data from the RealSense camera on the QArm.

    Inherits from `Camera3D` in `pal.utilities.vision`.

    Parameters
    ----------
    hardware : int, optional
        Indicates whether the camera is hardware-based (1) or virtual (0). Default is 1.
    deviceID : int, optional
        Identifier for the camera device. Default is 0.
    videoPort : int, optional
        Port number for virtual QArm. Default is 18901. 
    mode : str, optional
        Mode to use for capturing data. Default is 'RGB&DEPTH', as long as the string includes
        'rgb' and/or 'depth' it works.
    frameWidthRGB : int, optional
        Width of the RGB frame. Default is 640.
    frameHeightRGB : int, optional 
        Height of the RGB frame. Default is 400.
    frameRateRGB : int, optional
        Frame rate of the RGB camera. Default is 30.
    frameWidthDepth : int, optional
        Width of the depth frame. Default is 640.
    frameHeightDepth : int, optional
        Height of the depth frame. Default is 400.
    frameRateDepth : int, optional
        Frame rate of the depth camera. Default is 15.
    frameWidthIR : int, optional
        Width of the infrared (IR) frame. Default is 640.
    frameHeightIR : int, optional
        Height of the IR frame. Default is 400.
    frameRateIR : int, optional
        Frame rate of the IR camera. Default is 15.
    readMode : int, optional
        Mode to use for reading data from the camera. Default is 1.
    focalLengthRGB : ndarray, optional
        RGB camera focal length in pixels. Default is np.array([[None], [None]], dtype=np.float64).
    principlePointRGB : ndarray, optional
        Principle point of RGB camera in pixels. Default is np.array([[None], [None]], dtype=np.float64).
    skewRGB : float, optional
        Skew factor for RGB camera. Default is None.
    positionRGB : ndarray, optional
        Position of RGB camera in car's frame, shape (3,1). Default is array of None.
    orientationRGB : ndarray, optional
        Orientation of RGB camera in car's frame, shape (3,3). Default is array of None.
    focalLengthDepth : ndarray, optional
        Focal length of depth camera, shape (2,1). Default is array of None.
    principlePointDepth : ndarray, optional
        Principle point of depth camera, shape (2,1). Default is array of None.
    skewDepth : float, optional
        Skew of the depth camera. Default is None.
    positionDepth : ndarray, optional
        Position of depth camera, shape (3,1). Default is array of None.
    orientationDepth : ndarray, optional
        Orientation of depth camera in car's frame, shape (3,3). Default is array of None.

    Notes
    -----
    In simulation mode (hardware=0), frame dimensions are fixed to 640x480
    for all cameras.
    
    """
    def __init__(
            self,
            hardware = 1,
            deviceID = 0,
            videoPort = 18901,
            readMode=1,
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
        ):

        if hardware:
            deviceId = str(deviceID)
        else:
            deviceId = "0@tcpip://localhost:" +str(videoPort)
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

